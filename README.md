# Ticket Webhook Logger

This project is a lightweight Python webhook receiver that listens for incoming **HTTP POST requests** and logs **ticket resolution data** to a **PostgreSQL** database.

It uses:

- 🐍 **Flask** – to spin up a simple local server
- 🐘 **PostgreSQL** – for storing ticket data
- 🔁 **Python requests** – for testing the webhook
- 🔐 Environment variables (.env) for secure database credentials

---

## ✅ What This Project Demonstrates

- Receiving POST webhooks with JSON data
- Writing data to a PostgreSQL database using `psycopg2`
- Testing the webhook locally using a Python script instead of curl
- Using a virtual environment for clean package management

---

![Webhook to Postgres Flow](https://raw.githubusercontent.com/YOUR_USERNAME/YOUR_REPO/main/images/postgres_webhook_flow.png)

> Replace the image link above with your actual GitHub image path once added.