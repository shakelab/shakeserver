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
DUMMY CODE
"""

import sys
import subprocess

def main():
    """Extract job parameters and execute the simulation."""
    if len(sys.argv) < 5:
        print("Error: Missing required parameters.")
        print("Usage: urgentshake.sh <job_id> <magnitude> <longitude> <latitude> <depth> [strike] [dip] [rake]")
        sys.exit(1)

    job_id = sys.argv[1]  # Extract the job ID
    magnitude = sys.argv[2]
    longitude = sys.argv[3]
    latitude = sys.argv[4]
    depth = sys.argv[5]

    # Optional parameters
    strike = sys.argv[6] if len(sys.argv) > 6 else None
    dip = sys.argv[7] if len(sys.argv) > 7 else None
    rake = sys.argv[8] if len(sys.argv) > 8 else None

    # Simulate the execution (replace with actual computation)
    print(f"Running seismic simulation for job {job_id}...")
    print(f"  Magnitude: {magnitude}, Location: ({longitude}, {latitude}), Depth: {depth} km")
    if strike: print(f"  Strike: {strike}°")
    if dip: print(f"  Dip: {dip}°")
    if rake: print(f"  Rake: {rake}°")

    # Simulate a long computation (to be replaced with real execution)
    subprocess.run(["sleep", "10"])  # Replace with actual computation command

    # Call returnstatus.py to notify completion
    subprocess.run(["python3", "returnstatus.py", "--host", "127.0.0.1", "--port", "5001", job_id])

    print(f"Job {job_id} completed and notified.")

if __name__ == "__main__":
    main()
