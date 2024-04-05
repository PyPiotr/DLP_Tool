Data Loss Prevention Tool
==========================

Simple system that secures the organization communication channels but listening to messages flowing in and scanning them using a set of security tools.

SetUp
-----

Environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To operate the system, you must establish a ".env" directory at the project's root. This directory is essential for configuring environment variables required by the Django and MySQL containers.

==================================  ===============================================================================
Variable                             Description
----------------------------------  -------------------------------------------------------------------------------
SLACK_BOT_TOKEN                     Slack's app token; scopes and permissions will be described in the next section
SLACK_SIGNING_SECRET                Slack's secret token
AWS_ACCESS_KEY_ID                   Access id from AWS user must have read and write permissions for SQS
AWS_SECRET_ACCESS_KEY               AWS secret key
AWS_QUEUE                           The name of the SQS queue
AWS_QUEUE_REGION                    The name of the SQS region
DJANGO_DEFAULT_SUPERUSER_EMAIL      Django's superuser email
DJANGO_DEFAULT_SUPERUSER_USERNAME   Django's superuser usernam
DJANGO_DEFAULT_SUPERUSER_PASSWORD   Django's superuser pass
MYSQL_PORT                          ``3306`` recommended
MYSQL_ROOT_HOST                     ``mysql`` value recomended
MYSQL_DATABASE                      ``avanan`` value recomended
MYSQL_USER                          User
MYSQL_PASSWORD                      Password
MYSQL_ALLOW_EMPTY_PASSWORD          ``true`` recommended
==================================  ===============================================================================


Slack Config
^^^^^^^^^^^^^^

1. Begin by navigating to the Slack application panel within the Slack API section <https://api.slack.com/apps>_. Look for the "create new app" button.
2. Next, click on "create an app from scratch".
3. Provide a name for your app and select the workspace where you intend to create the bot.
4. You will then be directed to the page for configuring the app. Set the parameters to grant access to your bot within your workspace.
5. Proceed to the "OAuth & Permissions" tab under Features in the left panel.
6. Under the "Bot Token Scopes" section, add the following scopes:

  - app_mentions:read
  - channels:history
  - chat:write
  - files:read
  - groups:history
  - im:history
  - links:read
  - mpim:history
  - remote_files:write
7. Under the "User Token Scopes" section, add the following scopes:
  - channels:history
  - files:read
  - groups:history
  - chat:write
  - im:read
  - links:read
  - mpim:history
8. Navigate to the event subscriptions menu and enable the Event API by toggling the button to "on". Enter the full URL (including the domain) for the event subscription.
9. The URL format should be $YOUR_DOMAIN/slack/events/.
10. With the service running, provide the URL. Slack will attempt to access the URL, and upon receiving a 200 HTTP code, the subscription will be authorized. Click "Save changes".
11. Remember to install the app with a user that has administrative permissions in the workplace.
12. Ensure that the bot is added to the workspace that will be monitored.

DNS Configuration
^^^^^^^^^^^^^^^^^^^
Since we're utilizing HTTP events instead of socket methods, a publicly accessible domain is required. If you have one, you can skip this section. Otherwise, you can create a ngrok account and set it up according to its documentation_.

In another terminal, run the following command::
    $ ngrok http 8000

This will proxy port 8000 to port 80 or 443.

Deployment
^^^^^^^^^^^
The following outlines the deployment procedure for this application::
    $ docker-compose up --build 

