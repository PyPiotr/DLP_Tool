import json
from django.urls import path
from slack_bolt.adapter.django import SlackRequestHandler
from .slack_listener import app
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt


handler = SlackRequestHandler(app=app)

@csrf_exempt
def slack_events_handler(request: HttpRequest):
    payload = json.loads(request.body)
    print(payload)
    return handler.handle(request)


urlpatterns = [
    path("slack/events", slack_events_handler, name="slack_events"),
]
