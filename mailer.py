import smtplib
from models import EmailSubscriber, Competition
import os
from dotenv import load_dotenv
import ssl
from email.message import EmailMessage

def notify(subscriber: EmailSubscriber, competition: Competition) -> None:
    subject: str = f'[Competition Announcement] {competition.name} is announced'
    body = f"""<html>
    <body>
        <p>Dear {subscriber.name},</p>
        <p>{competition.name} has just been announced on the WCA Website, and will take place in {competition.city} on {competition.format_dates()}.</p>
        <p>Registration for this competition is open from {competition.registration_open_with_timezone('Europe/Oslo').strftime('%H:%M %A, %B %d')} to {competition.registration_close_with_timezone('Europe/Oslo').strftime('%H:%M %A, %B %d')}.</p>
        <p>You can register for this competition <a href="https://worldcubeassociation.org/competitions/{competition.id}">here</a>.</p>
        <p>Best regards,<br>{competition.delegates}</p>
    </body>
</html>"""

    # Load email and password from .env
    load_dotenv()
    email = str(os.getenv("EMAIL"))
    password = str(os.getenv("EMAIL_PASSWORD"))

    em = EmailMessage()
    em['From'] = email
    em['To'] = subscriber.email
    em['Subject'] = subject
    em.set_content(body, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email, password)
        smtp.sendmail(email, subscriber.email, em.as_string())
