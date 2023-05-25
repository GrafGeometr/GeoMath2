from random import choice
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


try:
    from email_secret_data import EMAIL, PASSWORD
except ImportError:
    EMAIL = os.environ.get("EMAIL")
    PASSWORD = os.environ.get("PASSWORD")
    print("EMAIL and PASSWORD not set")


def send_email(to, link):

    print([EMAIL])
    print([PASSWORD])

    headers = [
        "Подтверждение электронной почты",
        "Подтверждение электронной почты на сайте ge0math.ru", 
    ]

    texts = [
        "Для подтверждения электронной почты перейдите по ссылке:",
        "Для подтверждения электронной почты на сайте ge0math.ru перейдите по ссылке:",
        "Вы добавили эту почту на сайте ge0math.ru. Чтобы подтвердить электронную почту, перейдите по ссылке:",
        "Вы добавили эту почту на сайте ge0math.ru. Если это не вы, проигнорируйте это письмо. Чтобы подтвердить электронную почту, перейдите по ссылке:",
    ]
    
    text = f"""
    <html>
    <body>
    <h1>{choice(headers)}</h1>
    <p>{choice(texts)}</p>
    <a href="{link}">{link}</a>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = to

    msg['Subject'] = 'Подтверждение электронной почты'
    message = text
    msg.attach(MIMEText(message, 'html'))

    mailserver = smtplib.SMTP('smtp.yandex.ru', 587)
    mailserver.ehlo()
    mailserver.starttls()
    mailserver.ehlo()
    mailserver.login(EMAIL, PASSWORD)
    mailserver.sendmail(EMAIL, to, msg.as_string())
    mailserver.quit()

    