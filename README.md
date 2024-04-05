# Plex Hub Manager

This project provides a simple yet effective way to randomize the order of collections (hubs) on your Plex home screen and within individual library sections. Add an element of surprise and rediscover content in your Plex library!

## Why Randomize Hub Order?

Break out of viewing ruts: Randomization helps you discover movies or shows you might have overlooked.
Fresh perspective: A shuffled hub order can make your library feel new and exciting.
Customization: Pin specific hubs you always want at the top and selectively randomize others.

## How to Use

Prerequisites:

- A running Plex Media Server.
- Docker and Docker Compose installed on your system.
- Get Your Plex Token:
Follow this guide to obtain your Plex authentication token: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

1. Create the docker-compose.yml File:

```yaml
version: '2.1'
services:
  plex-hub-manager:
    image: silkychap/plex-hub-manager:latest
    container_name: plex-hub-manager
    environment:
      - PLEX_URL=<Your plex url> # eg http://192.168.0.142:32400
      - PLEX_TOKEN=<Your plex token>
      - LIBRARY_NAMES=Films,TV Shows # Names of your plex libraries
      - SECONDS_TO_WAIT=86400 # Time between executions
      - IGNORE_LIST=Continue Watching,Recently Released Movies # Names of the collections you want the randomiser to ignore
    restart: unless-stopped

```

2. Copy the provided docker-compose.yml content into a file named docker-compose.yml on your system.
Replace the placeholders with your actual Plex URL, Plex token, desired library names, and customization options (if needed).

3. Run the Project: `docker-compose up -d`

## Customization

IGNORE_LIST: Prevent specific hubs from being randomized by adding their names to this list (comma-separated). This is ideal for pinning your favorite or in-progress collections.

LIBRARY_NAMES: The actual names of the libraries you want it to randomise

## Notes

The randomization occurs at the interval specified in SECONDS_TO_WAIT.
The project logs its activity. You can monitor it using docker logs plex-hub-manager.

## Contributing

Feel free to submit pull requests for bug fixes, improvements, or new features.