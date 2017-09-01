#!/usr/bin/env python
# -*- coding: utf-8 -*-

from smtplib import SMTP as Client

client = Client('localhost', 2525)
r = client.sendmail('czocher@example.com', ['czocher@example.com'], """\
 From: Anne Person <anne@example.com>
 To: Bart Person <bart@example.com>
 Subject: A test
 Message-ID: <ant>
 Hi Bart, this is Anne.
 """)
