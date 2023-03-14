# Control NordVPN from your Terminal on MacOS (with Tunnelblick!)

This is a simple script in Python to handle connection/disconnection to a VPN configuration via Tunnelblick. The idea
came from the lack of an option, on MacOS, to handle NordVPN via command line, possible in Linux with the official
NordVPN client. Moreover, although having been tested using a Nord configuration, in theory it should work with any
other VPN configuration managed by Tunnelblick.

## Installation

1. First, refer
   to [this](https://support.nordvpn.com/Connectivity/macOS/1061815912/Manual-connection-setup-with-Tunnelblick-on-macOS.htm)
   guide to set up Tunnelblick with NordVPN.
2. Clone this repository and install the `request` library with `pip install requests==2.28.1`.
3. Now, you can run the script with `python3 nordvpn-term.py` and refer to #Usage for more information.

4. Optionally, to make the script available from anywhere, you can move the script to `/usr/local/bin` and add the
   following line to your `.bashrc` or `.zshrc` file:

```bash
alias nordvpn="python3 /path/to/nordvpn-term.py"
```

## Usage

The script take one positional argument referring to the command to perform. The available commands are:

- `connect`: connect to a VPN configuration. This command takes an optional arguments:
    - `--server`: the URL of the server to connect to. If not specified, the script will use the last configuration
      used on Tunnelblick.
- `disconnect`: disconnect from the current VPN configuration.
- `status`: print the status of the current VPN configuration.
- `configs`: print all available configurations that has been imported to Tunnelblick.


