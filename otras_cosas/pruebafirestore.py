from google.cloud import functions
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import base64
from email.message import EmailMessage

def send_email(to, subject, body):
    credentials = Credentials.from_service_account_file("service_account.json")
    service = build('gmail', 'v1', credentials=credentials)
    message = EmailMessage()
    message.set_content(body)
    message['to'] = to
    message['subject'] = subject
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
    send_message = (service.users().messages().send(userId="me", body=create_message).execute())
    print(F'Email was sent to {to} with Email Id: {send_message["id"]}')

def send_storage_alert_email(data, context):
    object = data
    email = "your-email-address@gmail.com"
    to = "recipient-email-address@example.com"
    subject = "Firebase Storage Alert"
    body = f"An event has occurred in Firebase Storage: {object['bucket']}/{object['name']}"
    send_email(to, subject, body)

def send_logging_alert_email(data, context):
    log = data
    email = "your-email-address@gmail.com"
    to = "recipient-email-address@example.com"
    subject = "Firebase Cloud Logging Alert"
    body = f"An event has occurred in Firebase Cloud Logging: {log['jsonPayload']['message']}"
    send_email(to, subject, body)


Note que aquí se utiliza el módulo googleapiclient para enviar correos electrónicos a través de Gmail, y se utiliza google.oauth2.service_account para autenticarse en el servicio. También es necesario tener un archivo service_account.json que contenga las credenciales de la cuenta de servicio.

Como en el ejemplo anterior, deberá reemplazar your-email-address@gmail.com y recipient-email-address@example.com con las direcciones de correo electrónico apropiadas.