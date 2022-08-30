import nextcord
import server
import datetime
import os
from nextcord.ext import commands

# NEVER publish this!!!
CLIENT_TOKEN = os.environ["CLIENT_TOKEN"]

# ----- Vars n stuff ----- #
help_txt = {
    "help": "The help command",
    "count [candidate]": "Get the current vote counts. Will provide the counts for [candidate] if provided",
    "vote <candidate>": "Cast a vote for <candidate>"
}
client = commands.Bot(command_prefix = "$", help_command = None)
user_whitelist = server.getwhitelist()

# ----- Events ----- #
@client.event
async def on_ready():
    print("bot online!")
    await client.change_presence(activity = nextcord.Activity(type = nextcord.ActivityType.watching, name = server.getstatus()))

    # Waking server message
    embed = nextcord.Embed(title = ":sleeping: Waking server, please wait", description = "This may take a few seconds", color = nextcord.Color.blurple())
    await client.get_channel(1007535110737899522).send(embed = embed)
    server_ping = server.ping()

    if server_ping == "success":
        embed = nextcord.Embed(title = ":white_check_mark: Server woke successfully", color = nextcord.Color.green())
    else:
        embed = nextcord.Embed(title = ":no_entry: Server failed to wake", description = server_ping, color = nextcord.Color.red())
    await client.get_channel(1007535110737899522).send(embed = embed)

# ----- Commands ----- #
@client.command()
async def help(ctx):
    embed = nextcord.Embed(title = "Help", description = "My commands are listed below", color = nextcord.Color.blurple())

    for command_name, command_desc in help_txt.items():
        embed.add_field(name = command_name, value = command_desc, inline = False)

    await ctx.reply(embed = embed)

@client.command()
async def test(ctx):
    await ctx.reply("test")

# ----- Electoral commands ----- #
@client.command()
async def count(ctx, arg = ""):
    if arg == "": count = server.get_count()
    else: 
        count = server.get_count(arg)
        if count == "failure: candidate not in counts dict":
            embed = nextcord.Embed(title = "Error: unknown candidate", description = "failure: the specified candidate isn't in the database. Please try again", color = nextcord.Color.red())
            await ctx.reply(embed = embed)
            return

    if arg == "": embed_title = "Vote counts"
    else: embed_title = f"Vote counts for {arg}"

    if arg.lower() in count.keys():
        embed = nextcord.Embed(title = embed_title, description = f"Figures are as of {str(datetime.date.today())}", color = nextcord.Color.blurple())
    elif arg == "":
        embed = nextcord.Embed(title = embed_title, description = f"Figures are as of {str(datetime.date.today())}", color = nextcord.Color.blurple())
    else:
        embed = nextcord.Embed(title = embed_title, description = "failure: the specified candidate isn't in the database. Please try again", color = nextcord.Color.red())
        await ctx.reply(embed = embed)
        return
    
    if arg == "":
        leaders = []

        for i in count.keys():
            field_name = ""

            if count[i] == max(count.values()): 
                field_name = f":crown: {i.title()} - {count[i]}"
                leaders.append(i.title())
            else: field_name = f"{i.title()} - {count[i]}"

            embed.add_field(name = field_name, value = f"`$vote {i}`")
        
        if len(leaders) == 1:
            embed.set_footer(text = f"Current leader: {leaders[0]}")
        else:
            footer_string = ""
            for i in leaders:
                footer_string += f"{i}, "
            footer_string = footer_string.rstrip(footer_string[-1])
            
            embed.set_footer(text = f"Current leaders: {footer_string.rstrip(footer_string[-1])}")

    else:
        embed.add_field(name = arg.title(), value = count[arg.lower()], inline = False)

    await ctx.reply(embed = embed)

@client.command()
async def register(ctx):
    user_whitelist = server.getwhitelist()
    if str(ctx.author.id) in user_whitelist:
        embed = nextcord.Embed(title = "User whitlisted", description = "You are whitelisted; there is no need to register to vote :slight_smile:", color = nextcord.Color.green())
    else:
        r = server.register(ctx.author.id)
        if r["error"] == True: embed_color = nextcord.Color.red()
        else: embed_color = nextcord.Color.green()
        embed = nextcord.Embed(title = r["header"], description = r["content"], color = embed_color)

    await ctx.reply(embed = embed)

@client.command()
async def vote(ctx, arg = ""):
    if arg == "":
        embed = nextcord.Embed(title = "Please choose a candidate", description = "You need to select a candidate to vote for!", color = nextcord.Color.red())
    else:
        r = server.vote(ctx.author.id, arg)
        if r["error"] == True: embed_color = nextcord.Color.red()
        else: embed_color = nextcord.Color.green()
        embed = nextcord.Embed(title = r["header"], description = r["content"], color = embed_color)

    await ctx.reply(embed = embed)

# ----- Admin commands ----- #
@client.command()
async def admin(ctx, cmd, *, arg):
    admin_role = nextcord.utils.get(ctx.guild.roles, id = 1013316067956891748)
    if admin_role in ctx.author.roles:
        if cmd == "blacklist": # blacklist user
            if arg == None:
                r = server.getblacklist()
            else:
                r = server.blacklist(arg)

        if cmd == "whitelist": # whitelist user
            if arg == None:
                r = server.getwhitelist()
            else:
                r = server.whitelist(arg)

        if cmd == "status": # Change/get bot status
            if arg == None:
                r = server.getstatus()

                embed = nextcord.Embed(title = "Current Status", description = f"My current status is `{r}`", color = nextcord.Color.blurple())
                await ctx.reply(embed = embed)
                return
            else:
                r = server.changestatus(arg)
                await client.change_presence(activity = nextcord.Activity(type = nextcord.ActivityType.watching, name = server.getstatus()))

        # Send back the results
        if r["error"] == True: embed_color = nextcord.Color.red()
        else: embed_color = nextcord.Color.green()
        try:
            embed = nextcord.Embed(title = r["header"], description = r["content"], color = embed_color)
        except:
            embed = nextcord.Embed(title = "idk", description = "tbc", color = nextcord.Color.blurple())
        await ctx.reply(embed = embed)

    else:
        embed = nextcord.Embed(title = "Nice try :smiling_imp:", description = "You don't have the perms to use that command.\nIf this is a mistake, contact an admiral or try again.", color = nextcord.Color.red())
        await ctx.reply(embed = embed)

client.run(CLIENT_TOKEN)