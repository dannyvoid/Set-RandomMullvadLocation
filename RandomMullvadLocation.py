import re
import os
import time
import random
import logging
import argparse
import subprocess

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %I:%M:%S %p",
)


def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(f"Error executing command: {e}")
        return None


def get_mullvad_locations():
    output = run_command(["mullvad", "relay", "list"])
    if not output:
        raise ValueError()

    locations = []
    for line in output.split("\n"):
        match = re.match(r"^([A-Za-z\s]+) \(([a-z]+)\)$", line.strip())
        if match:
            locations.append(
                {"Country": match.group(1).strip(), "Shorthand": match.group(2).lower()}
            )
    return locations


def list_mullvad_locations(locations):
    if locations:
        for location in locations:
            print(f"{location['Country']} ({location['Shorthand']})")
    else:
        print("No locations available.")
        raise ValueError()


def get_location_shorthand(locations, input_country):
    for location in locations:
        if input_country.lower() == location["Shorthand"]:
            return location["Shorthand"]

    for location in locations:
        if input_country.lower() == location["Country"].lower():
            return location["Shorthand"]

    return None


def get_location_longhand(locations, input_country):
    for location in locations:
        if input_country.lower() == location["Shorthand"]:
            return location["Country"]

    for location in locations:
        if input_country.lower() == location["Country"].lower():
            return location["Country"]

    return None


def set_mullvad_location(locations, country):
    shorthand = get_location_shorthand(locations, country)

    if shorthand:
        longhand = get_location_longhand(locations, country)

        logging.info(f"Setting Mullvad location to {longhand}")
        run_command(["mullvad", "relay", "set", "location", shorthand])
    else:
        logging.error("Invalid country provided.")
        raise ValueError()


def set_random_mullvad_location(locations):
    if locations:
        random_location = random.choice(locations)
        logging.info(f"Setting Mullvad location to {random_location['Country']}")
        run_command(
            ["mullvad", "relay", "set", "location", random_location["Shorthand"]]
        )
    else:
        logging.error("No locations available.")


def show_mullvad_status(verbose=False):
    command = ["mullvad", "status"]

    if verbose:
        command.append("-v")

    output = run_command(command)

    if not output:
        raise ValueError()

    print(output)


def main():
    parser = argparse.ArgumentParser(
        description="Set random Mullvad location or list available locations."
    )
    parser.add_argument(
        "--country",
        "-c",
        type=str,
        help="Set Mullvad location by country shorthand or full country name.",
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List available Mullvad locations.",
    )

    args = parser.parse_args()

    try:
        locations = get_mullvad_locations()
    except ValueError:
        logging.error("Failed to get Mullvad locations.")
        return

    if args.list:
        try:
            list_mullvad_locations(locations)
        except ValueError:
            logging.error("Failed to list Mullvad locations.")
            return
    elif args.country:
        try:
            set_mullvad_location(locations, args.country)
        except ValueError:
            logging.error("Failed to set Mullvad location.")
            return
    else:
        set_random_mullvad_location(locations)

    if not args.list:
        time.sleep(3)
        try:
            show_mullvad_status()
        except ValueError:
            logging.error("Failed to show Mullvad status.")
            return


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    main()
