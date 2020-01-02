# -*- coding: utf-8 -*-

"""Update and trigger alerts."""

from dotenv import load_dotenv

from models.alert import Alert

# Alert uses Mailgun to send email notifications. The Mailgun library requires
# environment variables which have not yet been loaded, so load them here.
load_dotenv()

alerts = Alert.fetch_all()

for alert in alerts:
    alert.fetch_item_price()
    alert.notify_if_price_reached()
    #alert.json()

if not alerts:
    print('No alerts have been created. Add an item and alert to begin.')
