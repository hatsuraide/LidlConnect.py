# LidlConnect.py

[![PyPI version](https://badge.fury.io/py/LidlConnect.py.svg)](https://badge.fury.io/py/LidlConnect.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Unofficial Python library for the Lidl Connect Self-Care API (Austria).

## Installation

```bash
pip install LidlConnect.py
```

## Usage

```python
from lidlconnect import LidlConnect

with LidlConnect(identifier="069012345678", puk="12345678") as client:
    user = client.user.get()
    print(f"Name: {user['name']}")
    print(f"Balance: {client.user.balance}")

    usage = client.usage.get()
    data = client.usage.data
    print(f"Data: {data['remaining']}/{data['total']} {data['unit']}")
    print(f"Package valid until: {client.usage.valid_to}")
```

The context manager handles login and logout automatically. If you prefer manual control:

```python
client = LidlConnect(identifier="069012345678", puk="12345678")
client.initialize()

# ... do stuff ...

client.logout()
```

You can also authenticate with a password instead of PUK:

```python
client = LidlConnect(identifier="069012345678", password="yourPassword")
```

## API

The client is split into namespaced sub-clients:

### `client.user`

```python
client.user.get()           # raw user dict
client.user.name
client.user.phone_number
client.user.balance
client.user.bonus_balance
client.user.status
client.user.has_password
client.user.birth_date
client.user.customer_type
client.user.customer_language
client.user.activation_date
client.user.deactivation_date
client.user.imsi
client.user.iccid
client.user.is_esim
client.user.notification_settings
client.user.topup_settings
```

### `client.usage`

```python
client.usage.get()              # raw usage dict
client.usage.data               # {"remaining", "total", "used", "unit"}
client.usage.eu_data
client.usage.minutes
client.usage.international_minutes
client.usage.tariff_name
client.usage.valid_from
client.usage.valid_to
client.usage.next_renewal
client.usage.gross_price
client.usage.download_speed     # bytes/sec or None
client.usage.upload_speed
client.usage.queued
```

### `client.tariffs`

```python
client.tariffs.get_available()      # CMS catalog (names, descriptions)
client.tariffs.get_switchable()     # tariffs switchable at next billing cycle
client.tariffs.get_purchasable()    # add-ons available to buy now
client.tariffs.get_balance()        # account balance
client.tariffs.switch(item_id)      # schedule a tariff switch
client.tariffs.buy(item_id)         # buy an add-on immediately
```

### `client.invoices`

```python
client.invoices.get_invoices()
client.invoices.get_vouchers()
client.invoices.get_calls(page=1, size=50)
client.invoices.get_config()
client.invoices.get_timeline()
client.invoices.download_calls()    # returns bytes
client.invoices.total_spent()       # sum of invoices + vouchers
client.invoices.last_payment_date()
```

### `client.settings`

```python
client.settings.get_services()
client.settings.get_topup()
client.settings.get_consents()
client.settings.get_egn()
client.settings.update_service(service_id, active)
client.settings.update_topup(settings)
client.settings.update_notifications(email_enabled, sms_enabled)
client.settings.update_egn(mask_premium, mask_non_premium)
client.settings.update_consents(consents)
```

### `client.credit`

```python
client.credit.topup(code)
client.credit.get_balance()
client.credit.get_payment_channels()
```

## Error handling

```python
from lidlconnect import LidlConnect, AuthError, APIError

try:
    with LidlConnect(identifier="069012345678", puk="12345678") as client:
        print(client.user.balance)
except AuthError as e:
    print(f"Login failed: {e}")
except APIError as e:
    print(f"API error {e.status_code}: {e}")
```

## Requirements

- Python 3.10+
- `requests`
- `beautifulsoup4`

## License

MIT

## Disclaimer

This is an unofficial library, not affiliated with or endorsed by Lidl or any of its affiliates.
