# LidlConnect API Documentation

A Python client library for interacting with the Lidl Connect Self-Care portal API.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Authentication](#authentication)
- [Core Client](#core-client)
- [Usage Data](#usage-data)
- [User Information](#user-information)
- [Tariffs](#tariffs)
- [Invoices and Payments](#invoices-and-payments)
- [Utility Methods](#utility-methods)
- [Caching](#caching)
- [Error Handling](#error-handling)

## Installation

```python
# Clone the repository
git clone https://github.com/MarcUs7i/LidlConnect.git

# Install dependencies
pip install -r requirements.txt
```

Required dependencies:
- `requests`
- `beautifulsoup4`

## Quick Start

```python
from LidlConnect import LidlConnect

# Initialize with PUK
client = LidlConnect(identifier="069012345678", puk="12345678")

# Or initialize with password
# client = LidlConnect(identifier="069012345678", password="yourPassword")

# Login and initialize connection
if not client.initialize():
    print("Failed to initialize client")
    exit(1)

# Get usage information
data_info = client.get_remaining_data()
print(f"Data: {data_info['remaining']}/{data_info['total']} GiB")

# Logout when done
client.logout()
```

## Authentication

### LidlConnect(identifier, puk=None, password=None)

Initialize the Lidl Connect client.

**Parameters:**
- `identifier` (str): Your phone number or customer ID
- `puk` (str, optional): Your PUK code (required if password not provided)
- `password` (str, optional): Your password (required if PUK not provided)

**Example:**
```python
# Using PUK
client = LidlConnect(identifier="069012345678", puk="12345678")

# Using password
client = LidlConnect(identifier="069012345678", password="yourPassword")
```

### initialize() → bool

Initialize the client by logging in, fetching the dashboard, and extracting necessary tokens and IDs.

**Returns:**
- `bool`: True if initialization successful, False otherwise

**Example:**
```python
if not client.initialize():
    print("Failed to initialize client")
    exit(1)
```

### login() → bool

Log in to Lidl Connect using the provided credentials.

**Returns:**
- `bool`: True if login successful, False otherwise

**Example:**
```python
success = client.login()
```

### logout() → bool

Log out from Lidl Connect, clearing the session.

**Returns:**
- `bool`: True if logout successful, False otherwise

**Example:**
```python
client.logout()
```

## Core Client

The client automatically handles session management and token extraction, it tries to log out when the program is about to exit or to get killed.

**Properties:**
- `identifier` (str): The phone number or customer ID
- `user_id` (int): The user ID extracted from the dashboard
- `endpoint_id` (int): The endpoint ID extracted from the dashboard
- `logged_in` (bool): Whether the client is currently logged in
- `csrf_token` (str): The CSRF token for API requests

## Usage Data

Methods for getting and displaying usage data.

### get_usage_data() → Dict[str, Any]

Get raw usage data for the current account.

**Returns:**
- `Dict[str, Any]`: Usage data including instanceGroups with counters

**Cache TTL:** 5 seconds

**Example:**
```python
usage_data = client.get_usage_data()
```

### print_usage_summary(data=None) → None

Pretty-print usage summary data.

**Parameters:**
- `data` (Dict[str, Any], optional): Optional usage data. If None, will fetch new data

**Example:**
```python
client.print_usage_summary()
```

### get_remaining_data() → Dict[str, float]

Get remaining data balance (in GiB).

**Returns:**
- `Dict[str, float]`: Dictionary with keys "remaining", "total", and "used" in GiB

**Example:**
```python
data_info = client.get_remaining_data()
print(f"Data: {data_info['remaining']}/{data_info['total']} GiB")
```

### get_remaining_eu_data() → Dict[str, float]

Get remaining EU data balance (in GiB).

**Returns:**
- `Dict[str, float]`: Dictionary with keys "remaining", "total", and "used" in GiB

**Example:**
```python
eu_data_info = client.get_remaining_eu_data()
print(f"EU Data: {eu_data_info['remaining']}/{eu_data_info['total']} GiB")
```

### get_remaining_minutes() → Dict[str, float]

Get remaining voice minutes.

**Returns:**
- `Dict[str, float]`: Dictionary with keys "remaining", "total", and "used" in minutes

**Example:**
```python
minutes_info = client.get_remaining_minutes()
print(f"Minutes: {minutes_info['remaining']}/{minutes_info['total']} minutes")
```

### tariff_package_valid_from → Optional[str]

Get the start date of the current tariff package.

**Returns:**
- `str`: ISO formatted date string or None if not available

**Example:**
```python
print(f"Package valid from: {client.tariff_package_valid_from}")
```

### tariff_package_valid_to → Optional[str]

Get the end date of the current tariff package.

**Returns:**
- `str`: ISO formatted date string or None if not available

**Example:**
```python
print(f"Package valid to: {client.tariff_package_valid_to}")
```

### tariff_package_details → Optional[Dict[str, Any]]

Get detailed information about the current tariff package.

**Returns:**
- `Dict[str, Any]`: Dictionary containing name, category, validFrom, validTo and counter details or None if not available

**Example:**
```python
details = client.tariff_package_details
if details:
    print(f"Package name: {details['name']}")
    print(f"Valid from: {details['validFrom']} to {details['validTo']}")
```

## User Information

Methods for retrieving user account information.

### _get_user_data() → Dict[str, Any]

Get user data from the server. This is an internal method used by the properties below.

**Returns:**
- `Dict[str, Any]`: User data including name, type, accounts, etc.

**Cache TTL:** 30 seconds

### user_name → Optional[str]

Get user's name.

**Returns:**
- `str`: User's name or None if not available

**Example:**
```python
print(f"User name: {client.user_name}")
```

### user_type → Optional[str]

Get user's type (e.g., 'CUSTOMER').

**Returns:**
- `str`: User type or None if not available

**Example:**
```python
print(f"User type: {client.user_type}")
```

### has_password → bool

Check if user has set a password.

**Returns:**
- `bool`: True if the user has a password, False otherwise

**Example:**
```python
if client.has_password:
    print("User has a password set")
```

### birth_date → Optional[str]

Get user's birth date.

**Returns:**
- `str`: Birth date or None if not available

**Example:**
```python
print(f"Birth date: {client.birth_date}")
```

### status → Optional[str]

Get endpoint status (e.g., 'ACTIVE').

**Returns:**
- `str`: Endpoint status or None if not available

**Example:**
```python
print(f"Status: {client.status}")
```

### customer_type → Optional[str]

Get customer type (e.g., 'ANONYM').

**Returns:**
- `str`: Customer type or None if not available

**Example:**
```python
print(f"Customer type: {client.customer_type}")
```

### customer_language → Optional[str]

Get customer language preference.

**Returns:**
- `str`: Customer language or None if not available

**Example:**
```python
print(f"Language: {client.customer_language}")
```

### balance → Optional[float]

Get account balance.

**Returns:**
- `float`: Account balance or None if not available

**Example:**
```python
print(f"Balance: €{client.balance if client.balance is not None else 'N/A'}")
```

### activation_date → Optional[str]

Get activation date.

**Returns:**
- `str`: ISO formatted activation date or None if not available

**Example:**
```python
print(f"Activation date: {client.activation_date}")
```

### deactivation_date → Optional[str]

Get deactivation date.

**Returns:**
- `str`: ISO formatted deactivation date or None if not available

**Example:**
```python
print(f"Deactivation date: {client.deactivation_date}")
```

## Tariffs

Methods for retrieving and displaying available tariffs.

### get_tariffs() → List[Dict[str, Any]]

Get all available tariffs for the current account.

**Returns:**
- `List[Dict[str, Any]]`: List of tariff objects with relevant information

**Cache TTL:** 60 seconds

**Example:**
```python
tariffs = client.get_tariffs()
```

### print_tariffs() → None

Pretty-print available tariffs.

**Example:**
```python
client.print_tariffs()
```

The output includes:
- Tariff name (German name if available)
- Tariff ID
- Details (cleaned from HTML, can look terrible)
- Featured status
- Visibility status

## Invoices and Payments

Methods for getting and displaying invoice and voucher history.

### get_invoices() → List[Dict[str, Any]]

Get list of invoices for the current account.

**Returns:**
- `List[Dict[str, Any]]`: List of invoice objects with transaction details

**Cache TTL:** 30 seconds

**Example:**
```python
invoices = client.get_invoices()
```

### get_vouchers() → List[Dict[str, Any]]

Get list of consumed vouchers for the current account.

**Returns:**
- `List[Dict[str, Any]]`: List of voucher objects with transaction details

**Cache TTL:** 30 seconds

**Example:**
```python
vouchers = client.get_vouchers()
```

### print_invoices() → None

Pretty-print invoice and voucher history.

**Example:**
```python
client.print_invoices()
```

The output includes:
- Transaction details for invoices (ID, date, amount, payment method)
- Voucher details (ID, serial, value, consumption date)

### get_total_spent() → float

Calculate the total amount spent across all invoices and vouchers.

**Returns:**
- `float`: Total amount in euros

**Example:**
```python
total = client.get_total_spent()
print(f"Total spent: €{total:.2f}")
```

### last_payment_date → Optional[str]

Get the date of the most recent payment from either invoices or vouchers.

**Returns:**
- `str`: ISO formatted date string or None if no payments

**Example:**
```python
print(f"Last payment date: {client.last_payment_date}")
```

## Utility Methods

General API utilities for Lidl Connect.

### make_api_request(url, data=None, method="POST") → Union[Dict[str, Any], str]

Make a generic API request to Lidl Connect.

**Parameters:**
- `url` (str): API endpoint to call
- `data` (Dict, optional): Payload to send
- `method` (str, optional): HTTP method (default: "POST")

**Returns:**
- `Dict[str, Any]` or `str`: API response (JSON parsed if Content-Type is application/json)

**Example:**
```python
response = client.make_api_request(
    "https://selfcare.lidl-connect.at/customer/some-endpoint", 
    data={"key": "value"}
)
```

## Caching

The library has a time-based cache for API requests to reduce load and improve performance.

Key caching parameters:
- Usage data: 5 seconds TTL
- User data: 30 seconds TTL
- Invoices and vouchers: 30 seconds TTL
- Tariffs: 60 seconds TTL

The cache is implemented using the `ttl_cache` decorator in helpers.py.

## Error Handling

Most methods raise `ValueError` exceptions when:
- Not logged in or missing CSRF token
- API requests fail
- Required data is missing

All public properties safely handle exceptions internally and return None when errors occur, ensuring your application doesn't crash.

Example of error handling:

```python
try:
    client = LidlConnect(identifier="069012345678", puk="12345678")
    if not client.initialize():
        print("Failed to initialize client")
        exit(1)
        
    # Your code here
    
except ValueError as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    if hasattr(client, 'logout') and client.logged_in:
        client.logout()
```