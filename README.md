# ShakeServer

ShakeServer is a lightweight client-server application for managing and executing seismic scenario simulations. 
It allows users to launch new simulations, retrieve stored calculations, and manage the scenario database efficiently.

## Features
- Start a new seismic scenario simulation with required and optional parameters.
- Retrieve information about past simulations.
- Manage stored simulations (list, delete, or reset the database).
- Flexible configuration of server host and port.

## Running the Server

The ShakeServer must be running before executing any client commands.

### Start the server with default settings
The server will listen on all network interfaces (0.0.0.0) and port 5001:
```sh
python3 shakeserver.py
```

### Start the server on a specific host and port
To bind the server to a specific IP and port, specify them with --host and --port:
```sh
python3 shakeserver.py --host 127.0.0.1 --port 6000
```

### Display help information
```sh
python3 shakeserver.py --help
```

## Using the Client

The ShakeClient provides an easy way to interact with the server. Below are the available commands.

### Run a new seismic scenario
A seismic scenario requires at least four parameters:
- Magnitude (float) – The magnitude of the earthquake.
- Longitude (float) – The longitude of the epicenter.
- Latitude (float) – The latitude of the epicenter.
- Depth (float) – The depth of the earthquake (in km).

#### Basic example (only required parameters)
```sh
python3 shakeclient.py run 5.2 12.34 -45.67 10
```

#### Run a scenario with optional parameters
Optional parameters:
- Strike (float) – The strike angle (degrees).
- Dip (float) – The dip angle (degrees).
- Rake (float) – The rake angle (degrees).

```sh
python3 shakeclient.py run 5.2 12.34 -45.67 10 --strike 120 --dip 45 --rake 90
```

#### Run a scenario on a specific server
If the server is running on 127.0.0.1:6000, specify it with --host and --port:
```sh
python3 shakeclient.py --host 127.0.0.1 --port 6000 run 5.5 12.34 -45.67 10
```

### Retrieve information for a specific scenario
Each executed scenario is assigned a unique ID. To get details about a specific scenario:

```sh
python3 shakeclient.py info 1
```
Example Output:
```json
{
  "id": 1,
  "timestamp": "2025-02-14 12:34:56",
  "params": {
    "magnitude": 5.5,
    "longitude": 12.34,
    "latitude": -45.67,
    "depth": 10,
    "strike": 120,
    "dip": 45,
    "rake": 90
  }
}
```

### List all stored scenarios
Retrieve a list of all recorded simulations:
```sh
python3 shakeclient.py list
```
Example Output:
```
ID 1 - 2025-02-14 12:34:56 - Magnitude: 5.5
ID 2 - 2025-02-15 08:20:10 - Magnitude: 4.8
```

### Delete a specific scenario
To remove a scenario from the database, provide its ID:
```sh
python3 shakeclient.py delete 1
```
Example Output:
```
Job ID 1 deleted.
```

### Reset the scenario database
This will delete all stored scenarios, resetting the database:
```sh
python3 shakeclient.py reset
```
Example Output:
```
All jobs deleted.
```

### Display help information
```sh
python3 shakeclient.py --help
```

## Configuration
- By default, the server listens on 0.0.0.0:5001.
- The client can specify --host and --port to connect to a different server.
- All scenarios are stored in a JSON file (shake_history.json).

## License
Copyright (c) 2019, ShakeLab Developers

ShakeLab is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

You should have received a copy of the GNU General Public License with this download. If not, see http://www.gnu.org/licenses/

## Disclaimer
ShakeServer is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

The authors of the software assume no liability for use of the software.
