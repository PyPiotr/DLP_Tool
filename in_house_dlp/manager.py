import asyncio
import json
import logging
import re
import boto3
import MySQLdb
import os

logger = logging.getLogger(__name__)


class Manager:

    def __init__(self):
        self.config = {
            "queue_name": os.environ["AWS_QUEUE"],
            "region": os.environ.get("AWS_QUEUE_REGION"),
            "AWS_ACCESS_KEY_ID": os.environ["AWS_ACCESS_KEY_ID"],
            "AWS_SECRET_ACCESS_KEY": os.environ["AWS_SECRET_ACCESS_KEY"],
            "db_host": os.environ["MYSQL_ROOT_HOST"],
            "db_port": os.environ["MYSQL_PORT"],
            "db_user": os.environ["MYSQL_USER"],
            "db_password": os.environ["MYSQL_PASSWORD"],
            "db_name": os.environ["MYSQL_DATABASE"],
        }
        self.loop = asyncio.get_event_loop()
        self._queue_db: asyncio.Queue = asyncio.Queue()
        self._queue_django: asyncio.Queue = asyncio.Queue()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        logger.warning("exit from context manager.")
        pass

    async def run(self):  # pragma: no cover
        await self.start()

    async def start(self):
        asyncio.ensure_future(self.main(), loop=self.loop)

    async def get_boto_client(self):
        if not hasattr(self, "client"):
            session = boto3.Session(
                aws_access_key_id=self.config.get("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=self.config.get("AWS_SECRET_ACCESS_KEY"),
            )
            self.client = session.resource("sqs", region_name=self.config.get("region"))
            return self.client
        return self.client

    async def get_aws_queue(self):
        await self.get_boto_client()
        return self.client.get_queue_by_name(QueueName=self.config.get("queue_name"))

    async def check_message(self, event):
        select_command = "SELECT * FROM dlp_app_losspreventionpattern"
        db = MySQLdb.connect(
            host=self.config.get("db_host"),
            user=self.config.get("db_user"),
            passwd=self.config.get("db_password"),
            db=self.config.get("db_name"),
        )
        cur = db.cursor()
        cur.execute(select_command)
        results = cur.fetchall()
        await self.check_regex_match(event, results)

    async def execute_sql(self, command, commit=True):
        db = MySQLdb.connect(
            host=self.config.get("db_host"),
            user=self.config.get("db_user"),
            passwd=self.config.get("db_password"),
            db=self.config.get("db_name"),
        )
        cur = db.cursor()
        logger.warning(command)
        cur.execute(command)
        if commit:
            db.commit()
        return cur.fetchall()

    async def check_regex_match(self, event, results):
        for line in results:
            pattern = re.compile(line[2])
            leak = False
            insert_command = f"""
                INSERT INTO dlp_app_dataleak (message, channel, pattern_id) VALUES ('{event.get('text')}', '{event['channel']}', '{line[0]}');
            """
            if event.get("text") and pattern.match(event.get("text")):
                leak = True
            if leak:
                await self.execute_sql(insert_command)

    async def _get_messages(self):
        """Read and pop messages from SQS queue"""
        queue = await self.get_aws_queue()
        for message in queue.receive_messages():
            message_dict = json.loads(message.body)
            logger.warning("msg detected")
            logger.warning(f"msg... \n{str(message_dict)}")
            await self.check_message(message_dict)
            logger.warning("no more messages...")
            message.delete()

    async def main(self):
        logger.warning("Initializing main loop....")
        while True:
            await self._get_messages()


async def main():
    controller = Manager()
    await controller.run()


asyncio.run(main())
