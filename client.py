#!/usr/bin/env python
# -*- coding: utf-8 -*-

from smtplib import SMTP as Client

client = Client('localhost', 8025)
r = client.sendmail('a@example.com', ['b@example.com'], """\
 From: Anne Person <anne@example.com>
 To: Bart Person <bart@example.com>
 Subject: A test
 Message-ID: <ant>
 łłłł
 Hi Bart, this is Anne.
 """)
