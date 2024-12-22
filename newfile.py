import requests
import threading
import time
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# Replace with your bot token
TELEGRAM_BOT_TOKEN = '8056935833:AAGvkytuETki9bFmvMm1hEJF8fybRAtX36c'

# Function to send a message to Telegram using a provided chat ID
def send_to_telegram(message, chat_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()  # This will raise an HTTPError for bad responses (4xx, 5xx)
        
        if response.status_code == 200:
            print(f"Message sent to {chat_id} successfully!")
        else:
            print(f"Error: {response.status_code} - {response.text}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

# Function to send a single message and avoid repeated submissions
def send_single_message(message, chat_id):
    send_to_telegram(message, chat_id)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")  # Get the merged first and last name
        chat_id = request.form.get("chat_id")  # Get the Telegram chat ID

        # Send message with the merged name once
        message = f"Name: {name}"

        # Send a single message
        send_single_message(message, chat_id)

        # Show the welcome message and photo after submission
        return render_template_string(welcome_html(name))

    # HTML and CSS for the form
    form_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Form</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f0f0;
            }

            .form-container {
                background-color: #ffffff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                width: 300px;
            }

            h2 {
                text-align: center;
                margin-bottom: 20px;
            }

            label {
                display: block;
                margin-bottom: 8px;
                font-weight: bold;
            }

            input[type="text"] {
                width: 100%;
                padding: 10px;
                margin-bottom: 15px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }

            button {
                width: 100%;
                padding: 10px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }

            button:hover {
                background-color: #45a049;
            }

            p {
                text-align: center;
                color: red;
            }
        </style>
    </head>
    <body>
        <div class="form-container">
            <h2>Submit Your Name</h2>
            <form method="POST">
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" placeholder="Name" required>
                <br>
                <label for="chat_id">Telegram Chat ID:</label>
                <input type="text" id="chat_id" name="chat_id" placeholder="Telegram Chat ID" required>
                <br>
                <button type="submit">Submit</button>
            </form>
        </div>
    </body>
    </html>
    """
    
    return render_template_string(form_html)

# HTML for the welcome page
def welcome_html(name):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Welcome</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-color: #f0f0f0;
                flex-direction: column;
                text-align: center;
            }}

            h1 {{
                font-size: 32px;
                margin-bottom: 20px;
            }}

            img {{
                width: 100%;
                height: 100%;
                object-fit: cover;
            }}
        </style>
    </head>
    <body>
        <h1>Welcome, {name}!</h1>
        <img src="data:image/jpeg;base64,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
" alt="Welcome Image" />
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(debug=True)