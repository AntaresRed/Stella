import discord
from discord.ext import commands
from googleapiclient.discovery import build
import requests
from json import load
from requests.models import Response

client = commands.Bot(command_prefix="!")

f = open(r'G:\Desktop Folders\Stella\Rules.txt')
rules = f.readlines()

#Load API KEY from json file (One secure way. Dont just put your key in script)
with open("G:/Desktop Folders/Stella/token.json", "r") as file:
    API_KEY = load(file)["youtube_key"]
with open("G:/Desktop Folders/Stella/token.json", "r") as file:
    WEATHER_KEY = load(file)["weather_key"]


#Message to send when bot ready
@client.event 
async def on_ready():
    print("I am ready to go!")

#Message delete command
@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx,number=2):
    await ctx.channel.purge(limit = number)

#Message hello command (Basic replies)
@client.command()
async def hello(ctx):
    await ctx.send("Hii!!!")

#Paste lines from a txt file
@client.command()
async def rule(ctx,*,number):
    await ctx.send(rules[int(number)-1])

#Paste all lines from a txt file
@client.command()
async def fullrules(ctx):
    for line in rules:
        await ctx.send(line)

#Kick members
@client.command()
@commands.has_permissions(manage_messages = True)
async def kick(ctx, member:discord.Member,*,reason="Not provided"):
    await member.send("You have been kicked from the Antares facility, because "+reason+"")
    await member.kick(reason = reason)

#Ban members
@client.command()
@commands.has_permissions(manage_messages = True)
async def ban(ctx, member:discord.Member,*,reason="Not provided"):
    await member.send("You have been banned from the Antares facility, because "+reason+"")
    await member.ban(reason = reason)

#Search channel
@client.command()
async def channel(ctx,*,name):
    mylist = searchchannel(name)
    banner = mylist[2]
    banner = banner.replace(" ", "")
    url = ("https://www.youtube.com/c/%s/about" % banner)
    await ctx.send(url)
    await ctx.send("The subscribers in this channel are: " + mylist[0]+"")
    await ctx.send("The views of this channel are "+mylist[1]+"")

#Search video
@client.command()
async def video(ctx,*,name):
    url = searchvideo(name)
    await ctx.send(url)

#Weather
@client.command()
async def weather(ctx,*,city):
    mylist = weather(city)
    await ctx.send("https://en.wikipedia.org/wiki/{fname}".format(fname = city))
    await ctx.send("Today's weather pattern is "+str(mylist[0])+" with maximum and minimum tempreature "+str(mylist[1])+" *C and "+str(mylist[2])+" *C .We have windspeeds measuring upto "+str(mylist[4])+" kmps and humidity of "+str(mylist[3]))

#Jokes
@client.command()
async def jokes(ctx):
    request = requests.get("https://official-joke-api.appspot.com/jokes/random")
    response = request.json()
    await ctx.send(response["setup"])
    await ctx.send(response["punchline"])

    

def searchvideo(name):
    fname = name
    #Make request to YOUTUBE API With parameters
    request = requests.get(f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={fname}&type=video&key={API_KEY}".format(fname=name))
    #Convert incoming data into json file for easier handling
    response = request.json()
    url = response["items"][0]["id"]["videoId"]
    #Concate video url into final url
    final = ("https://www.youtube.com/watch?v=%s" % url)
    return final


def searchchannel(name):
    fname = name
    request = requests.get(f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={fname}&type=channel&key={API_KEY}".format(fname = name))
    response = request.json()
    Id = response["items"][0]["id"]["channelId"]
    fid = Id
    IDrequest = requests.get(f"https://youtube.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id={fid}&maxResults=1&key={API_KEY}".format(fid = Id))
    response = IDrequest.json()
    subs = response["items"][0]["statistics"]["subscriberCount"]
    views = response["items"][0]["statistics"]["viewCount"]
    banner = response["items"][0]["snippet"]["title"]
    return [subs,views,banner]


def weather(city):
    fname = city
    request = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={fname}&units=metric&appid={WEATHER_KEY}".format(fname = city))
    response = request.json()
    main = response["weather"][0]["description"]
    tmax = response["main"]["temp_max"]
    tmin = response["main"]["temp_min"]
    humidity = response["main"]["humidity"]
    wind = response["wind"]["speed"]
    return [main,tmax,tmin,humidity,wind]


    


#Play music
#@client.command()
##Take in url of music
#async def play(ctx, url_:str):
    #Enter voice channel
#    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name = 'General')
 #   voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  #  if not voice.is_connected():
   #     await voiceChannel.connect()

#Leave voice channel
#@client.command()
#async def leave(ctx):
 #   voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  #  if voice.is_connected():
   #     await voice.disconnect()
    #else:
     #   await ctx.send("Not connected, so cant leave. ")

#Pause command
#@client.command()
#@sync def pause(ctx):
 #   voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  #  if voice.is_playing():
   #     voice.pause()
    #else:
     #   await ctx.send("No audio playing. ")

#Resume command
#@client.command()
#async def resume(ctx):
 #   voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  #  if not voice.is_paused():
   #     voice.resume()
    #else:
     #   await ctx.send("The audio isnt paused. ")

#Stop command
#@client.command()
#async def stop(ctx):
 #    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  #   voice.stop()


client.run('ODY0MTQ3NzYyNTEyOTIwNTc2.YOxOUQ.6sfPOUC_0XSxt-00CH0XPnVSTiI')