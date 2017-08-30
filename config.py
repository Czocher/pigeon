#!/usr/bin/env python3

from os import path

# The domain which Pigeon should support
DOMAIN = 'example.com'

# A list of users of this MTA
# Pigeon will accept messages sent only to one of those addresses
# and use only the selected keyfiles/fingerprints to do the encryption
USERS = {
    'exampleuser': {
        'to': 'otheremail@example.com',
        'fingerprint': 'DEADBEEF0987'
    },
}

# The GPG home directory used by Pigeon
# defaults to the gpghome subdirectory in the Pigeon project directory
GPGHOME = path.join(path.abspath(path.dirname(__file__)), 'gpghome')
