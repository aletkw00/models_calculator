
from smtplib import SMTP, SMTP_SSL
from email.message import EmailMessage
from file_system import read_a_file_byte


"""
# ONLY FOR TEST
import os
import smtp_server

def read_a_file_byte(path, name_file):
    with open(file=os.path.join(path, name_file), mode='rb') as f:
        data = f.read()        
        return data
    
# ONLY FOR TEST
"""

class email_Sender():

    def __init__(self) -> None:
        self.hostname = 'mail.email.ma'
        self.port = 465
        self.sender = 'mail@email.ma'
        self.password = 'password'
        self.charset = 'utf-8'
        self.contentPlain = 'text/plain'
        self.contentHtml = 'text/html'


    def create_message(self, dest: str, subj: str, body: str, isHTML: bool):
        # FOR CREATE A MESSAGE
        # https://docs.python.org/3/library/email.message.html
        # https://stackoverflow.com/questions/77330887/problem-sending-utf-8-display-name-in-gmail-api
        # 
        # ANOTHER SOLUTION WITH MIMETEXT (PROBLEMS WITH UTF-8)
        # https://stackoverflow.com/questions/38825943/mimemultipart-mimetext-mimebase-and-payloads-for-sending-email-with-file-atta
        # https://stackoverflow.com/questions/8171856/mimetext-utf-8-encode-problems-when-sending-email
        #

        self.msg = EmailMessage()
        self.msg.set_charset(self.charset)
        self.msg.add_header("From", self.sender)
        self.msg.add_header("To", dest)
        self.recipient = dest
        self.msg.add_header("Subject", subj)
        self.msg.set_payload(body)
        if isHTML:
            self.msg.set_type(self.contentHtml)
        else:
            self.msg.set_type(self.contentPlain)        


    def add_attachment(self, path, name_file):
        # https://stackoverflow.com/questions/44528466/attaching-pdf-file-to-an-emailmessage
        #
        # send all data as a general octet-stream, encoded with base64 as usual for an attachment
        #
        self.msg.add_attachment(read_a_file_byte(path, name_file), maintype='application', subtype='octet-stream', filename=name_file)

        
    def send_email(self):
        # https://stackabuse.com/how-to-send-emails-with-gmail-using-python/
        #
        client = SMTP_SSL(self.hostname, self.port)
        #client.set_debuglevel(True) # show communication with the server
        client.login(self.sender, self.password)
        try:
            client.sendmail(self.sender, self.recipient, self.msg.as_string().encode("utf-8"))
        finally:
            client.quit()


"""
# ONLY FOR TEST

if __name__ == '__main__':
    server = smtp_server.SMTP_Server()
    server.start()
    #input('invio')
    message = email_Sender()
    message.create_message(dest='prova@prova.p',
                           subj='Test email',
                           body='This is a è test.',
                           isHTML=True)
    message.add_attachment(os.getcwd(),'requirements.txt')
    message.send_email()
    server.stop()
# ONLY FOR TEST
"""