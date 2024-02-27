import smtplib


class SendEmailManager(object):
    def __init__(self, host: str, port: int) -> None :

        self.mail = smtplib.SMTP(host, port)
        
    def __enter__(self):
        self.mail.ehlo()
        self.mail.starttls()
        return self.mail
    def __exit__(self, type, value, traceback):
        self.mail.close()
        return True

class StorageLocalFile(object):
    def __init__(self, filename: str) -> None:
        filename = "media/" + filename
        self.file_obj = open(filename, 'w+b')

    def __enter__(self):
        return self.file_obj
    def __exit__(self, type, value, traceback):
        self.file_obj.close()
        return True