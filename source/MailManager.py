# This project created by urhoba
# www.urhoba.net

from Settings import MailSettings
#from LogManager import LogManager

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import ColoredPrint

class MailManager:
#region Init    
    def __init__(self) -> None:
        self.fromMail = MailSettings.fromMail
        self.fromPassword = MailSettings.fromPassword
        self.smtpHost = MailSettings.smtpHost
        self.smtpPort = MailSettings.smtpPort
        #self.logManager = LogManager("MailManager")
#endregion

#region Send Mail
    def SendMail(self, subject, content, toMail):
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.fromMail
            message["To"] = toMail

            _content = MIMEText(content.encode('utf-8'), _charset='utf-8')
            message.attach(_content)

            with smtplib.SMTP_SSL(self.smtpHost, self.smtpPort) as server:
                server.login(self.fromMail, self.fromPassword)
                server.sendmail(self.fromMail, toMail, message.as_string())
            ColoredPrint.GreenPrint("Mail gönderildi!")
        except Exception as e:
            # self.logManager.AddLog(f"Mail gönderilemedi!\nHata Kodu: {e}\nMail başlığı : {subject} \nMail içeriği : {content} \nAlıcı : {toMail}")
            ColoredPrint.RedPrint(f"Mail gönderilemedi!\nHata Kodu: {e}\nMail başlığı : {subject} \nMail içeriği : {content} \nAlıcı : {toMail}")

#endregion