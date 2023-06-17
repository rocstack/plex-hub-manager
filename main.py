import os
from plexapi.server import PlexServer
from utils.classes import UserInputs

# userInputs = UserInputs(
#     plex_url=os.getenv("PLEX_URL"),
#     plex_token=os.getenv("PLEX_TOKEN"),
#     library_name=os.getenv("LIBRARY_NAME"),
# )

userInputs = UserInputs(
    plex_url="http://192.168.0.21:32400",
    plex_token="6mz1G4Dtn14K_tdETQTg",
    library_name="Films",
)


def run():
    name = "Plex"
    print(f'Starting collection run, {name}')
    try:
        plex = PlexServer(userInputs.plex_url, userInputs.plex_token)
        print("Connected to Plex server")
    except Exception as e:
        print("Plex Authorization error")
        return


if __name__ == '__main__':
    run()

