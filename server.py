#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio

import email.mime.application
import email.mime.multipart
import email.mime.text
import email.encoders

import gnupg

import config


gpg = gnupg.GPG(homedir=config.GPGHOME)


def pgp_mime(message, recepients):
    content = gpg.encrypt(message.as_string(), recepients)

    encrypted = email.mime.application.MIMEApplication(
            _data=str(content),
            _subtype='octet-stream; name="encrypted.asc"',
            _encoder=email.encoders.encode_7or8bit)
    encrypted['Content-Description'] = 'OpenPGP encrypted message'
    encrypted.set_charset('us-ascii')

    control = email.mime.application.MIMEApplication(
            _data='Version: 1\n',
            _subtype='pgp-encrypted',
            _encoder=email.encoders.encode_7or8bit)
    control.set_charset('us-ascii')

    encmsg = email.mime.multipart.MIMEMultipart(
            'encrypted',
            protocol='application/pgp-encrypted')
    encmsg.attach(control)
    encmsg.attach(encrypted)
    encmsg['Content-Disposition'] = 'inline'

    return encmsg


class PigeonHandler:

    async def handle_RCPT(self, server, session,
                          envelope, address, rcpt_options):
        if not address.endswith('@' + config.DOMAIN):
            return '550 not relaying to that domain'
        envelope.rcpt_tos.append(address)
        return '250 OK'

    async def handle_DATA(self, server, session, envelope):
        message = email.mime.text.MIMEText(
                _text=envelope.content.decode('utf-8', errors='replace'))
        # TODO can len(rcpt_tos) > 1?
        fingerprints = map(
                lambda a: config.USERS[a.split('@')[0]], envelope.rcpt_tos)
        encrypted_message = pgp_mime(message, fingerprints)
        # TODO send
        return '250 Message accepted for delivery'


def main():
    # TODO handle address and port
    from aiosmtpd.controller import Controller
    import asyncio
    controller = Controller(PigeonHandler(), hostname='localhost', port=8025)
    controller.start()
    loop = asyncio.get_event_loop()
    loop.run_forever()

if __name__ == "__main__":
    main()
