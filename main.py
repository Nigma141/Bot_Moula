#Importation des librairies
import asyncio
import discord
from discord.ext import commands, tasks
from discord_slash import ButtonStyle, SlashCommand
from discord_slash.utils.manage_components import *
import os
import sys

#Importation des autres fichiers
import messages
import  Moula
import db

# chemin et Token
txt=open("token.txt", "r")
token=txt.readlines()[0]
txt.close()

pth='BaseDiscord.db'



client = commands.Bot(command_prefix = ",", description = "LeBostonMoulatise")
slash = SlashCommand(client, sync_commands=True)

@client.event
async def on_ready():
    print("le boston des thuisses est présent")

@client.event
async def on_member_join(member):
    await client.get_channel(904401747013955688).send(messages.BienvenuMsgAll)
    await client.get_channel(904401747013955688).send(f"Bienvenue a toi {member.name} !!!!")
    guild = member.guild
    category = discord.utils.get(guild.categories, id =904764160469004330)

    await category.create_text_channel(name='salon-de-{}'.format(member.name))
    IDChannel1 = discord.utils.get(guild.channels, name='salon-de-'+str(member.name.lower()))
    await client.get_channel(IDChannel1.id).send(messages.BienvenuMsg)
    db.AjoutJouer(member.id,pth)

@client.command(aliases=['rgl'])
async def regle(message):
    await message.channel.purge(limit=1)
    await message.send(messages.regleMsg)

@client.command(aliases=['clc'])
async def clear(message,*,amount=1):
    await message.channel.purge(limit=amount+1)

@client.command(aliases=['arr'])
async def arrivee(message):
    member=message.author
    await client.get_channel(904401747013955688).send(messages.BienvenuMsgAll)
    await client.get_channel(904401747013955688).send(f"Bienvenue a toi {member.name} !!!!")
    guild = member.guild
    category = discord.utils.get(guild.categories, id =905484635121795153)

    await category.create_text_channel(name='salon-de-{}'.format(member.name))
    IDChannel1 = discord.utils.get(guild.channels, name='salon-de-'+str(member.name.lower()))
    await client.get_channel(IDChannel1.id).send(messages.BienvenuMsg)
    db.AjoutJouer(member.id,pth)

@client.command()
async def status(ctx):
    print(client.get_channel(904825070382366741).overwrites)

@client.command()
async def init(ctx):
    os.remove("BaseDiscord.db")
    await client.get_channel(904401747013955688).purge(limit=100)
    await client.get_channel(904401747013955688).send(file=discord.File('baniere.png'))

    # mettre message initialisation

    db.CreateBase(pth)
    Moula.init(Moula.listeCac, pth)

    #supprimer message d init

    #mettre les messages  des regles

@client.command(aliases=["st"])
async def info(ctx):
    await ctx.channel.purge(limit=1)
    Liste=db.StatusJoueur(pth,ctx.author.id)
    await client.get_channel(ctx.channel.id).send(messages.MessCompt(Liste))

@client.command(aliases=["f5"])
async def actu(msg):
    Moula.Actu(Moula.listeCac,pth)

@client.command()
async def rout(msg):
    while not client.is_closed():
        await asyncio.sleep(5)
        print('bonjour')


@client.command()
async def acheter(ctx,index=1):
    options,fini=messages.gestionListe(Moula.listeCac, index)
    select = create_select(options, placeholder="choisi dans la liste", min_values=1,max_values=1)
    achat = await ctx.send("quelle achat veux tu faire ?", components=[create_actionrow(select)])
    def check(m):
        return m.author_id == ctx.author.id and m.origin_message.id == achat.id

    achat_ctx = await wait_for_component(client, components=select, check=check)


    if achat_ctx.values[0]== str(index+24):
        await acheter(ctx,index+24)
    elif achat_ctx.values[0]== "1":
        await ctx.channel.purge(limit=2)
        await achat_ctx.send("Dommage jeune bougre")
    else:
        await ctx.channel.purge(limit=2)
        await achat_ctx.send("Votre achat a été réalisé ")

client.run(token)
