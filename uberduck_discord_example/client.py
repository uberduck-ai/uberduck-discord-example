from datetime import datetime, timedelta
from io import BytesIO
from time import sleep
import asyncio
import base64
import random
import requests
import subprocess
import tempfile

import nextcord
from nextcord import SlashOption
from nextcord.ext import commands

from .http import query_uberduck

# It's important to pass guild_ids explicitly while developing your bot because
# commands can take up to an hour to roll out when guild_ids is not passed. Once
# you deploy your bot to production, you can remove guild_ids to add your
# commands globally.
#
# You can find your guild ID by right clicking on the name of your server inside
# Discord and clicking "Copy ID".
DEV_GUILD_ID = -1  # Replace this with your guild ID.
guild_ids = [DEV_GUILD_ID]

guild_to_voice_client = dict()

bot = commands.Bot()


async def terminate_stale_voice_connections():
    while True:
        await asyncio.sleep(5)
        for k in list(guild_to_voice_client.keys()):
            v = guild_to_voice_client[k]
            voice_client, last_used = v
            if datetime.utcnow() - last_used > timedelta(minutes=10):
                await voice_client.disconnect()
                guild_to_voice_client.pop(k)


def _context_to_voice_channel(ctx):
    return ctx.user.voice.channel if ctx.user.voice else None


async def _get_or_create_voice_client(ctx: nextcord.Interaction):
    joined = False
    if ctx.guild.id in guild_to_voice_client:
        voice_client, _ = guild_to_voice_client[ctx.guild.id]
    else:
        voice_channel = _context_to_voice_channel(ctx)
        if voice_channel is None:
            voice_client = None
        else:
            voice_client = await voice_channel.connect()
            joined = True
    return (voice_client, joined)


async def _send_help(ctx):
    await ctx.user.send(
        "See https://uberduck.ai/quack-help for instructions on using the bot commands. Make sure you enter a voice that exactly matches one of the listed voices."
    )


@bot.slash_command(
    name="vc-join",
    guild_ids=guild_ids,
)
async def join_vc(ctx: nextcord.Interaction):
    voice_client, joined = await _get_or_create_voice_client(ctx)
    if voice_client is None:
        await ctx.response.send_message(
            "You're not in a voice channel. Join a voice channel to invite the bot!",
            ephemeral=True,
        )
    elif ctx.user.voice and voice_client.channel.id != ctx.user.voice.channel.id:
        old_channel_name = voice_client.channel.name
        await voice_client.disconnect()
        voice_client = await ctx.user.voice.channel.connect()
        new_channel_name = voice_client.channel.name
        guild_to_voice_client[ctx.guild.id] = (voice_client, datetime.utcnow())
        await ctx.response.send_message(
            f"Switched from #{old_channel_name} to #{new_channel_name}!"
        )
    else:
        await ctx.response.send_message("Connected to voice channel!")
        guild_to_voice_client[ctx.guild.id] = (voice_client, datetime.utcnow())


@bot.slash_command(name="vc-kick", guild_ids=guild_ids)
async def kick_vc(ctx: nextcord.Interaction):
    if ctx.guild.id in guild_to_voice_client:
        voice_client, _ = guild_to_voice_client.pop(ctx.guild.id)
        await voice_client.disconnect()
        await ctx.response.send_message("Disconnected from voice channel")
    else:
        await ctx.response.send_message(
            "Bot is not connected to a voice channel. Nothing to kick.", ephemeral=True
        )


@bot.slash_command(
    name="vc-quack",
    guild_ids=guild_ids,
)
async def speak_vc(
    ctx: nextcord.Interaction,
    voice: str = SlashOption(
        name="voice", description="Voice to use for synthetic speech", required=True
    ),
    speech: str = SlashOption(
        name="speech", description="Speech to synthesize", required=True
    ),
):
    voice_client, _ = await _get_or_create_voice_client(ctx)
    if voice_client:
        guild_to_voice_client[ctx.guild.id] = (voice_client, datetime.utcnow())
        await ctx.response.defer(ephemeral=True, with_message=True)
        audio_data = await query_uberduck(speech, voice)
        with tempfile.NamedTemporaryFile(
            suffix=".wav"
        ) as wav_f, tempfile.NamedTemporaryFile(suffix=".opus") as opus_f:
            wav_f.write(audio_data.getvalue())
            wav_f.flush()
            subprocess.check_call(["ffmpeg", "-y", "-i", wav_f.name, opus_f.name])
            source = nextcord.FFmpegOpusAudio(opus_f.name)
            voice_client.play(source, after=None)
            while voice_client.is_playing():
                await asyncio.sleep(0.5)
            await ctx.send("Sent an Uberduck message in voice chat.")
    else:
        await ctx.response.send_message(
            "You're not in a voice channel. Join a voice channel to invite the bot!",
            ephemeral=True,
        )


@bot.slash_command(
    name="help",
    description="List all voices available to /quack",
    guild_ids=guild_ids,
)
async def _quack_help(ctx):
    await ctx.send("Sending help in private message.")
    await _send_help(ctx)
