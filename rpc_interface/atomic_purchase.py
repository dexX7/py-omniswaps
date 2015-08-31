#!/usr/bin/env
import sys

def help():
    print("atomic_purchase address rawtx\n")
    print("Prepares a signed transaction for the payment of an atomic swap.")
    exit()

def main():
    if len(sys.argv) != 3:
        help()
    print("Done!")

if __name__ == "__main__":
    main()
