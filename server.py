#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

import email.mime.application
import email.mime.multipart
import email.mime.text
import email.encoders

import gnupg

keyid="czochanski@gmail.com"

def pgp_mime(message, recepients):
    encrypted_content = gpg.encrypt(message.as_string(), recepients)

    enc = email.mime.application.MIMEApplication(
            _data=str(encrypted_content),
            _subtype='octet-stream; name="encrypted.asc"',
            _encoder=email.encoders.encode_7or8bit)
    enc['Content-Description'] = 'OpenPGP encrypted message'
    enc.set_charset('us-ascii')

    control = email.mime.application.MIMEApplication(
            _data='Version: 1\n',
            _subtype='pgp-encrypted',
            _encoder=email.encoders.encode_7or8bit)
    control.set_charset('us-ascii')

    encmsg = email.mime.multipart.MIMEMultipart(
            'encrypted',
            protocol='application/pgp-encrypted')
    encmsg.attach(control)
    encmsg.attach(enc)
    encmsg['Content-Disposition'] = 'inline'

    return encmsg

gpg = gnupg.GPG()



class ExampleHandler:
    async def handle_RCPT(self, server, session, envelope, address, rcpt_options):
        if not address.endswith('@example.com'):
            return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        message = email.mime.text.MIMEText(_text=envelope.content.decode('utf-8', errors='replace'))
        encrypted_message = pgp_mime(message, keyid)
        #print(encrypted_message)

        #print('Message from %s' % envelope.mail_from)
        #print('Message for %s' % envelope.rcpt_tos)
        #print('Message data:\n')
        #print(envelope.content.decode('utf8', errors='replace'))
        #print('End of message')
        return '250 Message accepted for delivery'

def main():
    from aiosmtpd.controller import Controller
    import asyncio
    controller = Controller(ExampleHandler(), hostname='localhost', port=8025)
    controller.start()
    print(controller.hostname)
    print(controller.port)
    loop = asyncio.get_event_loop()
    loop.run_forever()

if __name__ == "__main__":
    main()
