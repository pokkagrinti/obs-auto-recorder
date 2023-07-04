import obsws_python as obs
import time
import math
import requests
import json
import tomllib
import sys
from datetime import datetime   

THRESHOLD = 1000
SECONDS_TO_RECORD = 300
XP_POLLING_RATE_IN_SECONDS = 10

def load_toml(toml_filename="config.toml"):
    """Loads config.toml"""

    with open(toml_filename, 'rb') as f:
        data = tomllib.load(f)

    return data


def get_experience_for_level(level):
    """Calculates XP required for each level in OSRS"""
    points = 0
    output = 0

    for lvl in range(1, level + 1):
        points += math.floor(lvl + 300.0 * math.pow(2.0, lvl / 7.0))

        if lvl >= level:
            return output
        output = int(math.floor(points / 4))

    return 0


def get_stats_info():
    """Retrieves player stats using Morg HTTP Client plugin in Runelite"""
    data = {}
    try:
        # Get stats from HTTP Client
        response = requests.get('http://localhost:8081/stats')
        
        # check if request was successful
        if response.status_code == 200:
            # load the JSON data into Python object
            data = json.loads(response.text)
            
            # Drop first username, email dictionary
            data = data[1:]

    except requests.exceptions.RequestException as e:
        sys.exit(f"Error: {str(e)}\n Unable to retrieve player info. Ensure that player is logged in.")

    return data


def get_skills_and_xp():
    """Gets the skills to be tracked and its Level & XP value then return it as a dictionary"""

    # Gets skill config to see which skill is to be tracked
    skill_dict = load_toml()["skill"]
    skill_to_track = []

    for key, value in skill_dict.items():
        if value == 1:
            skill_to_track.append(key)

    # Get all tracked skills and the current Level & XP value
    tracked_skills_dict = {}

    for dictionary in get_stats_info():
        skill_name = dictionary["stat"]
        level_xp_value = {"level": dictionary["level"], "xp": dictionary["xp"]}

        # Store them in a dictionary
        if skill_name in skill_to_track:
            tracked_skills_dict[skill_name] = level_xp_value

    return tracked_skills_dict


def check_record(threshold=1000):
    """Checks if any of the tracked skills is within the XP threshold to start recording"""

    # Get XP of skills
    tracked_skills_dict = get_skills_and_xp()
    print(tracked_skills_dict, end="\n\n")

    # Generate XP required for each level
    xp_chart = {}
    for i in range(1, 100):
        xp_chart[i] = get_experience_for_level(i)

    # Check if XP is within threshold to start recording
    for skill_info_dict in tracked_skills_dict.values():
        level = skill_info_dict["level"]
        xp = skill_info_dict["xp"]

        # Get XP required for next level
        xp_left_to_level = xp_chart[level+1] - xp
        # Check if it is under the specified threshold
        if xp_left_to_level < threshold:
            return True
        
    return False


def get_formatted_time():
    """Returns current time in a specified format"""

    now = datetime.now()
    formatted_now = now.strftime('[%d/%m/%Y %H:%M:%S]')

    return formatted_now


def main():
    # Connect to OBS web socket
    try:
        client = obs.ReqClient()
    except:
        sys.exit("Please ensure that OBS is running before running this script")

    while True:
        # Output polls
        now = get_formatted_time()
        print(now, "Polling XP... ")

        start_recording = check_record(THRESHOLD)

        # Starts recording when XP is near
        if start_recording:
            now = get_formatted_time()
            print(now, "Started Recording.")
            client.start_record()
            
            time.sleep(SECONDS_TO_RECORD)
            
            client.stop_record()
            now = get_formatted_time()
            print(now, "Recording Ended.")

        time.sleep(XP_POLLING_RATE_IN_SECONDS)


if __name__ == "__main__":
    main()


