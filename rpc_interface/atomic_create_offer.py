#!/usr/bin/env
import sys


def check_balance(from_address, token_id, amount):
    pass


def select_coins(from_address, amount):
    pass


def request_shared():
    pass


def prepare_funding(from_address, to_destination, token_id, amount):
    pass


def prepare_offer():
    pass


def help():
    print("atomic_create_offer address forsale desired\n")
    print("Prepares a signed transaction for an atomic swap.")
    exit()


def main():
    if len(sys.argv) != 4:
        help()
    print("Done!")


if __name__ == "__main__":
    main()
