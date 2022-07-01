# uberduck-discord-example

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
pyton -m uberduck_discord_example
```
