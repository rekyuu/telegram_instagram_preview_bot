# Telegram Instagram Preview Bot

I made this bot because of a real cool guy in our group chat that loves to post Instagram links, but Instagram doesn't have enough of the billions of Facebook dollars to support sending image previews and forces you to click on the link to go to their website, like we're monkeys or something. All it does is download the images/videos and posts them in response to the posted links.

## How to run

1. Clone the repo
2. Rename `secrets.example.env` to `secrets.env`
3. Change `TELEGRAM_TOKEN` to your bot's token
4. Run `docker-compose up`.

## Issues

Currently, image previews don't work in containers for some reason. I'll need to find another library or write something myself.