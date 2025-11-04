import discord
from discord.ext import commands, tasks
import logging
from dotenv import load_dotenv
import os
import random
from datetime import (datetime)

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.members = True

# Character quotes list - each quote has a character name and their quote
character_quotes = [
    {"character": "Devil", "quote": "No matter what you will believe me!", "image":"https://cdn.discordapp.com/attachments/1434295486046797864/1435391236679925870/ElectionWinnerDevil.png?ex=690bcbc3&is=690a7a43&hm=db0606a88eecda5132f1bec9c735a3b0bb8e7c6e08d2090931551e8ad7474ecc&"},
    {"character": "Random Person", "quote": "What am I doing here?", "image":"https://cdn.discordapp.com/attachments/1434295486046797864/1435391316807909376/ElectionWinnerRP.png?ex=690bcbd6&is=690a7a56&hm=ade58f60a767e1733b1d8fbbc7e348670bfdefb8305cde1f33ca855d804cf09d&"},
    {"character": "Boot", "quote": "This world can be great for both of us, but we have to be great for each other first", "image":"https://cdn.discordapp.com/attachments/1434295486046797864/1435391180186714204/ElectionWinnerBoot.png?ex=690bcbb5&is=690a7a35&hm=e5c17f1888b2d469f624488870bcc970a5f5e8750a32a07d68f03e5306f1a366&"},
    {"character": "Cat", "quote": "*looks at you expectingly*", "image":"https://cdn.discordapp.com/attachments/1434295486046797864/1435391206598119516/ElectionWinnerCat.png?ex=690bcbbb&is=690a7a3b&hm=f038f7bc48cf7d9a16d0bd792187d50c230982c573fdf80f46d497a871bfb660&"},
    {"character": "Dog", "quote": "*begins to talk to you but you realize dogs cant speak*", "image":"https://cdn.discordapp.com/attachments/1434295486046797864/1435391244493783132/ElectionWinnerDog.png?ex=690bcbc4&is=690a7a44&hm=97817bd6ba283c00d4b4c4ef0fa129f4eb8725842eee268bfab1459bda7e7c28&"},
    {"character": "Chaos", "quote": "You stare towards chaos and realize that chaos is whats best for you", "image":"https://cdn.discordapp.com/attachments/1434295486046797864/1435391218396954656/ElectionWinnerChaos.png?ex=690bcbbe&is=690a7a3e&hm=e6a5301988d646a549a1219f92177bc1170199219f874294bc46fb7eab513458&"},
    {"character": "Headmaster", "quote": "Reading a book is the easiest ways not to be stupid", "image":"https://cdn.discordapp.com/attachments/1434295486046797864/1435391277318537327/ElectionWinnerHeadMaster.png?ex=690bcbcc&is=690a7a4c&hm=305bbe024a605792270ba6b6c07d25c87175b574fcaeef9033dd0bb5e574b694&"},
    {"character": "Queen of Hearts", "quote": "Love tears down most boundaries, but remember to be yourself", "image":"https://cdn.discordapp.com/attachments/1434295486046797864/1435393115610681535/ElectionWinnerKQHearts.png?ex=690bcd83&is=690a7c03&hm=acf2cb8d1369e87137fdb38b9efc012b7b79c7468a2ceb6d58d24b3f6ca2a2e3&"},
    {"character": "Grimes", "quote": "Even those at the bottom can rise when the opportunity presents itself", "image":"https://cdn.discordapp.com/attachments/1434295486046797864/1435391266526466088/ElectionWinnerGrimes.png?ex=690bcbca&is=690a7a4a&hm=0784f8d8eece9c0ee385c49e16e507316a61f054595734665bba49819e5bd248&"},
    {"character": "Brittany", "quote": "Nothing that a diamond cant fix!", "image":"https://cdn.discordapp.com/attachments/1434295486046797864/1435391196246704300/ElectionWinnerBrittany.png?ex=690bcbb9&is=690a7a39&hm=470424396076ba8d7ed736fe16b8c21ceee34d1e2d3ae98bc6970ba055cfa1ee&"},
    {"character": "King of Hearts", "quote": "When we hit our lowest point, we are open to the greatest change.", "image":"https://cdn.discordapp.com/attachments/1434295486046797864/1435393115610681535/ElectionWinnerKQHearts.png?ex=690bcd83&is=690a7c03&hm=acf2cb8d1369e87137fdb38b9efc012b7b79c7468a2ceb6d58d24b3f6ca2a2e3&"},
    {"character": "Corporation", "quote": "Shouldn't you be working?", "image":"https://cdn.discordapp.com/attachments/1434295486046797864/1435391228115030017/ElectionWinnerCorporation.png?ex=690bcbc1&is=690a7a41&hm=9e16c9b1369c304d09e028c4807337e5e22e6535c5284fef8007b9c01012dcdf&"},
    {"character": "Angry Old Man", "quote": "Get off my land", "image":"https://cdn.discordapp.com/attachments/1434295486046797864/1435391169050837012/ElectionWinnerAngryOldMan.png?ex=690bcbb2&is=690a7a32&hm=ab74fd7c9f1e0e2f8a49938b48724f8806a05e5bf6ec9212d81342b094945beb&"},
    {"character": "Farmer", "quote": "Just like people the land need a good foundation to grow", "image":"https://cdn.discordapp.com/attachments/1434295486046797864/1435391256023928872/ElectionWinnerFarmer.png?ex=690bcbc7&is=690a7a47&hm=730056cf86fe9cb0bb430f658c3f1035fdd3832bc674949b67f09605a9893bcc&"},
    {"character": "Old Man", "quote": "You gain nothing from doing nothing", "image":"https://cdn.discordapp.com/attachments/1434295486046797864/1435391307911659550/ElectionWinnerOM.png?ex=690bcbd4&is=690a7a54&hm=3d36d55c29a8ec47b365f85c843887fa804216cd9342cfa495987631d0cb06fa&"},
    {"character": "Man of Peace", "quote": "You must find peace without yourself before you can help others.", "image": "https://cdn.discordapp.com/attachments/1434295486046797864/1435391296910000320/ElectionWinnerMOP.png?ex=690bcbd1&is=690a7a51&hm=9b0453ee1c9bec574180d086655ca1b114a8a59f57506ea63db0e02c42e3bfec&"},
]

# Track which quote to post next
current_quote_index = 0


bot = commands.Bot(command_prefix='!', intents=intents)

# Store faction scores (you can later save this to a database)
faction_scores = {
    1407845702255775864: 100,  # Artificers
    1407845947630686269: 100,  # Charmers
    1407846005147172904: 100,  # Game Masters
    1407846008569729124: 100,  # Realtors
    1407846011535364186: 100,  # TheOutsiders
}

# Store last roll time for each user (user_id: datetime)
last_roll_time = {}

# Cooldown duration in seconds (3 hours = 10,800 seconds)
ROLL_COOLDOWN = 10800  # 3 hours

# Dice events for each faction
dice_events = {
    1407845702255775864: {  # Artificers
        1: ("🔧 Your invention exploded! Lost resources.", -15),
        2: ("⚙️ Minor breakthrough in your workshop.", +5),
        3: ("🛠️ Steady progress on your project.", +10),
        4: ("🔨 Created a useful gadget!", +15),
        5: ("💡 Brilliant innovation!", +20),
        6: ("🚀 REVOLUTIONARY INVENTION! The world is amazed!", +30),
    },
    1407845947630686269: {  # Charmers
        1: ("💔 Your charm offensive backfired!", -15),
        2: ("😊 Made a few new friends.", +5),
        3: ("💬 Pleasant conversation with allies.", +10),
        4: ("💖 Won hearts with your charisma!", +15),
        5: ("✨ Everyone loves you today!", +20),
        6: ("👑 LEGENDARY CHARM! You're irresistible!", +30),
    },
    1407846005147172904: {  # Game Masters
        1: ("🎲 Your game night was a disaster!", -15),
        2: ("🃏 Small tournament went okay.", +5),
        3: ("🎮 Fun gaming session!", +10),
        4: ("🏆 Epic victory in the arena!", +15),
        5: ("🎯 Dominating the competition!", +20),
        6: ("👾 LEGENDARY PLAY! Hall of fame worthy!", +30),
    },
    1407846008569729124: {  # Realtors
        1: ("📉 Property market crashed!", -15),
        2: ("🏠 Made a small sale.", +5),
        3: ("🏘️ Decent property deal closed.", +10),
        4: ("🏢 Sold a premium location!", +15),
        5: ("🏰 Multiple high-value sales!", +20),
        6: ("🌆 MEGA DEAL! Sold an entire district!", +30),
    },
    1407846011535364186: {  # TheOutsiders
        1: ("⚠️ Your plan got exposed!", -15),
        2: ("🌙 Laid low successfully.", +5),
        3: ("🎭 Pulled off a small scheme.", +10),
        4: ("🗡️ Executed a clever plot!", +15),
        5: ("🔥 Chaos spreads in your wake!", +20),
        6: ("💀 LEGENDARY HEIST! Nobody saw it coming!", +30),
    },
}

@bot.event
async def on_ready():
    print('Yall Ready For This?')
    monthly_post.start()
    daily_quote.start()

# Dice roll minigame command
@bot.command(name='roll')
async def roll_dice(ctx):
    """Roll a dice for your faction!"""
    # Check cooldown
    current_time = datetime.now()
    user_id = ctx.author.id

    if user_id in last_roll_time:
        time_since_last_roll = (current_time - last_roll_time[user_id]).total_seconds()
        if time_since_last_roll < ROLL_COOLDOWN:
            time_remaining = ROLL_COOLDOWN - time_since_last_roll
            hours = int(time_remaining // 3600)
            minutes = int((time_remaining % 3600) // 60)
            seconds = int(time_remaining % 60)

            embed = discord.Embed(
                title="⏰ Cooldown Active",
                description=f"You need to wait before rolling again!",
                color=discord.Color.red()
            )
            embed.add_field(
                name="Time Remaining",
                value=f"{hours}h {minutes}m {seconds}s",
                inline=False
            )
            embed.set_footer(text="Come back later to roll again!")
            await ctx.send(embed=embed)
            return

    # Get user's faction roles
    user_faction_role = None
    faction_roles = [1407845702255775864, 1407845947630686269, 1407846005147172904,
                     1407846008569729124, 1407846011535364186]

    for role in ctx.author.roles:
        if role.id in faction_roles:
            user_faction_role = role.id
            break

    if not user_faction_role:
        await ctx.send("❌ You need to be in a faction to play! Choose your faction first.")
        return

    # Roll the dice
    roll = random.randint(1, 6)
    event_text, score_change = dice_events[user_faction_role][roll]

    # Update faction score
    faction_scores[user_faction_role] += score_change
    new_score = faction_scores[user_faction_role]

    # Get faction name
    faction_role = ctx.guild.get_role(user_faction_role)
    faction_name = faction_role.name if faction_role else "Your Faction"

    # Create embed
    embed = discord.Embed(
        title=f"🎲 {ctx.author.display_name} rolled a {roll}!",
        description=event_text,
        color=discord.Color.gold() if score_change > 0 else discord.Color.red(),
        timestamp=datetime.now()
    )

    embed.add_field(name="Score Change", value=f"{'+' if score_change > 0 else ''}{score_change}", inline=True)
    embed.add_field(name=f"{faction_name} Total", value=f"{new_score} points", inline=True)
    embed.set_footer(text=f"Roll again to change your faction's fate!")

    # Add dice emoji based on roll
    dice_emoji = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"][roll - 1]
    embed.set_thumbnail(url=ctx.author.display_avatar.url)

    await ctx.send(f"{dice_emoji}", embed=embed)
    last_roll_time[user_id] = current_time

@bot.command(name='cooldown')
async def check_cooldown(ctx):
    """Check when you can roll again"""

    user_id = ctx.author.id

    if user_id not in last_roll_time:
        await ctx.send("✅ You can roll now! Use `!roll` to play.")
        return

    current_time = datetime.now()
    time_since_last_roll = (current_time - last_roll_time[user_id]).total_seconds()

    if time_since_last_roll >= ROLL_COOLDOWN:
        await ctx.send("✅ You can roll now! Use `!roll` to play.")
    else:
        time_remaining = ROLL_COOLDOWN - time_since_last_roll
        hours = int(time_remaining // 3600)
        minutes = int((time_remaining % 3600) // 60)
        seconds = int(time_remaining % 60)

        embed = discord.Embed(
            title="⏰ Cooldown Status",
            description=f"You rolled recently and need to wait.",
            color=discord.Color.orange()
        )
        embed.add_field(
            name="Time Remaining",
            value=f"{hours}h {minutes}m {seconds}s",
            inline=False
        )
        embed.set_footer(text="Be patient! Good things come to those who wait.")
        await ctx.send(embed=embed)


# Leaderboard command
@bot.command(name='scores')
async def show_scores(ctx):
    """Show all faction scores"""

    embed = discord.Embed(
        title="🏆 Faction Leaderboard",
        description="Current standings in the faction wars!",
        color=discord.Color.purple(),
        timestamp=datetime.now()
    )

    # Sort factions by score
    sorted_factions = sorted(faction_scores.items(), key=lambda x: x[1], reverse=True)

    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]

    for i, (role_id, score) in enumerate(sorted_factions):
        role = ctx.guild.get_role(role_id)
        if role:
            medal = medals[i] if i < len(medals) else "•"
            embed.add_field(
                name=f"{medal} {role.name}",
                value=f"**{score}** points",
                inline=False
            )

    embed.set_footer(text="Use !roll to earn points for your faction!")
    await ctx.send(embed=embed)

## Category Count
@bot.event
async def on_member_update(before, after):
    # Check if roles changed
    if before.roles != after.roles:
        # Update multiple categories
        await update_category_count(after.guild, CATEGORY_ID=1400193884109406360, ROLE_ID=1407845702255775864, BASE_NAME="┗⎯⎯|★Artificers🤓")
        await update_category_count(after.guild, CATEGORY_ID=1400194110048043199, ROLE_ID=1407845947630686269, BASE_NAME="┗⎯⎯|★Charmers😍")
        await update_category_count(after.guild, CATEGORY_ID=1400194614249652374, ROLE_ID=1407846005147172904, BASE_NAME="┗⎯⎯|★Game Masters🥳")
        await update_category_count(after.guild, CATEGORY_ID=1400194733111902278, ROLE_ID=1407846008569729124, BASE_NAME="┗⎯⎯|★Realtors🧐")
        await update_category_count(after.guild, CATEGORY_ID=1401261481101758464, ROLE_ID=1407846011535364186, BASE_NAME="┗⎯⎯|★TheOutsiders😎")

        role_channels = {
            1407845702255775864: 1434085439915950162,  # Role ID: Channel ID
            1407845947630686269: 1434098664414117981,  # Role ID: Channel ID
            1407846005147172904: 1434098786208190545,  # Role ID: Channel ID
            1407846008569729124: 1434098889027223594,
            1407846011535364186: 1434099053741998101,
        }

        role_messages = {
            1407845702255775864: f"🎉 {after.mention} just joined the Artificers! Welcome to the crafters! 🤓",
            1407845947630686269: f"💖 {after.mention} just joined the Charmers! Get ready to spread the love! 😍",
            1407846005147172904: f"🎮 {after.mention} just joined the Game Masters! Let the games begin! 🥳",
            1407846008569729124: f"🏠 {after.mention} just joined the Realtors! Time to make some deals! 🧐",
            1407846011535364186: f"😎 {after.mention} just joined TheOutsiders! Welcome to the crew! 😎",
        }

        # Check each role
        for role_id, channel_id in role_channels.items():
            role = after.guild.get_role(role_id)
            channel = after.guild.get_channel(channel_id)

            # Check if the role was added (not removed)
            if role and channel and role in after.roles and role not in before.roles:
                custom_message = role_messages.get(role_id, f"🎉 {after.mention} just joined the {role.name} role!")
                await channel.send(custom_message)


@bot.event
async def on_member_join(member):
    await update_category_count(member.guild, CATEGORY_ID=1400193884109406360, ROLE_ID=1407845702255775864, BASE_NAME="┗⎯⎯|★Artificers🤓")
    await update_category_count(member.guild, CATEGORY_ID=1400194110048043199, ROLE_ID=1407845947630686269, BASE_NAME="┗⎯⎯|★Charmers😍")
    await update_category_count(member.guild, CATEGORY_ID=1400194614249652374, ROLE_ID=1407846005147172904, BASE_NAME="┗⎯⎯|★Game Masters🥳")
    await update_category_count(member.guild, CATEGORY_ID=1400194733111902278, ROLE_ID=1407846008569729124, BASE_NAME="┗⎯⎯|★Realtors🧐")
    await update_category_count(member.guild, CATEGORY_ID=1401261481101758464, ROLE_ID=1407846011535364186, BASE_NAME="┗⎯⎯|★TheOutsiders😎")



@bot.event
async def on_member_remove(member):
    await update_category_count(member.guild, CATEGORY_ID=1400193884109406360, ROLE_ID=1407845702255775864, BASE_NAME="┗⎯⎯|★Artificers🤓")
    await update_category_count(member.guild, CATEGORY_ID=1400194110048043199, ROLE_ID=1407845947630686269, BASE_NAME="┗⎯⎯|★Charmers😍")
    await update_category_count(member.guild, CATEGORY_ID=1400194614249652374, ROLE_ID=1407846005147172904, BASE_NAME="┗⎯⎯|★Game Masters🥳")
    await update_category_count(member.guild, CATEGORY_ID=1400194733111902278, ROLE_ID=1407846008569729124, BASE_NAME="┗⎯⎯|★Realtors🧐")
    await update_category_count(member.guild, CATEGORY_ID=1401261481101758464, ROLE_ID=1407846011535364186, BASE_NAME="┗⎯⎯|★TheOutsiders😎")


async def update_category_count(guild, CATEGORY_ID, ROLE_ID, BASE_NAME):
    category = guild.get_channel(CATEGORY_ID)
    role = guild.get_role(ROLE_ID)

    if category and role:
        member_count = len(role.members)
        new_name = f"{BASE_NAME}: {member_count}"

        if category.name != new_name:
            await category.edit(name=new_name)



# Monthly picture post task
@tasks.loop(hours=720)  # 720 hours = 30 days
async def monthly_post():
    CHANNEL_ID = 1434281891556626532  # Channel to post in

    # Dictionary of pictures with their custom messages
    pictures = {
        "https://cdn.discordapp.com/attachments/1434295486046797864/1434295968076922947/PresidentialCardCAT.png?ex=6907cfb6&is=69067e36&hm=f51f87d9f9ab2095d3edb113eb5f96694e6717f9237e35c6735c22ebda324a7a&": " The Cat requires to be showered in the gifts they deserve and you oblige! - Jewelry costs skyrocket!",
        "https://cdn.discordapp.com/attachments/1434295486046797864/1434295889995890759/PresidentialCardANGRYOLDMAN.png?ex=6907cfa4&is=69067e24&hm=57b4161ddd61fa3cd2bfa0d08ccb25ec809f256f4e63cfbe2b97a63662573526&": "The Angry Old man takes out his anger on his constituents! - Taxes are raised for all the people! ",
        "https://cdn.discordapp.com/attachments/1434295486046797864/1434295908475994233/PresidentialCardBOOT.png?ex=6907cfa8&is=69067e28&hm=e6cdeafcb9b62addea71bc9b7571f1a7c4d282e08711105b5e64dc507f53f74b&": "Boot creates the ultimate A.I that will keep the world safe for a month! - Carl is relieved of duty for now!",
        "https://cdn.discordapp.com/attachments/1434295486046797864/1434295926431813682/PresidentialCardBrittany.png?ex=6907cfac&is=69067e2c&hm=1afa64757c2740c7cb58eb2d4621c36046c059302f08103fdb477004e512b3fb&": "Brittany believes that everyone deserves to have jewelery, so she is practically giving it away! - Jewelry now pays you! ",
        "https://cdn.discordapp.com/attachments/1434295486046797864/1434295945289400371/PresidentialCardBUSINESSPERSON.png?ex=6907cfb1&is=69067e31&hm=4fdc20a1795fd6b284df05bd8472f8902896b2af3561fac8d5195729edabbaab&": "The Corporation is going to make a quick buck off you! - All Prices Increase and Job Pay Decreases!",
        "https://cdn.discordapp.com/attachments/1434295486046797864/1434296008459948043/PresidentialCardDOG.png?ex=6907cfc0&is=69067e40&hm=c93c5eadf48ce0a2deabfc9eaf6a79064da6683a166395f89d1aa78c22935ad0&": "This good boy just wants a few extra treats here and there! - Food prices increase!",
        "https://cdn.discordapp.com/attachments/1434295486046797864/1434296031624954066/PresidentialCardFARMER.png?ex=6907cfc5&is=69067e45&hm=0da4d1f12586f6330e441b6a300a029b293985f0e05b08f5ec3852ccfe42f547&": "The humble Farmer increase production of food to record number! - Food prices decrease!",
        "https://cdn.discordapp.com/attachments/1434295486046797864/1434296058426429675/PresidentialCardGRIMES.png?ex=6907cfcc&is=69067e4c&hm=ca18a2e5062b11ec8080a61d0c9a94922180853adfa8150aea4a8fcc39a0ee9b&": "Grimes understands the struggles of everyone that tries to work their way from the bottom! - Job Pay increases!",
        "https://cdn.discordapp.com/attachments/1434295486046797864/1434296074935472138/PresidentialCardHEADMASTER.png?ex=6907cfd0&is=69067e50&hm=17e646985aae311bbe3aa6b216fb3a1bbb84637d66bd9bb7f4d01ef4e05764a9&": "The Headmaster believes the first step to building a healthy world, is to first build a healthy mind! - Healthcare costs decrease!",
        "https://cdn.discordapp.com/attachments/1434295486046797864/1434296096590532712/PresidentialCardKINGANDQUEENOFHEARTS.png?ex=6907cfd5&is=69067e55&hm=77ff076971ea80966899500557b169d44c30186fe8ffb7c12463284030a36b46&": "The King and Queen of Hearts are going to make it easier for everyone to spend time with a loved one! - Relax spaces increase!",
        "https://cdn.discordapp.com/attachments/1434295486046797864/1434296130019262554/PresidentialCardNORMALGUY.png?ex=6907cfdd&is=69067e5d&hm=c027d4de3a3426888b409dd195d1bd5e2f4164ab36302a3f98d873ed68a31122&": "This Random Person is just doing the best they can! - Nothing changes!",
        "https://cdn.discordapp.com/attachments/1434295486046797864/1434296157131116676/PresidentialCardOLDMAN.png?ex=6907cfe3&is=69067e63&hm=093f55f804073354a3f6c46eba44ce8911a0ef4c6301ccb6aade0fd8232a9456&": "The Old Man is trying to be hip with the kids, and will decrease the cost to play video games! - Utility costs decrease! ",
        "https://cdn.discordapp.com/attachments/1434295486046797864/1434296191973326919/PresidentialCardTheDevil.png?ex=6907cfec&is=69067e6c&hm=6c8f14fe6576520fb9110c7dc68e6448a428c872ceb3a9745ba8ae89d1c9456e&": "The Devil will keep the world in constant war, distracting you with his cute little dance moves! - This board will not know peace this month",
        "https://cdn.discordapp.com/attachments/1434295486046797864/1434296257588760676/PresidentialCardManOFPEACE.png?ex=6907cffb&is=69067e7b&hm=8e7d33b861f70d1c96987461c146b4473db49f0040face1aa5184d46fc1790bb&": "The Man of Peace just has a vibe about him that makes everyone less hostile! - War will not wage with him around",
        "https://cdn.discordapp.com/attachments/1434295486046797864/1434309369318736056/PresidentialCardCHAOS.png?ex=6907dc31&is=69068ab1&hm=1d8e49a4d4e0d10d0996ee9af350860de56197dd8947e6b1b92ffd3da58ae6da&": "Chaos shows up when you least expect it! - Chaos Tiles show up more often",
    }

    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        # Pick a random picture
        image_url, message = random.choice(list(pictures.items()))

        embed = discord.Embed(
            description=message,
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_image(url=image_url)


        await channel.send(embed=embed)



@monthly_post.before_loop
async def before_monthly_post():
    await bot.wait_until_ready()


@tasks.loop(hours=168)  # Runs every 24 hours
async def daily_quote():
    global current_quote_index

    QUOTE_CHANNEL_ID = 1435365963783606425  # Replace with your desired channel ID

    channel = bot.get_channel(QUOTE_CHANNEL_ID)
    if channel:
        # Get the current quote
        quote_data = character_quotes[current_quote_index]
        character_name = quote_data["character"]
        quote = quote_data["quote"]
        image_url = quote_data["image"]

        embed = discord.Embed(
            title=f"💭 Daily Quote from {character_name}",
            description=f"*\"{quote}\"*",
            color=discord.Color.purple(),
            timestamp=datetime.now()
        )
        embed.set_image(url=image_url)
        embed.set_footer(text=f"- {character_name}")

        await channel.send(embed=embed)

        # Move to next quote, loop back to start if at the end
        current_quote_index = (current_quote_index + 1) % len(character_quotes)


@daily_quote.before_loop
async def before_daily_quote():
    await bot.wait_until_ready()


bot.run(token, log_handler=handler, log_level=logging.DEBUG)