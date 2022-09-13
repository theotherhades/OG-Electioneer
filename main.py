import nextcord
import server
import datetime
import os
from nextcord.ext import commands, tasks

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
log_channel = 1014449804136423474

# ----- Events ----- #
@client.event
async def on_ready():
    print("bot online!")
    await client.change_presence(activity = nextcord.Activity(type = nextcord.ActivityType.watching, name = server.getstatus()))

    # Waking server message
    embed = nextcord.Embed(title = ":sleeping: Waking server, please wait", description = "This may take a few seconds", color = nextcord.Color.blurple())
    await client.get_channel(log_channel).send(embed = embed)
    server_ping = server.ping()

    if server_ping == "success":
        embed = nextcord.Embed(title = ":white_check_mark: Server woke successfully", color = nextcord.Color.green())
    else:
        embed = nextcord.Embed(title = ":no_entry: Server failed to wake", description = server_ping, color = nextcord.Color.red())
    await client.get_channel(log_channel).send(embed = embed)

@client.event
async def on_message(message):
    reaction_phrases = {
        # People
        "drako": "😎",
        "solo": "<:pepe_ez~1:925650217464918056>",
        "novo": "⚡",
        "naeem": "😍",
        "sandwich": "🥪",

        # A
        "afghanistan": "🇦🇫",
        "albania": "🇦🇱",
        "algeria": "🇩🇿",
        "andorra": "🇦🇩",
        "angola": "🇦🇴",
        "antigua and barbuda": "🇦🇬",
        "argentina": "🇦🇷",
        "armenia": "🇦🇲",
        "australia": "🇦🇺",
        "austria": "🇦🇹",
        "azerbaijan": "🇦🇿",

        # B
        "bahamas": "🇧🇸",
        "bahrain": "🇧🇭",
        "bangladesh": "🇧🇩",
        "barbados": "🇧🇧",
        "belarus": "🇧🇾",
        "belgium": "🇧🇪",
        "belize": "🇧🇿",
        "benin": "🇧🇯",
        "bhutan": "🇧🇹",
        "bolivia": "🇧🇴",
        "bosnia and herzegovina": "🇧🇦",
        "botswana": "🇧🇼",
        "brazil": "🇧🇷",
        "bulgaria": "🇧🇬",
        "burkina faso": "🇧🇫",
        "burundi": "🇧🇮",

        # C
        "cabo verde": "🇨🇻",
        "cambodia": "🇰🇭",
        "cameroon": "🇨🇲",
        "canada": "🇨🇦",
        "central african republic": "🇨🇫",
        "chad": "🇹🇩",
        "chile": "🇨🇱",
        "china": "🇨🇳",
        "colombia": "🇨🇴",
        "comoros": "🇰🇲",
        "congo": "🇨🇬",
        "democratic republic of the congo": "🇨🇩",
        "costa rica": "🇨🇷",
        "côte d'ivoire": "🇨🇮",
        "ivory coast": "🇨🇮",
        "croatia": "🇭🇷",
        "cuba": "🇨🇺",
        "cyprus": "🇨🇾",
        "czechia": "🇨🇿",
        "czech republic": "🇨🇿",

        # D
        "denmark": "🇩🇰",
        "djibouti": "🇩🇯",
        "dominica": "🇩🇲",
        "dominican republic": "🇩🇴",
        
        # E
        "ecuador": "🇪🇨",
        "egypt": "🇪🇬",
        "el salvador": "🇸🇻",
        "equatorial guinea": "🇬🇶",
        "eritrea": "🇪🇷",
        "estonia": "🇪🇪",
        "eswatini": "🇸🇿",
        "ethiopia": "🇪🇹",

        # F
        "fiji": "🇫🇯",
        "finland": "🇫🇮",
        "france": "🇫🇷",
        
        # G
        "gabon": "🇬🇦",
        "gambia": "🇬🇲",
        "georgia": "🇬🇪",
        "germany": "🇩🇪",
        "ghana": "🇬🇭",
        "greece": "🇬🇷",
        "grenada": "🇬🇩",
        "guatemala": "🇬🇹",
        "guinea": "🇬🇳",
        "guinea-bissau": "🇬🇼",
        "guyana": "🇬🇾",

        # H
        "haiti": "🇭🇹",
        "honduras": "🇭🇳",
        "hungary": "🇭🇺",

        # M
        "madagascar": "🇲🇬",
        "moldova": "🇲🇩",

        # N
        "namibia": "🇳🇦",
        "nauru": "🇳🇷",
        "nepal": "🇳🇵",
        "netherlands": "🇳🇱",
        "new zealand": "🇳🇿",
        "nicaragua": "🇳🇮",
        "niger": "🇳🇪",
        "nigeria": "🇳🇬",
        "north korea": "🇰🇵",
        "north macedonia": "🇲🇰",
        "norway": "🇳🇴",

        # O
        "oman": "🇴🇲",

        # P
        "pakistan": "🇵🇰",
        "palau": "🇵🇼",
        "panama": "🇵🇦",
        "papua new guinea": "🇵🇬",
        "paraguay": "🇵🇾",
        "peru": "🇵🇪",
        "philippines": "🇵🇭",
        "poland": "🇵🇱",
        "portugal": "🇵🇹",
        
        # Q
        "qatar": "🇶🇦",

        # R
        "romania": "🇷🇴",
        "russia": "🇷🇺",
        "rwanda": "🇷🇼",

        # S
        "st kitts and nevis": "🇰🇳",
        "st lucia": "🇱🇨",
        "st vincent and the grenadines": "🇻🇨",
        "samoa": "🇼🇸",
        "san marino": "🇸🇲",
        "sao tome and principe": "🇸🇹",
        "saudi arabia": "🇸🇦",
        "senegal": "🇸🇳",
        "serbia": "🇷🇸",
        "seychelles": "🇸🇨",
        "sierra leone": "🇸🇱",
        "singapore": "🇸🇬",
        "slovakia": "🇸🇰",
        "slovenia": "🇸🇮",
        "solomon islands": "🇸🇧",
        "somalia": "🇸🇴",
        "south africa": "🇿🇦",
        "south korea": "🇰🇷",
        "south sudan": "🇸🇸",
        "spain": "🇪🇸",
        "sri lanka": "🇱🇰",
        "sudan": "🇸🇩",
        "suriname": "🇸🇷",
        "sweden": "🇸🇪",
        "switzerland": "🇨🇭",
        "syria": "🇸🇾",

        # T
        "tajikistan": "🇹🇯",
        "tanzania": "🇹🇿",
        "thailand": "🇹🇭",
        "timor leste": "🇹🇱",
        "togo": "🇹🇬",
        "tonga": "🇹🇴",
        "trinidad and tobago": "🇹🇹",
        "tunisia": "🇹🇳",
        "turkiye": "🇹🇷",
        "turkmenistan": "🇹🇲",
        "tuvalu": "🇹🇻",
        
        # U
        "uganda": "🇺🇬",
        "ukraine": "🇺🇦",
        "united arab emirates": "🇦🇪",
        "uae": "🇦🇪",
        "united kingdom": "🇬🇧",
        "uk": "🇬🇧",
        "united states of america": "🇺🇸",
        "usa": "🇺🇸",
        "uruguay": "🇺🇾",
        "uzbekistan": "🇺🇿",

        # V
        "vanuatu": "🇻🇺",
        "vatican": "🇻🇦",
        "venezuela": "🇻🇪",
        "vietnam": "🇻🇳",

        # Y
        "yemen": "🇾🇪",
        
        # Z
        "zambia": "🇿🇲",
        "zimbabwe": "🇿🇼",
    }

    for phrase in reaction_phrases.keys():
        if (message.content.lower() == phrase) or (f" {phrase} " in message.content.lower()) or (message.content.lower().startswith(phrase)) or (message.content.lower().endswith(f" {phrase}")): 
            await message.add_reaction(reaction_phrases[phrase])
    
    await client.process_commands(message)

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
        if (nextcord.utils.get(ctx.guild.roles, id = 961997055507714088) in ctx.author.roles) or (nextcord.utils.get(ctx.guild.roles, id = 1011815110429397072) in ctx.author.roles):
            embed = nextcord.Embed(title = "Registration failed", description = "You failed to meet the requirements to vote. If this is a mistake, try again or contact an admiral.", color = nextcord.Color.red())
            await ctx.reply(embed = embed)
            return
            
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

    if r["error"] == False:
        log_embed = nextcord.Embed(title = "Vote log", description = f"A vote was cast for `{arg}`. More details below.")
        log_embed.add_field(name = "Vote cast by", value = ctx.author.mention)
        log_embed.add_field(name = "User ID", value = ctx.author.id)
        log_embed.add_field(name = "Vote cast for", value = f"`{arg}`")
        await client.get_channel(log_channel).send(embed = log_embed)

# ----- Admin commands ----- #
@client.command()
async def admin(ctx, cmd, *, arg = ""):
    admin_roles = [
        nextcord.utils.get(ctx.guild.roles, id = 1013316067956891748), # dev server
        nextcord.utils.get(ctx.guild.roles, id = 925636478850195517), # vice
        nextcord.utils.get(ctx.guild.roles, id = 930302959668056135), # admiral
        nextcord.utils.get(ctx.guild.roles, id = 949071726392778843), # coleader
        nextcord.utils.get(ctx.guild.roles, id = 997799134557913129), # grand admiral
        nextcord.utils.get(ctx.guild.roles, id = 925640681425338378) # supreme founder
    ]
    for i in admin_roles:
        if i in ctx.author.roles:
            has_perms = True
            break
    else:
        has_perms = False

    if has_perms == True:
        if cmd == "blacklist": # blacklist user
            if arg == "":
                r = server.getblacklist()
            else:
                r = server.blacklist(arg)

        if cmd == "whitelist": # whitelist user
            if arg == "":
                r = server.getwhitelist()
            else:
                r = server.whitelist(arg)

        if cmd == "status": # Change/get bot status
            if arg == "":
                r = server.getstatus()

                embed = nextcord.Embed(title = "Current Status", description = f"My current status is `{r}`", color = nextcord.Color.blurple())
                await ctx.reply(embed = embed)
                return
            else:
                r = server.changestatus(arg)
                await client.change_presence(activity = nextcord.Activity(type = nextcord.ActivityType.watching, name = server.getstatus()))

        if cmd == "open":
            r = server.open()
        
        if cmd == "close":
            r = server.close()

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