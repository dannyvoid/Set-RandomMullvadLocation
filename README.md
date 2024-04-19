# Set-RandomMullvadLocation

`Set-RandomMullvadLocation` is a tool to set a random or specific Mullvad VPN server location using either PowerShell or Python scripts. It leverages the Mullvad CLI to list available server locations and set the desired* location.

## Features

- **Random Location**: Set a random Mullvad VPN server location.
- **Specific Location**: Set a Mullvad VPN server location by country shorthand or full country name.
- **List Locations**: Display available Mullvad VPN server locations.

## Requirements

- Mullvad VPN CLI (`mullvad`)

### PowerShell

- PowerShell

### Python

- Python 3.x

## Usage

### PowerShell

```powershell
# List available locations
Set-RandomMullvadLocation -ListLocations

# Set random location
Set-RandomMullvadLocation

# Set specific location
Set-RandomMullvadLocation -Country US
```

### Python

```python
# List available locations
python RandomMullvadLocation.py --list

# Set random location
python RandomMullvadLocation.py

# Set specific location
python RandomMullvadLocation.py --country US
```

## To-Do
- Bring the Powershell version up to parity with the Python copy
  - Allow shorthand or longhand for Country input with Powershell
