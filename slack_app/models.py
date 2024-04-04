import boto3
from django.db import models
from django.conf import settings


class Queue(models.Model):
    name = models.CharField(max_length=255, unique=True)
    region = models.CharField(max_length=255, default="eu-north-1")

    def __str__(self):
        return self.name

    def get_client(self):
        if not hasattr(self, "client"):
            session = boto3.Session(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            )
            self.client = session.resource("sqs", region_name=self.region)
            return self.client
        return self.client

    def get_aws_queue(self):
        self.get_client()
        return self.client.get_queue_by_name(QueueName=self.name)
