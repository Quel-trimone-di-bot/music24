import discord
from discord.ext import commands
import asyncio
import os
import ffmpeg
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
VC_CHANNEL_ID = int(os.getenv("VC_CHANNEL_ID"))
RADIO_URL = os.getenv("RADIO_URL", "https://radio.nicolairar.it/listen/nico/radio.mp3")

# Enable necessary intents
intents = discord.Intents.default()
intents.guilds = True
intents.voice_states = True
intents.members = True

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    """Check if the bot is in the server and join the voice channel."""
    print(f"✅ Bot {bot.user} is online!")

    guild = bot.get_guild(GUILD_ID)
    if guild is None:
        print("⚠️ ERROR: The bot is NOT in the specified server!")
        return
    
    print(f"📡 Connected to server: {guild.name}")
    
    await join_and_stream()

async def join_and_stream():
    """Connects the bot to the voice channel and starts streaming."""
    while True:
        try:
            guild = bot.get_guild(GUILD_ID)
            if guild:
                voice_channel = guild.get_channel(VC_CHANNEL_ID)
                if voice_channel:
                    # Disconnect if already connected
                    if bot.voice_clients:
                        await bot.voice_clients[0].disconnect()

                    voice_client = await voice_channel.connect(reconnect=True)
                    print(f"🎶 Connected to {voice_channel.name}")

                    ffmpeg_options = {
                        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                        'options': '-vn'
                    }
                    audio_source = discord.FFmpegPCMAudio(RADIO_URL, **ffmpeg_options)

                    # Debug: Print if audio starts playing
                    print("▶️ Attempting to start audio playback...")
                    voice_client.play(audio_source, after=lambda e: print(f"⚠️ Playback error: {e}") if e else None)

                    await asyncio.sleep(3)  # Short delay to ensure playback starts

                    if voice_client.is_playing():
                        print("🔊 Audio playback started successfully!")
                    else:
                        print("❌ Bot is NOT playing audio.")

                    while True:
                        await asyncio.sleep(5)  # Keep the bot alive

        except Exception as e:
            print(f"⚠️ Streaming error: {e}")
            await asyncio.sleep(10)  # Wait before retrying

@bot.command()
async def stop(ctx):
    """Stops the stream and disconnects the bot."""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("🛑 Bot has disconnected from the voice channel.")

bot.run(TOKEN)
