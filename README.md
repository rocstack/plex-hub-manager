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

2. Copy the provided docker-compose.yml content into a file named docker-compose.yml on your system.
Replace the placeholders with your actual Plex URL, Plex token, desired library names, and customization options (if needed).

3. Run the Project: `docker-compose up -d`

## Customization

IGNORE_LIST: Prevent specific hubs from being randomized by adding their names to this list (comma-separated). This is ideal for pinning your favorite or in-progress collections.

## Notes

The randomization occurs at the interval specified in SECONDS_TO_WAIT.
The project logs its activity. You can monitor it using docker logs plex-hub-manager.

## Contributing

Feel free to submit pull requests for bug fixes, improvements, or new features.