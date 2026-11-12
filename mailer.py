import smtplib
from models import EmailSubscriber, Competition
import os
from dotenv import load_dotenv
import ssl
from email.message import EmailMessage
from email.utils import formataddr

load_dotenv()
EMAIL = str(os.getenv("EMAIL"))
PASSWORD = str(os.getenv("EMAIL_PASSWORD"))

def connect() -> smtplib.SMTP_SSL:
    context = ssl.create_default_context()
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)
    smtp.login(EMAIL, PASSWORD)
    return smtp

def notify(smtp: smtplib.SMTP_SSL, subscriber: EmailSubscriber, competition: Competition) -> None:
    sender_name = "Competition Notifications"
    subject: str = f'[Competition Announcement] {competition.name} is announced'
    body = f"""<html>
    <body>
        <p>Dear {subscriber.name},</p>
        <p>{competition.name} has just been announced on the WCA Website, and will take place in {competition.city} on {competition.format_dates()}.</p>
        <p>Registration for this competition opens at {competition.registration_open_with_timezone('Europe/Oslo').strftime('%H:%M on %A %b %d')}, with a competitor limit of {competition.competitor_limit}.</p>
        <p>You can register for this competition <a href="https://worldcubeassociation.org/competitions/{competition.id}">here</a>.</p>
        <p>Best regards,<br>{competition.list_officials()}</p>
    </body>
</html>"""

    em = EmailMessage()
    em['From'] = formataddr((sender_name, EMAIL))
    em['To'] = subscriber.email
    em['Subject'] = subject
    em.set_content(body, subtype='html')

    smtp.sendmail(EMAIL, subscriber.email, em.as_string())
