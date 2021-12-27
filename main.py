# Importation des librairies
import asyncio
import discord
from discord.ext import commands, tasks
from discord_slash import ButtonStyle, SlashCommand
from discord_slash.utils.manage_components import *
import os
import sys

# Importation des autres fichiers
import messages
import Moula
import db

# Initialisation du bot
txt = open("token.txt", "r")
token = txt.readlines()[0]
txt.close()

pth = 'BaseDiscord.db'


intents=discord.Intents.all()

client = commands.Bot(command_prefix=",",intents=intents, description="LeBostonMoulatise")
slash = SlashCommand(client, sync_commands=True)


@client.event
async def on_ready():
    print("le boston des thuisses est présent")
    while not client.is_closed():
        await asyncio.sleep(180)
        Moula.Actu(Moula.listeCac, pth)

@client.event
async def on_member_join(member):
    print("quelqu un est arrivé")
    await client.get_channel(904401747013955688).send(messages.BienvenuMsgAll)
    await client.get_channel(904401747013955688).send(f"Bienvenue a toi {member.name} !!!!")
    guild = member.guild
    category = discord.utils.get(guild.categories, id=905484635121795153)

    await category.create_text_channel(name='salon-de-{}'.format(member.name))
    IDChannel1 = discord.utils.get(guild.channels, name='salon-de-' + str(member.name.lower()))
    await client.get_channel(IDChannel1.id).send(messages.BienvenuMsg)
    db.AjoutJouer(member.id, pth)

@client.command(aliases=['rgl'])
async def regle(message):
    await message.channel.purge(limit=1)
    await message.send(messages.regleMsg)

@client.command(aliases=['clc'])
async def clear(message, *, amount=1):
    await message.channel.purge(limit=amount + 1)

@client.command(aliases=['arr'])
async def arrivee(message):
    member = message.author
    await client.get_channel(904401747013955688).send(messages.BienvenuMsgAll)
    await client.get_channel(904401747013955688).send(f"Bienvenue a toi {member.name} !!!!")
    guild = member.guild
    category = discord.utils.get(guild.categories, id=905484635121795153)

    await category.create_text_channel(name='salon-de-{}'.format(member.name))
    IDChannel1 = discord.utils.get(guild.channels, name='salon-de-' + str(member.name.lower()))
    await client.get_channel(IDChannel1.id).send(messages.BienvenuMsg)
    db.AjoutJouer(member.id, pth)

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
    Moula.init(Moula.ListeActif,Moula.NomActif, pth)

@client.command(aliases=["st"])
async def info(ctx):
    await ctx.channel.purge(limit=1)
    Liste = db.StatusJoueur(pth, ctx.author.id)
    await client.get_channel(ctx.channel.id).send(messages.MessCompt(Liste))

@client.command(aliases=["f5"])
async def actu(msg):
    Moula.Actu(Moula.listeCac, pth)

@client.command()
async def acheter(ctx, index=0,index2=0):
    liste,fini=messages.gestionListe(Moula.ListeListeActif, Moula.NomListeListe,index)
    await ctx.send(liste)
    selection = create_select(liste, placeholder="choisi dans la liste", min_values=1, max_values=1)

    Choix = await ctx.send("Dans quelle liste veux tu choisir ?", components=[create_actionrow(selection)])
    def check2(m):
        return m.author_id == ctx.author.id and m.origin_message.id == Choix.id

    choix_ctx = await wait_for_component(client, components=selection, check=check2)


    if choix_ctx.values[0] == "0":
        await ctx.channel.purge(limit=2)
        await choix_ctx.send("Dommage jeune bougre")
    else:
        await ctx.send(choix_ctx.values[0])
        await ctx.send(Moula.ListeListeActif[int(choix_ctx.values[0])-1][0])
        options, fini = messages.gestionListe(Moula.ListeListeActif[int(choix_ctx.values[0])-1], Moula.NomListeListe[int(choix_ctx.values[0])-1], index2)
        print("voici les options")
        print(options)
        select = create_select(options, placeholder="choisi dans la liste", min_values=1, max_values=1)
        achat = await ctx.send("quelle achat veux tu faire ?", components=[create_actionrow(select)])

        def check(m):
            return m.author_id == ctx.author.id and m.origin_message.id == achat.id

        achat_ctx = await wait_for_component(client, components=select, check=check)

        if achat_ctx.values[0] == str(index2 + 24):
            await acheter(ctx, index, index2 + 24)
        elif achat_ctx.values[0] == "0":
            await ctx.channel.purge(limit=2)
            await achat_ctx.send("Dommage jeune bougre")
        else:
            ctx.send("Combien veux tu en acheter ?")
            def check3(msg):
                return( msg.author== ctx.author and msg.channel == ctx.channel)
            msg = await  client.wait_for("message",check=check3, timeout=30)

            print(msg)
            VolumeDemande=float(msg)
            message = db.AcheterAction(pth, ctx.author.id, Moula.listeCac[int(achat_ctx.values[0]) - 2], 1)
            await ctx.channel.purge(limit=2)

            await achat_ctx.send(message)

@client.command()
async def vendre(Vente_ctx, indice=0):
    Portefeuille = db.ReturnPtf(pth, Vente_ctx.author.id)
    await Vente_ctx.channel.purge(limit=1)
    if len(Portefeuille) != 0:
        print(Portefeuille)

        NomAction = [Moula.NomCac[Moula.listeCac.index(elm[1])] for elm in Portefeuille]
        print(NomAction.values)

        options, fini = messages.gestionVente(NomAction, indice, NomAction)
        select = create_select(options, placeholder="choisi dans la liste", min_values=1, max_values=1)
        Vente = await Vente_ctx.send("quelle actions veux tu vendre ?", components=[create_actionrow(select)])

        def check(m):
            return m.author_id == Vente_ctx.author.id and m.origin_message.id == Vente.id

        achat_ctx = await wait_for_component(client, components=select, check=check)

        if achat_ctx.values[0] == str(indice + 24):
            await acheter(Vente_ctx, indice + 24)
        elif achat_ctx.values[0] == "1":
            await Vente_ctx.channel.purge(limit=2)
            await achat_ctx.send("Dommage jeune bougre")
        else:
            message = db.VenteAction(pth, Vente_ctx.author.id, Moula.listeCac[int(achat_ctx.values[0]) - 1], 1)
            await Vente.channel.purge(limit=2)

            await achat_ctx.send(message)
    else:
        await Vente_ctx.send("T'es pauvre t'as pas d'action")
    await Vente_ctx.send(str(Portefeuille))

@client.command()
async def quit(ctx):
    await client.logout()

@client.command()
async def cours():
    pass

client.run(token)
