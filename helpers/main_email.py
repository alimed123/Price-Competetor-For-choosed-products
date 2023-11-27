# import sys
# sys.path.insert(1, '/home/marketpro/public_html/dev/common')
# from main_email import send_email
# from main_email import send_email_attachment
# from main_email import send_html_email
# send_email(to_email,email_subject,email_message)
# send_email_attachment(to_email,email_subject,email_message,file_name_with_path):
# send_html_email(to_email,email_subject,email_message):


import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from dotenv import load_dotenv
import os

load_dotenv()

# Use this to change between "DEV" and "PROD" .env variables
ENV = os.getenv("PROD")

ORCAEMAIL = os.getenv("ORCAEMAIL")

def send_email(to_email,email_subject,email_message):

    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = os.getenv(f"{ENV}_SENDER_EMAIL")
    password = os.getenv(f"{ENV}_SENDER_PASSWORD")
    receiver_email = to_email
    subject = email_subject
    body = email_message

    message = f"Subject: {subject}\n\n{body}"

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

        server.quit()





# send_email('vivekjainindia@gmail.com','Simple Email', 'This is simple message')


#* Remember to pass full path as filename
def send_email_attachment(to_email,email_subject,email_message,file_name_with_path):
    
    receiver_email = to_email
    subject = email_subject
    body = email_message
    sender_email = os.getenv(f"{ENV}_SENDER_EMAIL")
    password = os.getenv(f"{ENV}_SENDER_PASSWORD")

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = file_name_with_path  # pass full path

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:

        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)


    # Add header as key/value pair to attachment part

    part.add_header(

        "Content-Disposition",

        f"attachment; filename= {filename}",

    )



    # Add attachment to message and convert message to string

    message.attach(part)
    text = message.as_string()


    # Log in to server using secure context and send email

    # context = ssl.create_default_context()
    # with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    #     server.login(sender_email, password)
    #     server.sendmail(sender_email, receiver_email, text)
    #     server.quit()
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
    server.quit()



def send_html_email(to_email,email_subject,email_message, files = []):

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = email_subject
    msg['From'] = os.getenv(f"{ENV}_SENDER_EMAIL")
    msg['To'] = to_email

    # Create the body of the message (a plain-text and an HTML version).
    text = "Plain Text, Ignore"
    html = email_message

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Attach file if present
    if files:
        for f in files:
            filename = os.path.basename(f)
            attachment = MIMEApplication(open(f, "rb").read(), _subtype='txt')
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(attachment)

    # Send the message via local SMTP server.
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login(os.getenv(f"{ENV}_SENDER_EMAIL"), os.getenv(f"{ENV}_SENDER_PASSWORD"))
    mail.sendmail(os.getenv(f"{ENV}_SENDER_EMAIL"), to_email, msg.as_string())
    mail.quit()



#send_email_attachment('vivekjainindia@gmail.com',"new server test","test body","/home/orcacorp/public_html/common/report.pdf")

#more examples https://docs.python.org/3/library/email.examples.html