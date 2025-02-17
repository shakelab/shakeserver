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
import json
import sys

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 5001


def send_command(host, port, command):
    """Send a command to the server and return the response."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        client.sendall(command.encode())
        response = client.recv(4096).decode()
    return response


def format_scenario_output(response, params):
    """Format the output of a scenario run in a readable way."""
    print("\nScenario started successfully:\n")
    print("Parameters:")
    print(f"  Magnitude:  {params['magnitude']}")
    print(f"  Longitude:  {params['longitude']}")
    print(f"  Latitude:   {params['latitude']}")
    print(f"  Depth:      {params['depth']} km")

    if params["strike"] is not None:
        print(f"  Strike:     {params['strike']}°")
    if params["dip"] is not None:
        print(f"  Dip:        {params['dip']}°")
    if params["rake"] is not None:
        print(f"  Rake:       {params['rake']}°")

    print("\nServer Response:")
    print(f"  Scenario ID: {response.strip()}")


def format_info_output(response):
    """Format the output of a scenario info request in a readable way."""
    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        print("Error: Invalid response from server.")
        return

    print("\nScenario Details:")
    print("=" * 40)
    print(f"  ID:         {data['id']}")
    print(f"  Timestamp:  {data['timestamp']}")
    print("-" * 40)
    print(f"  Magnitude:  {data['params']['magnitude']}")
    print(f"  Longitude:  {data['params']['longitude']}")
    print(f"  Latitude:   {data['params']['latitude']}")
    print(f"  Depth:      {data['params']['depth']} km")

    if data["params"].get("strike") is not None:
        print(f"  Strike:     {data['params']['strike']}°")
    if data["params"].get("dip") is not None:
        print(f"  Dip:        {data['params']['dip']}°")
    if data["params"].get("rake") is not None:
        print(f"  Rake:       {data['params']['rake']}°")

    print("=" * 40)


def format_list_output(response):
    """Format the output of the list command in a readable way."""
    if "No jobs recorded" in response:
        print("\nNo scenarios found.\n")
        return

    print("\nStored Scenarios:")
    print("=" * 40)

    for line in response.split("\n"):
        if line.strip():
            parts = line.split(" - ")
            print(f"  {parts[0]}  |  {parts[1]}  |  Magnitude: {parts[2]}")

    print("=" * 40)


def main():
    """Parse command-line arguments and send the corresponding command."""
    parser = argparse.ArgumentParser(
        description="Client for ShakeServer"
    )
    parser.add_argument(
        "--host", type=str, default=DEFAULT_HOST,
        help=f"Server hostname or IP (default: {DEFAULT_HOST})"
    )
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT,
        help=f"Server port number (default: {DEFAULT_PORT})"
    )

    subparsers = parser.add_subparsers(dest="command")

    # run <magnitude> <longitude> <latitude> <depth> [options]
    run_parser = subparsers.add_parser(
        "run", help="Run a new shake scenario"
    )
    run_parser.add_argument("magnitude", type=float, help="Magnitude")
    run_parser.add_argument("longitude", type=float, help="Longitude")
    run_parser.add_argument("latitude", type=float, help="Latitude")
    run_parser.add_argument("depth", type=float, help="Depth (km)")
    run_parser.add_argument("--strike", type=float, help="Strike", default=None)
    run_parser.add_argument("--dip", type=float, help="Dip", default=None)
    run_parser.add_argument("--rake", type=float, help="Rake", default=None)

    # list
    subparsers.add_parser("list", help="List all scenarios")

    # info <id>
    info_parser = subparsers.add_parser("info", help="Get details of a specific scenario")
    info_parser.add_argument("id", type=int, help="Scenario ID")

    # delete <id>
    delete_parser = subparsers.add_parser("delete", help="Delete a scenario")
    delete_parser.add_argument("id", type=int, help="Scenario ID")

    # reset
    subparsers.add_parser("reset", help="Reset the database")

    # Se il client viene eseguito senza argomenti validi, mostra l'help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    host = args.host
    port = args.port

    if args.command == "run":
        params = {
            "magnitude": args.magnitude,
            "longitude": args.longitude,
            "latitude": args.latitude,
            "depth": args.depth,
            "strike": args.strike,
            "dip": args.dip,
            "rake": args.rake,
        }
        response = send_command(host, port, f"run {json.dumps(params)}")
        format_scenario_output(response, params)

    elif args.command == "list":
        response = send_command(host, port, "list")
        format_list_output(response)

    elif args.command == "info":
        response = send_command(host, port, f"info {args.id}")
        format_info_output(response)

    elif args.command == "delete":
        response = send_command(host, port, f"delete {args.id}")
        print(response)

    elif args.command == "reset":
        response = send_command(host, port, "reset")
        print(response)

    else:
        print("Error: Invalid command.\n")
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
