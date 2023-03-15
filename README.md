# uberduck-discord-example

A Discord bot that uses the [Uberduck API](https://uberduck.readme.io/) for text-to-speech in voice channels. See the [Uberduck blog](https://uberduck.ai/blog/build-a-text-to-speech-discord-bot-in-python) for a full tutorial on building this bot.

## Install dependencies

1. Install [ffmpeg](https://ffmpeg.org/download.html) if not already installed.
2. Ensure you have the [Opus audio codecs](https://opus-codec.org/).
3. Create a fresh Python environment. I like to use Miniconda, which you can
   install [here](https://docs.conda.io/en/latest/miniconda.html).

   ```
   conda create -n uberduck-discord-example python=3.8
   conda activate uberduck-discord-example
   pip install -e .
   ```

## Run

Add your Discord Bot token, Uberduck API key, and Uberduck API secret into the
code.

Then you can run the bot via:

```
python -m uberduck_discord_example
```
