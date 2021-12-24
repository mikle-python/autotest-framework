import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os


class EmailObj(object):
    _smtp = None

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    @property
    def smtp(self):
        if self._smtp is None:
            self._smtp = smtplib.SMTP(self.host, port=self.port)
            self._smtp.login(self.username, self.password)

        return self._smtp

    def send(self, sender, receivers, title, send_files=[]):
        try:
            message = MIMEMultipart()
            message['From'] = sender
            message['To'] = ','.join(receivers) if isinstance(receivers, list) else receivers
            message['Subject'] = Header(title, 'utf-8')

            for send_file in send_files:
                with open(send_file, 'rb') as f:
                    mail_body = f.read()

                if os.path.splitext(send_file)[-1] == '.html':
                    message.attach(MIMEText(mail_body, 'html', 'utf-8'))

                att = MIMEText(mail_body, 'base64', 'utf-8')
                att["Content-Type"] = 'application/octet-stream'
                att["Content-Disposition"] = 'attachment; filename="{name}"'.format(name=os.path.basename(send_file))
                message.attach(att)

            if not isinstance(receivers, list):
                receivers = receivers.split(",")
            self.smtp.sendmail(sender, receivers, message.as_string())
        except Exception as e:
            raise e
        finally:
            self.smtp.quit()


if __name__ == '__main__':
    from configparser import ConfigParser
    config_obj = ConfigParser()
    config_obj.read(os.path.join(os.getcwd().split('ghostcloudtest')[0], 'ghostcloudtest/config/config.ini'))

    sender = config_obj.get('email', 'sender')
    receivers = config_obj.get('email', 'receivers').split(',')
    smtp_server = config_obj.get('email', 'smtp_server')
    username = config_obj.get('email', 'username')
    password = config_obj.get('email', 'password')
    smtp_port = int(config_obj.get('email', 'smtp_port'))

    title = 'Inferface Test'
    send_file = ['C:/Project/Python/ghostcloudtest/log/interface/192_168_7_148/api-2021-10-20-11-35-33/2021-10-20-11-35-33.html']

    email_obj = EmailObj(smtp_server, smtp_port, username, password)
    email_obj.send(sender, receivers, title, send_file)