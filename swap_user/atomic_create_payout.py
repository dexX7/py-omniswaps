#!/usr/bin/env python
import sys


def help():
    print("atomic_create_payout txid vout destination amount\n")
    print("Creates script locked 2-of-2 multisig destination.\n")
    print("Arguments:")
    print("1. pubkey    (string, optional) the user's public key\n")
    print("Examples:")
    print("atomic_create_destination")
    print("atomic_create_destination 032c6d9e8c65b62b4f8e8396a7687830590fad2a4bebde5d6be5b7d3d9f0019cc1")
    exit()


def main():
    if len(sys.argv) < 1 or str(sys.argv[1]) == 'help':
        help()


if __name__ == "__main__":
    main()
