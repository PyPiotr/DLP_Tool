import logging
from slack_bolt import App
from django.conf import settings
from slack_app.models import Queue
import json

logger = logging.getLogger(__name__)


app = App(
    token=settings.SLACK_BOT_TOKEN,
    signing_secret=settings.SLACK_SIGNING_SECRET,
    # disable eagerly verifying the given SLACK_BOT_TOKEN value
    token_verification_enabled=False,
)


def send_msg_to_sqs(message):
    queue_instance, created = Queue.objects.get_or_create(
        name=settings.AWS_QUEUE, region=settings.AWS_QUEUE_REGION
    )
    queue = queue_instance.get_aws_queue()
    response = queue.send_message(MessageBody=message)
    print(response)
    return response


@app.event("message")
def handle_app_messages(logger, event, ack, say):
    logger.info(event)
    ack()
    send_msg_to_sqs(json.dumps(event))


@app.event("app_mention")
def handle_app_mentions(logger, event, say):
    logger.info(event)
    say(f"Hi there, <@{event['user']}>")
    send_msg_to_sqs(json.dumps(event))
