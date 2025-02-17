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
import json

def main():
    """Parse command-line arguments and print the received parameters."""
    if len(sys.argv) < 5:
        print("Error: Missing required parameters.")
        print("Usage: urgentshake.sh <magnitude> <longitude> <latitude> <depth> [strike] [dip] [rake]")
        sys.exit(1)

    # Parse required parameters
    try:
        magnitude = float(sys.argv[1])
        longitude = float(sys.argv[2])
        latitude = float(sys.argv[3])
        depth = float(sys.argv[4])
    except ValueError:
        print("Error: Invalid number format in required parameters.")
        sys.exit(1)

    # Parse optional parameters
    strike = float(sys.argv[5]) if len(sys.argv) > 5 else None
    dip = float(sys.argv[6]) if len(sys.argv) > 6 else None
    rake = float(sys.argv[7]) if len(sys.argv) > 7 else None

    # Print received parameters
    print("\nUrgentShake Script Received Parameters:")
    print(f"  Magnitude:  {magnitude}")
    print(f"  Longitude:  {longitude}")
    print(f"  Latitude:   {latitude}")
    print(f"  Depth:      {depth} km")
    if strike is not None:
        print(f"  Strike:     {strike}°")
    if dip is not None:
        print(f"  Dip:        {dip}°")
    if rake is not None:
        print(f"  Rake:       {rake}°")

    # Return True to indicate success
    print("\nResult: True")
    sys.exit(0)


if __name__ == "__main__":
    main()
