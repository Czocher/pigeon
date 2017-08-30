#!/usr/bin/env python3

import gnupg
import argparse
import config
import sys


GPG = gnupg.GPG(homedir=config.GPGHOME)


def list_missing_keys():
    missing_keys = []
    available_keys = map(lambda k: k['fingerprint'], GPG.list_keys())
    for user, cfg in config.USERS.items():
        if cfg['fingerprint'] not in available_keys:
            missing_keys.append((user, cfg['fingerprint']))
    return missing_keys


def check_cmd():
    for user, fingerprint in list_missing_keys():
        print('No key available for user {} (fingerprint: {}).'
              .format(user, fingerprint), file=sys.stderr)


def import_key_cmd(path):
    with open(path, 'r') as keyfile:
        GPG.import_keys(keyfile.read())


def clean_cmd():
    available_keys = set(map(lambda k: k['fingerprint'], GPG.list_keys()))
    required_keys = set(map(lambda k: k['fingerprint'], config.USERS.values()))
    for fingerprint in available_keys - required_keys:
        print('Deleting key: {}.'.format(fingerprint), file=sys.stderr)
        GPG.delete_keys(fingerprint)
    print('Key database clean.', file=sys.stderr)

def run_cmd():
    pass  # TODO run pigeon


def main():
    parser = argparse.ArgumentParser(prog='pigeon')
    subparsers = parser.add_subparsers()

    # TODO add proper help messages
    run_parser = subparsers.add_parser('run', help='run help')
    run_parser.set_defaults(command='run')

    check_parser = subparsers.add_parser('check', help='check help')
    check_parser.set_defaults(command='check')

    import_key_parser = subparsers.add_parser('importkey', help='import help')
    import_key_parser.add_argument('path',
                                   help='path to the keyfile to import')
    import_key_parser.set_defaults(command='importkey')

    clean_parser = subparsers.add_parser('clean', help='clean help')
    clean_parser.set_defaults(command='clean')

    args = parser.parse_args()

    if args.command == 'check':
        check_cmd()
    elif args.command == 'importkey':
        import_key_cmd(args.path)
    elif args.command == 'clean':
        clean_cmd()
    elif args.command == 'run':
        if list_missing_keys():
            print('Some keys seem to be missing, run the \'check\' command.',
                  file=sys.stderr)
        run_cmd()

if __name__ == "__main__":
    main()
