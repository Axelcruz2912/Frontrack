import smtplib
from email.mime.text import MIMEText

def enviar_correo(destino, asunto, mensaje):
    remitente = "jeronimoaxel62@gmail.com"
    password = "owtn twqw qyvv aibi"  

    msg = MIMEText(mensaje, "html")
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destino

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(remitente, password)
    server.sendmail(remitente, destino, msg.as_string())
    server.quit()
