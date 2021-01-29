import time
import json
import random
import discord
import requests
from discord.ext import commands

# customizeable

prefix = '$'
try: token = str(open('token.txt','r').readline().strip()); prefix = '>'
except: token = 'do not see me token'

# main bot

fun = {
    'sexy': {
        'emojis': {
            ':nauseated_face:': list(range(11)),
            ':face_vomiting:': list(range(26)),
            ':frowning:': list(range(46)),
            ':face_with_monocle:': list(range(56)),
            ':smirk:': list(range(66)),
            ':kissing_smiling_eyes:': list(range(76)),
            ':heart_eyes:': list(range(86)),
            ':drooling_face:': list(range(100)),
            ':hot_face:': [100],
        }
    },
    'gay': {
        'emojis': {
            ':sunglasses:': [0],
            ':smile:': list(range(16)),
            ':slight_smile:': list(range(36)),
            ':smiling_face_with_tear:': list(range(56)),
            ':face_with_raised_eyebrow:': list(range(76)),
            ':no_mouth:': list(range(86)),
            ':eggplant::sweat_drops:': list(range(100)),
            ':rainbow_flag::rainbow_flag::rainbow_flag::rainbow_flag::rainbow_flag::rainbow_flag::rainbow_flag:': [100],
        }
    },
    'pp': {
        'emojis': {
            ':hot_face:': [0],
            ':face_with_hand_over_mouth:': list(range(4)),
            ':drooling_face::yum:': list(range(8)),
            ':open_mouth::flushed:': list(range(12)),
            ':kissing_smiling_eyes::kiss::kiss::kiss:': list(range(15)),
            ':confounded::persevere::tired_face:': [15],
        }
    },
}

funcopy = fun
invites = {}
spacing = '\u2800'*7
servers = json.load(open('servers.json','r'))

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)
bot.remove_command('help')

## functions

async def config(server, channel):
    global servers
    servers[server] = channel
    with open('servers.json','w') as f:
        json.dump(servers,f)

async def loadInvites(server):
    global invites
    try:
        invites[server.id] = {invite.code:invite.uses for invite in await server.invites()}
    except: print(f'{server.name} has not given perms')

## events

@bot.event
async def on_ready():
    for server in bot.guilds:
        if str(server.id) in servers:
            await loadInvites(server)
    print(f'\n\n{bot.user} is online.\n----------------\n\n')
    await bot.change_presence(activity=discord.Game(name='with your pp', type=1))

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    if isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(
            description = f'I dont have the permissions to do that.',
            colour = discord.Colour(int('ff0000',16))
        )
        await ctx.send(embed=embed)
        print(error)
        return
    print(error)
    embed = discord.Embed(
        description = f'{error}',
        colour = discord.Colour(int('ff0000',16))
    )
    await ctx.send(embed=embed)

@bot.event
async def on_guild_join(ctx):
    await loadInvites(ctx)

@bot.event
async def on_member_join(ctx):
    server = ctx.guild
    if str(server.id) in servers:
        channel = bot.get_channel(servers[str(server.id)])
        used = None
        for invite in await server.invites():
            if invite.code in invites[server.id]:
                if invite.uses > invites[server.id][invite.code]:
                    used = invite
                    break
            elif invite.uses > 0:
                used = invite
                break
        if used:
            await channel.send(f'{ctx.mention} (**{str(ctx)}**) joined; invited by {used.inviter.id} (**{str(used.inviter)}**)')
            await loadInvites(server)
        else:
            await channel.send(f'{ctx.mention} (**{str(ctx)}**) joined; invited by ???')

## commands

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title = f'NCM Bot ( {prefix} )',
        description = 'by idiocrasy#4606',
        colour = discord.Colour(int('000000',16))
    )
    embed.add_field(name = 'setChannel'+spacing,value = 'invite logs',inline=True)
    embed.add_field(name = 'randomban'+spacing,value = ':flushed:',inline=True)
    embed.add_field(name = 'ban',value = 'ban a member',inline=True)
    embed.add_field(name = 'av'+spacing,value = 'discord avatar',inline=True)
    embed.add_field(name = 'google'+spacing,value = 'search a term',inline=True)
    embed.add_field(name = 'lim',value = 'cheapest roblox limited',inline=True)
    embed.add_field(name = 'Fun Commands',value = 'sex, sexy, gay, pp',inline=False)
    embed.add_field(name = 'addy',value = 'my btc addy',inline=False)
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(administrator=True)
async def setChannel(ctx, channel:discord.TextChannel):
    await config(str(channel.guild.id),channel.id)
    embed = discord.Embed(
        description = f'Set __{channel.guild.name}__\'s channel to {channel.mention}',
        colour = discord.Colour(int('00ed3f',16))
    )
    print(f'Set {channel.guild.name}\'s channel to {channel.name}')
    await ctx.send(embed=embed)
    await loadInvites(ctx.guild)

@bot.command()
@commands.has_permissions(administrator=True)
async def randomban(ctx):
    member = random.choice(ctx.guild.members)
    embed = discord.Embed(
        description = f'{member.mention} (**{member}**) was banned',
        colour = discord.Colour(int('00ed3f',16))
    )
    await member.ban()
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member, *, reason=None):
    desc = f'{member.mention} (**{member}**) was banned'
    if reason: desc += f': ***{reason}***'
    embed = discord.Embed(
        description = desc,
        colour = discord.Colour(int('00ed3f',16))
    )
    await member.ban(reason=reason)
    await ctx.send(embed=embed)

@bot.command()
async def av(ctx, member:discord.Member=None):
    if not member: member = ctx.message.author
    await ctx.send(member.avatar_url)

@bot.command()
async def google(ctx, term):
    dictionary = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{term}').json()
    if 'title' in dictionary:
        embed = discord.Embed(
            title = f'{dictionary["title"]}',
            colour = discord.Colour(int('ff0000',16))
        )
        await ctx.send(embed=embed)
    else:
        definitions = []
        for word in dictionary:
            for meaning in word['meanings']:
                for definition in meaning['definitions']:
                    definitions.append('» '+definition['definition'])
        amt = len(definitions)
        definitions = "\n".join(definitions)
        embed = discord.Embed(
            title = f'{term}',
            colour = discord.Colour.green()
        )
        embed.add_field(name=f'{amt} definitions found', value = f'{definitions}')
        await ctx.send(embed=embed)

@bot.command()
async def lim(ctx):
    price = 1234567890
    for limited in requests.get('https://catalog.roblox.com/v1/search/items/details?category=Collectibles&limit=30&sortType=4&subcategory=Collectibles').json()['data']:
        if int(limited['lowestPrice']) < price:
            price = int(limited['lowestPrice'])
            info = limited

    embed = discord.Embed(
        title = f'{info["name"]} @ {price}',
        description = f'https://www.roblox.com/catalog/{info["id"]}',
        colour = discord.Colour.blue()
    )
    embed.set_thumbnail(url=f'https://www.roblox.com/asset-thumbnail/image?assetId={info["id"]}&width=420&height=420&format=png')
    await ctx.send(embed=embed)

@bot.command()
async def sex(ctx):
    await ctx.send(f'{ctx.message.author.mention} had sex with **{random.choice(ctx.guild.members).name}** :flushed:')

@bot.command(aliases=['sexiness','sexyness','sexyrate'])
async def sexy(ctx, member:discord.Member=None):
    if not member: member = ctx.message.author
    try:
        f = fun['sexy'][member.id]
    except:
        f = random.randint(0,100)
        fun['sexy'][member.id] = f
    for x in fun['sexy']['emojis']:
        if f in fun['sexy']['emojis'][x]: break
    await ctx.send(f'{member.name} is {f}% sexy {x}')

@bot.command(aliases=['homo','gayrate','homosexual','gayness'])
async def gay(ctx, member:discord.Member=None):
    if not member: member = ctx.message.author
    try:
        f = fun['gay'][member.id]
    except:
        f = random.randint(0,100)
        fun['gay'][member.id] = f
    for x in fun['gay']['emojis']:
        if f in fun['gay']['emojis'][x]: break
    await ctx.send(f'{member.name} is {f}% gay {x}')

@bot.command(aliases=['penis','ppsize'])
async def pp(ctx, member:discord.Member=None):
    if not member: member = ctx.message.author
    try:
        f = fun['pp'][member.id]
    except:
        f = random.randint(0,15)
        fun['pp'][member.id] = f
    for x in fun['pp']['emojis']:
        if f in fun['pp']['emojis'][x]: break
    await ctx.send(f'{member.name}\'s pp is {f} inches long {x}\n**8{"="*f}D**')

@bot.command()
async def addy(ctx):
    await ctx.send('1AYJYtjpT7CbeRF4KroV7iFA3VGCTf3zDe')

bot.run(token)
