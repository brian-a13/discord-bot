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
async def on_ready():
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
            #Bot connects to VC
            vc = await after.channel.connect()
            
            generated_name_audio = generate_tts_audio(member.name)
            #add the path to the ffmpeg bin file to the user variables for the systems PATH 
            audio_source = FFmpegPCMAudio(generated_name_audio)
            vc.play(audio_source, after=lambda e: print("Done playing"))


            while vc.is_playing():  #After playing audio, Bot will disconnect from thr VC
                await asyncio.sleep(1)
            await vc.disconnect()

bot.run(bot_token)