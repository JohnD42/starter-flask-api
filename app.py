from flask import Flask
from flask import Flask, request, jsonify
import ssl
import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS

app = Flask(__name__)

load_dotenv()

CORS(app)

@app.route('/')
@app.route('/index')
def index():
    return "Hello, this is my API! You can't do anything with it from this link."

@app.route('/contact', methods=["POST", "OPTIONS"])
def contact():
    req = request.get_json()
    email = req['email']
    message = req['message']
    if message is None:
        return jsonify({"msg": "No message was provided."}), 400
    if email is None:
        return jsonify({"msg": "No email was provided."}), 400
    
    print(os.environ)
    EMAIL_SENDER = os.getenv('EMAIL_SENDER')
    print(EMAIL_SENDER)
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
    print(EMAIL_PASSWORD)
    email_receiver = 'johndurtka@gmail.com'
    email_body = f"Message from {email}: {message}"

    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = email_receiver
    msg['Subject'] = 'Contact from Personal Portfolio Website'

    msg.attach(MIMEText(email_body, 'plain'))

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
    return jsonify({"msg": "Message sent!"}), 200 

@app.before_request 
def before_request(): 
    headers = { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS', 'Access-Control-Allow-Headers': 'Content-Type' } 
    if request.method == 'OPTIONS' or request.method == 'options': 
        return jsonify(headers), 200