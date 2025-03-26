# Ticket Webhook Logger

This project is a lightweight, full-stack webhook solution for logging **ticket resolution data** from **Microsoft Dataverse** into a **PostgreSQL** database using a custom **Flask** API.

It includes:

- **Power Automate** — detects when a ticket is marked as "Resolved" and sends a POST request
- **Flask** — receives and authenticates incoming webhook requests via header token
- **PostgreSQL** — stores the ticket resolution data in a structured table
- **Ngrok** — exposes your local Flask app to receive webhooks from Power Automate
- **Python requests** — for local testing of the webhook with test data
- **Environment variables (`.env`)** — securely manage DB connection info and webhook secret

---

## What This Project Demonstrates

- Receiving POST webhooks with JSON data
- Writing data to a PostgreSQL database using `psycopg2`
- Testing the webhook locally using a Python script instead of curl
- Using a virtual environment for clean package management

---

> **Demo in Action**  
> Watch the end-to-end webhook flow in this GIF — Ticket Resolved → Trigger Flow to Send POST Request→ Flask → PostgreSQL:

![Webhook to Postgres Flow](https://raw.githubusercontent.com/jonathanduru/TicketWebhookLogger/refs/heads/main/images/webhook-demo2.gif)

---


## Project Setup

To run this project locally, follow these steps:

### 1. Clone the Repository
```bash
git clone https://github.com/jonathanduru/TicketWebhookLogger.git
cd TicketWebhookLogger
```

### 2. Set Up the Python Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Required Packages
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and add your database credentials and token:
```env
DB_HOST=your_host_url
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_PORT=5432
WEBHOOK_SECRET=your_webhook_token
```

### 5. Create the Database Table
```bash
python create_table.py
```
To add columns later (like `received_at`), use:
```bash
python alter_table.py
```

### 6. Start the Flask Server
```bash
flask run
```
This runs the webhook listener at `http://127.0.0.1:5000`. You can use Ngrok to expose your server:
```bash
ngrok http 5000
```

<div align="center">
  <img src="https://raw.githubusercontent.com/jonathanduru/TicketWebhookLogger/main/images/WebhookLoggerFlowChart.png" alt="Webhook to Postgres Flow" width="300"/>
</div>

---

## Power Automate Flow

This section explains how to configure a Microsoft Power Automate flow to trigger your webhook when a ticket is marked as **Resolved** in Dataverse.

### 1. Create an Automated Cloud Flow
- Go to [Power Automate](https://flow.microsoft.com).
- Create an **"Automated Cloud Flow"**. 
- Set the trigger:  
  `When a row is added, modified or deleted` (Microsoft Dataverse)

### 2. Configure the Trigger
- **Change Type**: `Modified`
- **Table Name**: `ticket` *(or your custom ticket table)*
- **Scope**: `Organization`
- **Select Columns**: `status`
- **Filter Rows**:  
  ```plaintext
  status eq 165790002
  ```
  *(Replace with the status code for "Resolved" in your system, in this case it was 165790002)*

### 3. Add a Compose Action (Optional)
- Add a **Compose** step called `Compose - X-Auth-Token Password`.
- Use this to securely store the webhook secret token (e.g., `super-secret-1234`).
- Refer to it in the HTTP step as:  
  `@outputs('Compose_-_X-Auth-Token_Password')`

### 4. Add an HTTP POST Action
- Action: **HTTP**
- **Method**: `POST`
- **URI**: Your public ngrok forwarding URL + `/log-ticket`  
  *(e.g., `https://abc123.ngrok-free.app/log-ticket`)*
- **Headers**:
  ```json
  {
    "Content-Type": "application/json",
    "X-Auth-Token": "@outputs('Compose_-_Password')"
  }
  ```
- **Body**:
  ```json
  {
    "ticket_id": "@{triggerOutputs()?['body/cr42f_ticketid_pk']}",
    "title": "@{triggerOutputs()?['body/cr42f_title']}",
    "resolution_notes": "@{triggerOutputs()?['body/cr42f_resolutionnotesnew']}"
  }
  ```

> *This step sends the relevant ticket info as JSON to your Flask webhook when the ticket is marked as resolved.*

![Flow Screenshot](https://raw.githubusercontent.com/jonathanduru/TicketWebhookLogger/refs/heads/main/images/HTTP_POST_Flow.png)

---

**Next:** Test it by resolving a ticket in Dataverse and watch your Flask terminal + database update in real time!

---

## How the Webhook Works

This section explains the flow of data from Power Platform to PostgreSQL when a ticket is marked as resolved.

### 1. Dataverse Ticket Status Updates

The webhook flow begins when a ticket's status is changed in **Dataverse**. Power Automate monitors the ticket table for changes and filters for records where the status equals `165790002` (Resolved).

### 2. Power Automate Triggers the Webhook

Power Automate uses an HTTP action to send a **POST request** to your Flask webhook endpoint. The request includes a small JSON payload containing:

- `ticket_id`
- `title`
- `resolution_notes`

A custom **X-Auth-Token** header is also included to authenticate the request.

### 3. Flask Webhook Receives and Validates

Your Flask server:

- Listens for POST requests at the `/log-ticket` endpoint.
- Verifies the `X-Auth-Token` against the secret stored in your `.env` file.
- Parses the incoming JSON payload.

If the token is valid, it proceeds to write the data to PostgreSQL. Otherwise, it returns a 403 Unauthorized response.

### 4. Data Inserted into PostgreSQL

Using `psycopg2`, the webhook inserts a new row into the `ticket_resolutions` table, including the current timestamp to mark when the webhook was received.

This lets you keep a structured log of all resolved tickets outside of Power Platform for backup, analytics, or integration.

---






