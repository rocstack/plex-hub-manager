import os
import time
import requests
import random
from plexapi.server import PlexServer
from utils.classes import UserInputs

userInputs = UserInputs(
    plex_url=os.getenv("PLEX_URL"),
    plex_token=os.getenv("PLEX_TOKEN"),
    library_names=os.getenv("LIBRARY_NAMES", 'Films,TV Shows'),
    ignore_list=os.getenv("IGNORE_LIST", 'Continue Watching,Recently Released Movies'),
    wait_seconds=int(os.getenv("SECONDS_TO_WAIT", 86400))
)


def clean_identifier(hub_identifier: str):
    parts = hub_identifier.split('.')
    if len(parts) >= 2 and parts[-1] == parts[-2]:  # Duplicate at the end
        clean_identifier = '.'.join(parts[:-1])
    elif parts[-1].isdigit():  # Handles various cases ending with a digit
        clean_identifier = '.'.join(parts[:-1])
    else:
        clean_identifier = hub_identifier

    # Secondary check for trailing '.1'
    if clean_identifier.endswith('.1'):
        clean_identifier = clean_identifier[:-2]  # Remove the trailing '.1'

    return clean_identifier


def reorder_hub(hub_title: str, hub_id: str, after_hub_id: str, section_id: int = 1):
    url = f"{userInputs.plex_url}/hubs/sections/{section_id}/manage/{hub_id}/move?after={after_hub_id}"
    headers = {'X-Plex-Token':  userInputs.plex_token}

    response = requests.put(url, headers=headers)

    if response.status_code == 200:
        print(f"Hub order updated successfully: {hub_title}")
    else:
        print(f"Failed to update hub order for {hub_title}. Error: {response.text}")


def validate_ignore_list(hubs, ignore_list, library_name):
    existing_hub_titles = {hub.title for hub in hubs}
    valid_ignore_list = []
    invalid_entries = []

    for entry in ignore_list:
        if entry in existing_hub_titles:
            valid_ignore_list.append(entry)
        else:
            invalid_entries.append(entry)

    print("Validated Ignore List:")
    print(f"Valid Entries: {valid_ignore_list}")
    if invalid_entries:
        print(f"Invalid Entries (not found in {library_name}): {invalid_entries}")

    return valid_ignore_list


def randomize_hub_order(plex, library_name: str):
    movie_library = plex.library.section(library_name)
    hubs = movie_library.hubs()

    # Validate ignore list
    ignore_list = userInputs.ignore_list.split(",")
    valid_ignore_list = validate_ignore_list(hubs, ignore_list, library_name)

    # Filter based on title and build identifiers list
    hubs_to_reorder = [(hub.title, clean_identifier(hub.hubIdentifier)) for hub in hubs
                       if hub.title not in valid_ignore_list]

    random.shuffle(hubs_to_reorder)

    for i in range(len(hubs_to_reorder) - 1):
        current_title, current_id = hubs_to_reorder[i]
        next_id = hubs_to_reorder[i + 1][1]

        reorder_hub(current_title, current_id, next_id, hubs[0].librarySectionID)


def run():
    while True:
        print("Starting hub randomizer...")

        try:
            plex = PlexServer(userInputs.plex_url, userInputs.plex_token)
            print("Connected to Plex server")
        except Exception as e:
            print("Plex Authorization error", e)
            return

        # Randomize the order of the hubs for each library
        library_names = userInputs.library_names.split(",")
        for library_name in library_names:
            print(f"Randomizing hub order for library: {library_name}")
            randomize_hub_order(plex, library_name)

        print("Waiting on next call...")
        time.sleep(userInputs.wait_seconds)


if __name__ == '__main__':
    run()
