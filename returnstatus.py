#!/usr/bin/env python3

# ****************************************************************************
#
# Copyright (C) 2019-2025, ShakeLab Developers.
# This file is part of ShakeLab.
#
# ShakeLab is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# ShakeLab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# with this download. If not, see <http://www.gnu.org/licenses/>
#
# ****************************************************************************

"""
"""

import socket
import argparse
import sys

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5001


def send_completion_notification(host, port, job_id):
    """Send a completion signal to ShakeServer for a given job ID."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((host, port))
            command = f"complete {job_id}"
            client.sendall(command.encode())

            response = client.recv(1024).decode()
            print(f"Server response: {response}")

    except ConnectionRefusedError:
        print(f"Error: Could not connect to {host}:{port}. Ensure ShakeServer is running.")
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


def main():
    """Parse command-line arguments and send job completion notification."""
    parser = argparse.ArgumentParser(
        description="Notify ShakeServer of job completion."
    )
    parser.add_argument(
        "--host", type=str, default=DEFAULT_HOST,
        help=f"ShakeServer hostname or IP (default: {DEFAULT_HOST})"
    )
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT,
        help=f"ShakeServer port number (default: {DEFAULT_PORT})"
    )
    parser.add_argument(
        "job_id", type=int, help="Job ID to mark as completed"
    )

    args = parser.parse_args()

    send_completion_notification(args.host, args.port, args.job_id)


if __name__ == "__main__":
    main()
