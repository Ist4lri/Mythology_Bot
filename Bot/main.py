from asyncio import wait_for
from numbers import Number
from random import randint
import discord
from discord.ext import commands

sobriquet = ["raclures", "minables", "vers de terre",
             "bon à rien", "mangeur de terres", "engeance d'hommes rats"]


# -------------------- on récupère le token
with open("/home/pl/Bureau/Code/Discord_Bots/Mytho/Mythology/Bot/token.txt", "r", encoding="utf-8") as fichier:
    token = fichier.readline()


# -------------------- on choisit le préfixe pour nos commandes, ici !
bot = commands.Bot(command_prefix="/", intents=discord.Intents.all(
), description="Bot des Mythology")

##########################################################################
# à la connexion
##########################################################################


@bot.event
async def on_ready():
    # remplacer "général" par le nom du salon
    channel = discord.utils.get(bot.get_all_channels(), name="olympe")
    await bot.get_channel(channel.id).send(f"Bot up. Pour m'invoquer, utilisez le préfixe :{bot.command_prefix}")
    print(f"{bot.user.name} est prêt. Le préfixe :{bot.command_prefix}")

##########################################################################
# en cas d'erreur dans les commandes
##########################################################################


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("Vérifier votre commande.")
    else:
        raise error

##########################################################################
# en cas d'arrivée sur le serveur
##########################################################################

welcomeList = ["Circule vermine !", "T'as pris ton temps, raclure.", "Sauron te désavouerais si il te voyait.",
               "Fait c'que j'te dis...", "Minable ! Un minable de plus dans nos rangs !", "Je vais te donner en pâture aux vers..."]


@bot.event
async def on_member_join(member):
    Index = randint(0, len(welcomeList)-1)
    await member.send(welcomeList[Index])
    channel = member.guild.system_channel
    if channel is not None:
        await channel.send(f'Immonde {member.mention} ! Tu me donnes envie de vomir !')
    else:
        print('Il faut définir le channel Welcome !')


##########################################################################
# Coucou
##########################################################################


@bot.command(name="coucou")
async def bonjour(ctx):
    reponse = f"Ça va, {ctx.message.author.mention} ?"
    await ctx.reply(reponse)


##########################################################################
# Event
##########################################################################


@bot.command()
async def event(ctx):
    eventChannel = discord.utils.get(
        bot.get_all_channels(), id=995675244666822787)
    openEventChannel = discord.utils.get(
        bot.get_all_channels(), id=1021488753568649306)
    divinity = discord.utils.get(ctx.guild.roles, id=995739644744454195)
    oua = bot.get_emoji(995754889131065366)
    cdg = bot.get_emoji(995754346178420756)
    gne = bot.get_emoji(995754293820923925)
    fn = bot.get_emoji(995756263545782334)
    prof = bot.get_emoji(995762015333261466)
    fau = bot.get_emoji(995754611333935114)
    sauron = bot.get_emoji(995755177061654588)
    await ctx.send("Préparation de l'event...")
    await ctx.author.send("Quel serait le jour ? (Mettez le sous la forme DD/MM/YYYY)")

    def checkMessage(message):
        return message.author == ctx.message.author and ctx.message.channel != message.channel

    # Pour avoir accès a day, day.content
    try:
        day = await bot.wait_for("message", timeout=15, check=checkMessage)
    except:
        await ctx.author.send("Toujours là ? Il faudrait recomencer...")
        return

    ofOption = await ctx.author.send("Groupe ouvert 🅾️ ou fermé 🚪 ?")
    await ofOption.add_reaction("🅾️")
    await ofOption.add_reaction("🚪")

    def checkEmojis(reaction, user):
        return ctx.message.author == user and (str(reaction.emoji) == "🅾️" or str(reaction.emoji) == "🚪")

    def checkNumber(message):

        return ctx.message.author == message.author and isinstance(message.content, Number)

    # pour avoir accès a l'émojis, reacChoose[0.emoji]
    try:
        reacChoose = await bot.wait_for("reaction_add", timeout=15, check=checkEmojis)
    except:
        await ctx.author.send("Toujours là ? Il faudrait recomencer...")
        return

    await ctx.author.send('Ok ! J\'ai bien tout enregistre ! Let\'s go to l\'annoncer')

    def insulte():
        index = randint(0, len(sobriquet))
        Insulte = sobriquet[index-1]
        return Insulte

    if reacChoose[0].emoji == "🚪":
        closeCall = await bot.get_channel(eventChannel.id).send(f"**Jour de raid les {insulte()} de {divinity.mention}⚔️!**\n\n**Ce sera le : {day.content} 📅.**\n\n**Ramènes tes fesses à 21h00, et le départ est à 21h30 🕛. Soit pas en retard, {insulte()}, tu tateras de mon fouet sinon...**\n\n**Objectif : Les landes ne tremblent pas assez devant nous ! Faisons leur une frayeur !🎯**\n\n**Réagissez avec la classe avec laquelle tu viens. Et ton {insulte()} d'ami qui n'est pas dans la tribu n'est pas invité...Il serait gênant.**\n\n\n**__{sauron}POUR SAURON{sauron}__**")
        await closeCall.add_reaction(gne)
        await closeCall.add_reaction(oua)
        await closeCall.add_reaction(cdg)
        await closeCall.add_reaction(prof)
        await closeCall.add_reaction(fn)
        await closeCall.add_reaction(fau)
        await closeCall.add_reaction("❌")
    elif reacChoose[0].emoji == "🅾️":
        openCall = await bot.get_channel(openEventChannel.id).send(f"**Jour de raid les {insulte()} de {divinity.mention}⚔️!**\n\n**Rassemblez vous les {insulte()} Sauron à besoin de vous comme chair à cannon !Ramènes toi à 21h00, on part à 21h30, et on prendra aucun retardataire !🕛**\n\n**Cela se passera le {day.content} 📅.**\n\n**Ramène tes {insulte()} de camarades avec toi, on a besoin de chair à canon, et je pense que t'as pas envie que ça soit toi...**\n\n**Objectif : TUER DU HEROS 🎯 ! Réagissez avec la classe avec laquelle tu viens.**\n\n\n**__{sauron}POUR SAURON{sauron}__**")
        await openCall.add_reaction(gne)
        await openCall.add_reaction(oua)
        await openCall.add_reaction(cdg)
        await openCall.add_reaction(prof)
        await openCall.add_reaction(fn)
        await openCall.add_reaction(fau)
        await openCall.add_reaction("❌")
    else:
        await ctx.author.send("Euuuuh...En fait y'a une erreur. Recommence s'il te plait, j'ai du m'embrouiller...")

##########################################################################
# Réaction de message
##########################################################################

    '''
    oua = bot.get_emoji(1025125432380629023)
    cdg = bot.get_emoji(1025125331813814292)
    gne = bot.get_emoji(1025125300843065344)
    fn = bot.get_emoji(1025125399786705067)
    prof = bot.get_emoji(1025125464014082128)
    fau = bot.get_emoji(1025125368337797201)
    '''


##########################################################################
# Clear
##########################################################################


@bot.command()
async def clear(ctx):
    await ctx.channel.purge(limit=100000)

##########################################################################
# Déconnexion
##########################################################################


@bot.command(name="exit")
async def exit(ctx):
    reponse = "Veuillez MP <@974353774032334848> pour pouvoir shutdown le bot."
    await ctx.reply(reponse)


##########################################################################
# Help
# *
@bot.command(name="help")
async def help(ctx):
    reponse = "La liste des commandes :\n-/coucou\n-/exit\n-/event\n-/clear"

##########################################################################
##########################################################################
##########################################################################
# Exécution du bot
##########################################################################
##########################################################################
##########################################################################
bot.run(token)
