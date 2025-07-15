# `tap-opentable`

This is a Singer tap for [OpenTable](https://www.opentable.com/restaurant-solutions), designed to sync critical restaurant data including reservations, menus, reviews, and availability.

This tap is built with the [Meltano Singer SDK](https://sdk.meltano.com) and is a product of [Dishio](https://dish.io).

## Introduction

The OpenTable API ecosystem allows restaurants and partners to extend the core functionality of OpenTable. This tap leverages those APIs to extract valuable data for analysis, integration, or backup purposes. It handles authentication, pagination, and data extraction for key OpenTable resources.

Key features include:

  * **OAuth 2.0 Authentication:** Securely connects to the OpenTable API using the Client Credentials flow.
  * **Dynamic Environments:** Easily switch between OpenTable's Sandbox and Production environments.
  * **Multiple Data Streams:** Syncs comprehensive data including Restaurants, Reservations, Menus, Reviews, and Availability.
  * **Incremental Sync:** For streams that support it, the tap will only sync new or updated data, saving time and resources.

## Getting Started

### 1\. Prerequisites

Before you can use this tap, you must be an approved OpenTable integration partner.

  * **Apply for Partnership:** Fill out the application form at [OpenTable API Partners](https://www.opentable.com/restaurant-solutions/api-partners/become-a-partner/).
  * **Receive Credentials:** Once your application is approved, the OpenTable partnerships team will provide you with a `Client ID` and `Client Secret` for both their Sandbox and Production environments.
  * **Subscribe to Status Updates:** It is required that you subscribe to the [OpenTable API Status Dashboard](https://www.google.com/search?q=https://status-api.opentable.com/subscribe) to stay informed about maintenance and outages.

### 2\. Installation

Install the tap using `pip`:

```bash
pip install tap-opentable
```

*Note: The final installation command may vary depending on the package repository.*

### 3\. Configuration

Create a `config.json` file in your project directory containing your API credentials and settings.

#### Configuration Settings:

| Setting                 | Required | Default | Description                                                                                                                                              |
|:------------------------|:--------:|:-------:|:---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `client_id`             | **True** | `None`  | Your OpenTable application's Client ID.                                                                                                                  |
| `client_secret`         | **True** | `None`  | Your OpenTable application's Client Secret.                                                                                                              |
| `is_pre_production`     | False    | `True`  | If `true`, the tap uses the Sandbox/Pre-production environment (`platform.otqa.com`). If `false`, it uses the Production environment (`platform.opentable.com`). |
| `start_date`            | False    | `None`  | The earliest record date to sync for incremental streams (e.g., `reservations`). Format: `YYYY-MM-DDTHH:MM:SSZ`.                                          |

#### Example `config.json`:

```json
{
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "is_pre_production": true,
  "start_date": "2024-01-01T00:00:00Z"
}
```

## Onboarding & Authentication Flow

This tap automates the **OAuth 2.0 Client Credentials** grant type required by OpenTable.

1.  **Provide Credentials:** You provide your `client_id` and `client_secret` in the `config.json` file.
2.  **Select Environment:** The `is_pre_production` flag determines which environment the tap targets:
      * **Sandbox (True):**
          * OAuth Host: `https://oauth-pp.opentable.com`
          * API Host: `https://platform.otqa.com`
      * **Production (False):**
          * OAuth Host: `https://oauth.opentable.com`
          * API Host: `https://platform.opentable.com`
3.  **Token Exchange:** The tap automatically requests a bearer token from the appropriate OAuth host.
4.  **API Requests:** The obtained token is then used to authenticate all subsequent requests to the OpenTable API. The tap manages token expiration and renewal internally.


## Synced Data Streams

This tap supports the following data streams. Child streams are synced for each parent record discovered.

| Stream           | Type          | Replication Key | Parent Stream | Description                                                                   |
|:-----------------|:--------------|:----------------|:--------------|:------------------------------------------------------------------------------|
| **`restaurants`**| Full Table    | `None`          | `N/A`         | Syncs core details for each restaurant associated with your partner account.    |
| **`reservations`** | Incremental   | `modified_at`   | `restaurants` | Syncs reservation data for each restaurant, including status and guest info.  |
| **`menus`** | Incremental   | `modified_at`   | `restaurants` | Syncs menu details, including sections and items, for each restaurant.        |
| **`reviews`** | Incremental   | `dined_at`      | `restaurants` | Syncs guest reviews and detailed ratings for each restaurant.                 |
| **`availability`** | Full Table    | `None`          | `restaurants` | Syncs upcoming reservation availability for the next 7 days for each restaurant. |

## Technical Details

  * **API Protocol:** All communication is over HTTPS. As of **October 6, 2025**, OpenTable will require **TLS 1.3**.
  * **Data Format:** The tap expects and receives data in `JSON` format.
  * **Compression:** To improve performance, OpenTable supports `lz4` encoding. The tap should handle this automatically.
  * **Idempotency:** For `POST`, `PUT`, and `PATCH` requests, a unique `X-Request-Id` header is used to ensure idempotent processing. This is managed by the underlying Singer SDK.

## Usage

You can run `tap-opentable` directly from the command line.

1.  **Discover Streams:**
    Generate a `catalog.json` file which describes the available streams and their schemas.

    ```bash
    tap-opentable --config config.json --discover > catalog.json
    ```

2.  **Run a Sync:**
    Execute the tap to sync data based on the catalog's configuration.

    ```bash
    tap-opentable --config config.json --catalog catalog.json
    ```

    *You can edit `catalog.json` to select which streams and fields to sync.*

## Developer Resources

### Development Environment

Set up your development environment using `poetry`:

```bash
poetry install
```

### Testing

Run the test suite using `pytest`:

```bash
poetry run pytest
```

You can also use `tox` to run tests across multiple Python versions:

```bash
tox
```
