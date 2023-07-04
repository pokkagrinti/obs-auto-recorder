# Runelite Auto OBS

[![Python Version](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![GitHub license](https://img.shields.io/badge/license-GPLv3-blue.svg)](LICENSE)

Runelite Auto OBS is a Python tool designed to integrate with the Runelite client and Open Broadcaster Software (OBS) to automatically record your gameplay when a selected skill is about to level up. This prevents moments where player forgets to record their level up.

## Features

- Integrates with Runelite and OBS.
- Automatically detects when a skill is about to level up.
- Starts recording gameplay for a default period of 5 minutes (configurable).
- Easy to use and customize.

## Prerequisites

Before you begin, ensure you have met the following requirements:

1. Python 3.8 or later
2. OBS
3. Runelite (With plugins installed)
   - Morg HTTP Client

## Installation

1. Clone this repository:
    ```
    git clone https://github.com/pokkagrinti/runelite-auto-obs.git
    ```
2. Install the requirements:
    ```
    pip install -r requirements.txt
    ```

## Usage

To use Runelite Auto OBS, follow these steps:

1. Start the Runelite client and login to your account.
2. Start OBS and configure your scenes. (Note: Manual configuration in OBS is needed to record Runelite screen as this script will not configure OBS.)
3. Edit `config.toml` to select the skill you want to track and set the desired recording time.
    ```toml
    # Example tracking of Attack
    # Change the values of the skills to 1 to start tracking them
    Attack = 1
    ```
4. Run the Runelite Auto OBS script:
    ```
    python runelite_auto_obs.py
    ```

    
## Configuration

You can adjust these global variables to change recording duration, XP threshold, polling rate in the `runelite_auto_obs.py` file:

```python
# Default recording time in seconds
SECONDS_TO_RECORD = 300  # 5 minutes

# Threshold XP to start recording 
THRESHOLD = 1000
SECONDS_TO_RECORD = 300

# Rate of polling the XP of the skill(s)
XP_POLLING_RATE_IN_SECONDS = 10
```


## Contributing
Any contributions are welcome! If you have a feature request, bug report, or improvement to the existing code, please feel free to open an issue or make a pull request.

## License
This project uses the GNU GPLv3 license.