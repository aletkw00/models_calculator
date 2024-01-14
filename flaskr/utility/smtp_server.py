from aiosmtpd.controller import Controller

# ONLY FOR TESTS


class Custom_Handler():
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        if not address.endswith('@example.com'):
            return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        return '250 OK'


    async def handle_DATA(self, server, session, envelope):
        print('Message from %s' % envelope.mail_from)
        print('Message for %s' % envelope.rcpt_tos)
        print('Message data:\n')
        for ln in envelope.content.decode('utf8', errors='replace').splitlines():
            print(f'> {ln}'.strip())
        print()
        print('End of message')
        return '250 Message accepted for delivery'


class SMTP_Server:
    def __init__(self) -> None:
        self.hostname = 'localhost'
        self.port = 8025


    def start(self):
        self.smtp = Controller(Custom_Handler(), hostname=self.hostname, port=self.port)
        self.smtp.start()


    def stop(self):
        self.smtp.stop()

