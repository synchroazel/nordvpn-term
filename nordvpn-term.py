import argparse
import subprocess
import time

import requests

UNDERLINE = "\u001b[4m"
BOLD = "\u001b[1m"
NS = "\u001b[0m"
RED = '\033[0;31m'
GREEN = '\033[0;32m'
BLUE = '\033[0;34m'
NC = '\033[0m'


def main():
    parser = argparse.ArgumentParser(add_help=False,
                                     description="A script to connect to a VPN using Tunnelblick and your terminal.",
                                     formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30))

    parser.add_argument("action", choices=["help", "connect", "disconnect", "status", "configs"],
                        help="The command to execute.")

    parser.add_argument("-s", "--server", required=False,
                        help="The URL of the server to connect to.")

    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='Show this help message and exit.')

    args = parser.parse_args()

    command = args.action
    server = args.server

    if command == "connect":
        if get_status() == "CONNECTED":
            print(f"{RED}You are already connected to a VPN{NC}")
            exit(0)

        if server is None:
            server = get_configurations()[-1]

        country_code = ''.join([c for c in server.split(".")[0] if c.isalpha()])
        server_number = ''.join([c for c in server.split(".")[0] if c.isdigit()])

        print(f"Connecting to {BLUE}{country_code.upper()}#{server_number}{NC}...")

        old_ip = get_public_ip()

        out = connect(server)

        if out:
            wait_ip_change()
            print(f"{GREEN}Connected successfully to {UNDERLINE}{server}{NS}{GREEN}, your IP is {get_public_ip()}{NC}")
        else:
            print(f"{RED}Connection failed{NC}")

    if command == "disconnect":

        if get_status() == "EXITING":
            print(f"{RED}You are not connected to any VPN{NC}")
            exit(0)

        out = disconnect()

        if out:
            wait_ip_change()
            print(f"{GREEN}Disconnected successfully.{NC}")
        else:
            print(f"{RED}Disconnection failed.{NC}")

    if command == "status":
        status = get_status()

        if status == "EXITING":
            print(f"{RED}You are not connected to any VPN, your IP is {BOLD}{get_public_ip()}{NC}{NS}")
        elif status == "CONNECTED":
            print(f"{GREEN}You are connected to a VPN, with IP {BOLD}{get_public_ip()}{NC}{NS}")
        elif status == "DISCONNECTING":
            print(f"{RED}You are being disconnected, please retry in a moment.{NC}")
        else:
            print(f"Your current status is {status} | not been implemented yet")

    if command == "configs":
        confs = get_configurations()
        print(f"{BLUE}Available configurations:{BLUE}")
        for i, conf in enumerate(confs):
            if i + 1 == len(confs):
                print(f"\t{BLUE}{BOLD}>{NS} {UNDERLINE}{conf}{NS}{BLUE}")
            else:
                print(f"\t{BLUE}{BOLD}>{NS} {conf}{BLUE}")


def connect(server):
    out = subprocess.check_output(
        ["osascript",
         "-e", "tell application \"/Applications/Tunnelblick.app\"",
         "-e", f"connect \"{server}\"",
         "-e", "end tell"]
    )

    return out.strip().decode("utf-8")


def disconnect():
    out = subprocess.check_output(
        ["osascript",
         "-e", "tell application \"/Applications/Tunnelblick.app\"",
         "-e", "disconnect all",
         "-e", "end tell"]
    )

    return out.strip().decode("utf-8")


def get_status():
    out = subprocess.check_output(
        ["osascript",
         "-e", "tell application \"/Applications/Tunnelblick.app\"",
         "-e", "get state of first configuration",
         "-e", "end tell"]
    )

    return out.strip().decode("utf-8")


def get_configurations():
    out = subprocess.check_output(
        ["osascript",
         "-e", "tell application \"/Applications/Tunnelblick.app\"",
         "-e", "get name of configurations",
         "-e", "end tell"]
    )

    return out.strip().decode("utf-8").split(", ")


def get_public_ip():
    try:
        raw = requests.get('https://api.duckduckgo.com/?q=ip&format=json')
        answer = raw.json()["Answer"].split()[4]
    except Exception as e:
        return 'Error: {0}'.format(e)
    else:
        return answer


def wait_ip_change():
    old_ip = get_public_ip()
    while old_ip == get_public_ip():
        time.sleep(1)


if __name__ == '__main__':
    main()
