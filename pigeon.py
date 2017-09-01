#!/usr/bin/env python3

import gnupg
import argparse
import config
import sys
import subprocess


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
        result = GPG.import_keys(keyfile.read())
        print('Imported keys:\n{}'.format(
            '\n'.join(result.fingerprints)))


def clean_cmd():
    available_keys = set(map(lambda k: k['fingerprint'], GPG.list_keys()))
    required_keys = set(map(lambda k: k['fingerprint'], config.USERS.values()))
    for fingerprint in available_keys - required_keys:
        print('Deleting key: {}.'.format(fingerprint), file=sys.stderr)
        GPG.delete_keys(fingerprint)
    print('Key database clean.', file=sys.stderr)


def run_cmd(address, port):
    # Restart the process on failure
    while True:
        p = subprocess.Popen(['python3', './server.py',
            address or '0.0.0.0', port or '2525'],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()


def main():
    parser = argparse.ArgumentParser(prog='pigeon')
    subparsers = parser.add_subparsers()

    run_parser = subparsers.add_parser('run',
            help='run the pigeon smtp server')
    run_parser.add_argument('port', nargs='?',
            help='specify alternative port [default: 2525]')
    run_parser.add_argument('--bind', dest='address',
            help='specify alternative bind address [dafault: all interfaces]')
    run_parser.set_defaults(command='run')

    check_parser = subparsers.add_parser('check',
            help='check the current configuration for mistakes')
    check_parser.set_defaults(command='check')

    import_key_parser = subparsers.add_parser('importkey',
            help='import a given key to the key database')
    import_key_parser.add_argument('path',
                                   help='path to the keyfile to import')
    import_key_parser.set_defaults(command='importkey')

    clean_parser = subparsers.add_parser('clean',
            help='clean the database of unused keys')
    clean_parser.set_defaults(command='clean')

    args = parser.parse_args()

    if not hasattr(args, 'command'):
        parser.print_usage()
        return
    elif args.command == 'check':
        check_cmd()
    elif args.command == 'importkey':
        import_key_cmd(args.path)
    elif args.command == 'clean':
        clean_cmd()
    elif args.command == 'run':
        if list_missing_keys():
            print('Some keys seem to be missing, run the \'check\' command.',
                  file=sys.stderr)
        else:
            run_cmd(args.address, args.port)

if __name__ == "__main__":
    main()
