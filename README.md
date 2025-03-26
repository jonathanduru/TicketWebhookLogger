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

<div align="center">
  <img src="https://raw.githubusercontent.com/jonathanduru/TicketWebhookLogger/main/images/WebhookLoggerFlowChart.png" alt="Webhook to Postgres Flow" width="300"/>
</div>

