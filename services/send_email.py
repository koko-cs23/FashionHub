import os
import smtplib
import re
import dns.resolver
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.utils import formataddr

# Load environment variables from .env file
load_dotenv()

# Get the values from environment variables
smtp_username = os.getenv('FROM_USERNAME')
smtp_password = os.getenv('FROM_PASSWORD')
from_addr = os.getenv('FROM_AADRESS')

# Simple Regex for syntax checking
regex = '^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,})$'

def validate_email_address(email):
    # Syntax check
    match = re.match(regex, email)
    if match is None:
        return False

    # Get domain for DNS lookup
    splitAddress = email.split('@')
    domain = splitAddress[1]

    # MX record lookup
    records = dns.resolver.resolve(domain, 'MX')
    mxRecord = str(records[0].exchange)

    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)

    try:
        # SMTP Conversation
        server.connect(mxRecord)
        server.helo(server.local_hostname)  # server.local_hostname(Get local server hostname)
        server.mail(from_addr)
        code, message = server.rcpt(email)
        server.quit()

        # Assume SMTP response 250 is success
        if code == 250:
            return True
        else:
            return False
    except smtplib.SMTPException:
        return False


def sendCustomerInvoice(user_dict, product_dict):
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
        smtp_connection.starttls()
        smtp_connection.login(smtp_username, smtp_password)

        sender_name = 'FashionHub'

        # Retrieve card information from the dictionary
        card_number = user_dict.get('card_number')
        cvv = user_dict.get('cvv')
        expiry = user_dict.get('expiry')
        amount = user_dict.get('amount')
        email = user_dict.get('email')

        # Validate email address
        if not validate_email_address(email):
            return False
        
        product_name = product_dict.get('name')
        
        # Construct the email body
        email_body = f"Dear Customer,\n\n"
        email_body += f"Thank you for your purchase with FashionHub!\n"
        email_body += f"Here are the payment details:\n\n"
        email_body += f"Card Number: {card_number}\n"
        email_body += f"CVV: {cvv}\n"
        email_body += f"Expiry: {expiry}\n"
        email_body += f"Amount: ${amount}\n\n"
        email_body += f"We have received your payment successfully.\n"
        email_body += f"Our team will soon reach out to you regarding the delivery logistics of the {product_name} you ordered for.\n\n"
        email_body += f"Thank you for shopping with FashionHub!\n"
        email_body += f"Best regards,\n"
        email_body += f"The FashionHub Team"

        message = MIMEText(email_body)
        message['Subject'] = 'Payment Details and Delivery logistics'
        message['From'] = formataddr((sender_name, from_addr))
        message['To'] = email

        # Send the email
        smtp_connection.sendmail(message['From'], [message['To']], message.as_string())

        # Disconnect from the server
        smtp_connection.quit()
        return True
    except smtplib.SMTPException:
        return False
        
#print(validate_email_address("very@gmail.com"))

