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

import os
import json
import subprocess
import socket
import threading
import time
import argparse

DEFAULT_HOST = "0.0.0.0"
DEFAULT_PORT = 5001
HISTORY_FILE = "shake_history.json"


def load_history():
    """Load job history from file."""
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)


def save_history(history):
    """Save job history to file."""
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def run_scenario(params):
    """Run a shake scenario and record it in the database."""
    history = load_history()
    job_id = len(history) + 1
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    try:
        cmd = ["./urgentshake.py",
               str(params["magnitude"]),
               str(params["longitude"]),
               str(params["latitude"]),
               str(params["depth"])]
        if params["strike"] is not None:
            cmd.append(str(params["strike"]))
        if params["dip"] is not None:
            cmd.append(str(params["dip"]))
        if params["rake"] is not None:
            cmd.append(str(params["rake"]))

        subprocess.Popen(cmd)
    except FileNotFoundError:
        return "Error: urgentshake.py not found or not executable."

    entry = {"id": job_id, "timestamp": timestamp, "params": params}
    history.append(entry)
    save_history(history)

    return str(job_id)  # Return only the job ID


def list_scenarios():
    """List all recorded shake scenarios."""
    history = load_history()
    if not history:
        return "No jobs recorded."
    return "\n".join([f"ID {e['id']} - {e['timestamp']} - "
                      f"Magnitude: {e['params']['magnitude']}"
                      for e in history])


def get_scenario_info(job_id):
    """Retrieve details of a specific shake scenario by ID."""
    history = load_history()
    for entry in history:
        if entry["id"] == job_id:
            return json.dumps(entry, indent=2)
    return f"Job ID {job_id} not found."


def delete_scenario(job_id):
    """Delete a specific scenario by ID."""
    history = load_history()
    new_history = [e for e in history if e["id"] != job_id]

    if len(history) == len(new_history):
        return f"Job ID {job_id} not found."

    save_history(new_history)
    return f"Job ID {job_id} deleted."


def reset_history():
    """Delete all recorded shake scenarios."""
    save_history([])
    return "All jobs deleted."


def handle_client(conn):
    """Handle incoming client requests."""
    data = conn.recv(1024).decode().strip()
    response = "Unknown command."

    if data.startswith("run"):
        _, params_str = data.split(" ", 1)
        try:
            params = json.loads(params_str)  # Use JSON for safe conversion
            response = run_scenario(params)
        except json.JSONDecodeError:
            response = "Error: Invalid JSON format in request."
    elif data == "list":
        response = list_scenarios()
    elif data.startswith("info"):
        _, job_id = data.split()
        response = get_scenario_info(int(job_id))
    elif data.startswith("delete"):
        _, job_id = data.split()
        response = delete_scenario(int(job_id))
    elif data == "reset":
        response = reset_history()

    conn.sendall(response.encode())
    conn.close()


def start_server(host, port):
    """Start the server and listen for incoming connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}...")

    while True:
        conn, _ = server.accept()
        threading.Thread(target=handle_client, args=(conn,)).start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="ShakeServer: a simple server for running seismic scenarios."
    )
    parser.add_argument(
        "--host", type=str, default=DEFAULT_HOST,
        help=f"Host to bind the server (default: {DEFAULT_HOST})"
    )
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT,
        help=f"Port to bind the server (default: {DEFAULT_PORT})"
    )

    # Se il server viene avviato senza argomenti validi, mostra l'help
    if len(os.sys.argv) == 1:
        parser.print_help()
        os.sys.exit(1)

    args = parser.parse_args()
    start_server(args.host, args.port)
