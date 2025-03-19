import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from gtts import gTTS
import os
import asyncio
import dotenv
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

#Generate TTS Audio here
def generate_tts_audio(username):
    tts = gTTS(text=f"{username} has joined.", lang="en")
    filename = "welcome.mp3"
    tts.save(filename)
    print(f"Generated TTS file: {filename}") 
    return filename

@bot.event
async def on_ready(): #When bot is ready, this will display
    print(f"{bot.user.name} is ready for work!")

@bot.event
async def on_voice_state_update(member, before, after):
    #Check if someone is in VC
    if before.channel is None and after.channel is not None:
        print(f"{member.name} joined {after.channel.name}")

        #Checks if bot is already in VC
        if bot.user in after.channel.members:
            print("Bot is already in the voice channel.")
        else:
            #Bot connects to VC here
            vc = await after.channel.connect()

            #Play TTS audio
            filename = generate_tts_audio(member.name)

             #Use FFmpeg to play audio
            audio_source = discord.FFmpegPCMAudio(filename)
            vc.play(audio_source, after=lambda e: print("Done playing"))


            while vc.is_playing():  #After playing TTS, Bot will disconnect
                await asyncio.sleep(1)
            await vc.disconnect()

bot.run(bot_token) #Bot token here