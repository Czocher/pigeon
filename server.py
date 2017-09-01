#!/usr/bin/env python3

from aiosmtpd.controller import Controller

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.encoders import encode_7or8bit

import asyncio
import sys
import gnupg
import config


gpg = gnupg.GPG(homedir=config.GPGHOME, verbose=True)


def pgp_mime(message, recipients):
    content = gpg.encrypt(message.as_string(), *recipients)
    encrypted = MIMEApplication(
            _data=str(content),
            _subtype='octet-stream; name="encrypted.asc"',
            _encoder=encode_7or8bit)
    encrypted['Content-Description'] = 'OpenPGP encrypted message'
    encrypted.set_charset('us-ascii')

    control = MIMEApplication(
            _data='Version: 1\n',
            _subtype='pgp-encrypted',
            _encoder=encode_7or8bit)
    control.set_charset('us-ascii')

    encmsg = MIMEMultipart('encrypted', protocol='application/pgp-encrypted')
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
        message = MIMEText(
                _text=envelope.content.decode('utf-8', errors='replace'))
        recipients = envelope.rcpt_tos

        if not self._valid_recipients(recipients):
            return '550 Unknown recipients'

        try:
            fingerprints = self._get_fingerprints(recipients)
        except:
            return '550 PGP key fingerprint not configured'

        encrypted_message = pgp_mime(message, fingerprints)
        print(encrypted_message.as_string())
        # TODO send
        return '250 Message accepted for delivery'

    def _valid_recipients(self, recipients):
        func = lambda r: r.split('@')[0] in config.USERS.keys()
        return all(map(func, recipients))

    def _get_fingerprints(self, recipients):
        func = lambda r: config.USERS[r.split('@')[0]]['fingerprint']
        return list(map(func, recipients))

def main():
    address, port = sys.argv[1:3]
    controller = Controller(PigeonHandler(), hostname=address, port=port)
    controller.start()
    loop = asyncio.get_event_loop()
    loop.run_forever()

if __name__ == "__main__":
    main()
