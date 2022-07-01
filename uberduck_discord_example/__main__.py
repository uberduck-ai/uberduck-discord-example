import asyncio

from .client import bot, terminate_stale_voice_connections

# Replace with your Discord bot token.
# To find this, head to https://discord.com/developers/applications, click your
# application, click "Bot", and click "Reset Token".
DISCORD_TOKEN = "replace-me"


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                terminate_stale_voice_connections(), bot.start(DISCORD_TOKEN)
            )
        )
    except KeyboardInterrupt:
        loop.run_until_complete(bot.close())
    finally:
        loop.close()
