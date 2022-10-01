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
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(
), description="Bot des Mythology")

##########################################################################
# à la connexion
##########################################################################


@bot.event
async def on_ready():
    # remplacer "général" par le nom du salon
    channel = discord.utils.get(bot.get_all_channels(), name="général")
    await bot.get_channel(channel.id).send("Bonjour à tous !")
    print(f"{bot.user.name} est prêt.")

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
    eventChannel = discord.utils.get(bot.get_all_channels(), name="event")
    divinity = discord.utils.get(ctx.guild.roles, id=1025026978337787944)
    oua = bot.get_emoji(1025125432380629023)
    cdg = bot.get_emoji(1025125331813814292)
    gne = bot.get_emoji(1025125300843065344)
    fn = bot.get_emoji(1025125399786705067)
    prof = bot.get_emoji(1025125464014082128)
    fau = bot.get_emoji(1025125368337797201)
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
        closeCall = await bot.get_channel(eventChannel.id).send(f"{divinity.mention} ! Rassemblez vous les {insulte()} Sauron à besoin de vous comme chair à cannon !\nCela se passera le {day.content}.\n Ramenez pas votre {insulte()} de camarades, il ne nous servirais à rien. Tout juste a nous embêtter.")
        await closeCall.add_reaction(gne)
        await closeCall.add_reaction(oua)
        await closeCall.add_reaction(cdg)
        await closeCall.add_reaction(prof)
        await closeCall.add_reaction(fn)
        await closeCall.add_reaction(fau)
        await closeCall.add_reaction("❌")
    elif reacChoose[0].emoji == "🅾️":
        openCall = await bot.get_channel(eventChannel.id).send(f"{divinity.mention} ! Rassemblez vous les {insulte()} Sauron à besoin de vous comme chair à cannon !\nCela se passera le {day.content}.\n Ramène tes {insulte()} de camarades avec toi, on a besoin de chair à canon, et je pense que t'as pas envie que ça soit toi...")
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


@ bot.command(name="exit")
async def exit(ctx):
    reponse = "Bot déconnecté. Bye Bye !"
    await ctx.reply(reponse)
    await bot.close()

##########################################################################
##########################################################################
##########################################################################
# Exécution du bot
##########################################################################
##########################################################################
##########################################################################
bot.run(token)
