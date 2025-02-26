import discord
from discord.ext import commands
import asyncio
import os
import ffmpeg
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
VC_CHANNEL_ID = int(os.getenv("VC_CHANNEL_ID"))
RADIO_URL = os.getenv("RADIO_URL", "https://radio.nicolairar.it/listen/nico/radio.mp3")

# Bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} is online!")
    await join_and_stream()

async def join_and_stream():
    """Connects the bot to the voice channel and starts streaming the radio."""
    while True:
        try:
            guild = discord.utils.get(bot.guilds, id=GUILD_ID)
            if guild:
                voice_channel = discord.utils.get(guild.voice_channels, id=VC_CHANNEL_ID)
                if voice_channel:
                    voice_client = await voice_channel.connect(reconnect=True)
                    print(f"🎶 Connected to {voice_channel.name}")

                    ffmpeg_options = {'options': '-vn'}
                    audio_source = discord.FFmpegPCMAudio(RADIO_URL, **ffmpeg_options)

                    while True:
                        if not voice_client.is_playing():
                            voice_client.play(audio_source)
                        await asyncio.sleep(5)

        except Exception as e:
            print(f"⚠️ Streaming error: {e}")
            await asyncio.sleep(10)  # Wait before retrying

@bot.event
async def on_voice_state_update(member, before, after):
    """Rejoins the voice channel if the bot is disconnected."""
    if member == bot.user and before.channel and not after.channel:
        print("🚨 Bot got disconnected! Attempting to reconnect...")
        await asyncio.sleep(5)
        await join_and_stream()

@bot.command()
async def stop(ctx):
    """Stops the stream and disconnects the bot from the voice channel."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("🛑 Bot has disconnected from the voice channel.")

bot.run(TOKEN)
