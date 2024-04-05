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


def reorder_hub(hub_id: str, after_hub_id: str, section_id: int = 1):
    url = f"{userInputs.plex_url}/hubs/sections/{section_id}/manage/{hub_id}/move?after={after_hub_id}"
    headers = {'X-Plex-Token':  userInputs.plex_token}

    response = requests.put(url, headers=headers)

    if response.status_code == 200:
        print("Hub order updated successfully", hub_id)
    else:
        print(f"Failed to update hub order. Error: {response.text}")


def randomize_hub_order(plex, library_name: str):
    movie_library = plex.library.section(library_name)

    hubs = movie_library.hubs()

    # Filter based on title and build identifiers list
    ignore_list = userInputs.ignore_list.split(",")
    identifiers_to_reorder = [clean_identifier(hub.hubIdentifier) for hub in hubs
                              if hub.title not in ignore_list]

    random.shuffle(identifiers_to_reorder)

    for i in range(len(identifiers_to_reorder) - 1):
        current_id = identifiers_to_reorder[i]
        next_id = identifiers_to_reorder[i + 1]

        reorder_hub(current_id, next_id, hubs[0].librarySectionID)


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
