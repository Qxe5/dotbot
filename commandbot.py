import constants
import punishment
import roles
from embed import decorate_embed
from leaderboard import get_leaderboard

import random

import discord
from discord.ext import commands

command_bot = commands.Bot('!')

@command_bot.event
async def on_ready():
    print('Logged in as', command_bot.user, '[Command]')

class Staff(commands.Cog):
    # !mute, !ban
    # cant punish staff
    # Apply roles

    def check_quote(ctx):
        return '"' in ctx.message.content

    def handle(self, error):
        if isinstance(error, commands.CheckFailure):
            return 'You forgot to quote your reason or give a reason'
        else:
            return error

    @commands.command()
    @commands.guild_only()
    @commands.has_role('Server Staff')
    @commands.check(check_quote)
    async def minor(self, ctx, memberid : int, reason : str):
        punishment.minor(memberid)
        punishment.log(memberid, 'Minor Strike', reason, ctx.message.author.id)
        await ctx.message.add_reaction('✅')

    @minor.error
    async def minor_error(self, ctx, error):
        await ctx.send(self.handle(error))

    @commands.command()
    @commands.guild_only()
    @commands.has_role('Server Staff')
    @commands.check(check_quote)
    async def major(self, ctx, memberid : int, reason : str):
        punishment.major(memberid)
        punishment.log(memberid, 'Major Strike', reason, ctx.message.author.id)
        await ctx.message.add_reaction('✅')

    @major.error
    async def major_error(self, ctx, error):
        await ctx.send(self.handle(error))

    @commands.command()
    @commands.guild_only()
    @commands.has_role('Server Staff')
    @commands.check(check_quote)
    async def mute(self, ctx, memberid : int, period : int, reason: str):
        member = await ctx.guild.fetch_member(memberid)
        await member.add_roles(roles.get_role('Mute', ctx.guild.roles), reason=f'{command_bot.command_prefix}mute')

        punishment.mute(memberid, period)
        punishment.log(memberid, f'{period}h Mute', reason, ctx.message.author.id)
        await ctx.message.add_reaction('✅')

    @mute.error
    async def mute_error(self, ctx, error):
        await ctx.send(self.handle(error))

    @commands.command()
    @commands.guild_only()
    @commands.has_role('Server Staff')
    async def strikes(self, ctx, memberid : int):
        await ctx.send(punishment.strikes(memberid))

    @strikes.error
    async def strikes_error(self, ctx, error):
        await ctx.send(error)

class Nexus(commands.Cog):
    @commands.command()
    @commands.guild_only()
    async def leaderboard(self, ctx, page : int):
        '''Get the top 100 ranked players

        <page> is 1-10
        '''

        leaderboard_embed = discord.Embed(colour=discord.Colour.purple(), description=get_leaderboard(page))
        leaderboard_embed.set_author(icon_url='https://cdn.discordapp.com/attachments/557420699191476227/896365274918445106/ladder-icon-vector-sign-symbol-isolated-white-background-logo-concept-your-web-mobile-app-design-134.jpg', name='Leaderboard')
        decorate_embed(leaderboard_embed)

        await ctx.send(embed=leaderboard_embed)

    @leaderboard.error
    async def leaderboard_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'Missing page number. See {command_bot.command_prefix}help')

class FAQ(commands.Cog):
    @commands.command()
    @commands.guild_only()
    async def when(self, ctx):
        '''Answer "When will X card be added?"'''

        answer_embed = discord.Embed(colour=discord.Colour.purple())
        answer_embed.add_field(name='Q: When will [Insert Card Name Here] be added into the game?', value='**A:** Dueling Nexus does not currently update on a consistent schedule. It is unknown when new cards will be added. Generally, after being announced, a scripter will make the card within a week, and so long as it\'s made it should be added into the game whenever an update occurs. You can check <#{}> for the latest game updates, which will include a list of new cards added with every update.'.format(constants.PATCH_NOTES_CHANNEL))
        decorate_embed(answer_embed)

        await ctx.send(embed=answer_embed)

    @commands.command()
    @commands.guild_only()
    async def howreport(self, ctx):
        '''Answer "How can I report a player in-game?"'''

        answer_embed = discord.Embed(colour=discord.Colour.purple())
        answer_embed.add_field(name='Q: How can I report a player in-game?', value='**A:** You cannot. DNX does not have a player reporting system at this time.')
        decorate_embed(answer_embed)

        await ctx.send(embed=answer_embed)

class Fun(commands.Cog):
    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def yuwluv(self, ctx):
        image_urls = ['https://i.pinimg.com/originals/e7/93/b1/e793b19f2d849ac5e386df815b7a8f4c.jpg', 'https://www.nicepng.com/png/detail/603-6030515_honoka-x-maki-love-live-yuri-honomaki.png', 'https://c.tenor.com/BmbTYhCZ5UsAAAAC/yuri-sleeping-yuri-sleep.gif', 'https://images3.alphacoders.com/837/thumb-1920-837981.jpg', 'https://i.pinimg.com/originals/8f/87/2d/8f872dfa19aee8efd8bd5762bd4bd731.jpg', 'https://static.zerochan.net/Love.Live%21.full.1758878.jpg']

        await ctx.send(f'<@{constants.USER_YUW}>')
        await ctx.send(f'{random.choice(image_urls)}')

    @yuwluv.error
    async def yuwluv_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            await ctx.send(f'Only <@{constants.USER_DOT}> can do that <:Reaper:641046300053471233>')

    @commands.command()
    @commands.guild_only()
    async def cute(self, ctx):
        image_urls = ['https://media.discordapp.net/attachments/403731033738182657/858937334136832050/image0.gif', 'https://www.allkpop.com/upload/2019/09/content/280221/1569651690-5.gif', 'https://tenor.com/view/miyeon-cho-miyeon-jo-miyeon-gidle-idle-gif-18962243', 'https://tenor.com/view/miyeon-cho-miyeon-jo-miyeon-gidle-idle-gif-18962146', 'https://tenor.com/view/miyeon-chomiyeon-gif-20083577']

        await ctx.send(random.choice(image_urls))

    @commands.command()
    @commands.guild_only()
    async def getpat(self, ctx):
        '''I give you a pat'''

        await ctx.send('<:KannaHeadpat:580154534488178689>')

    @commands.command()
    @commands.guild_only()
    async def givepat(self, ctx):
        '''You give me a pat'''

        if random.getrandbits(1):
            await ctx.send('^_^')
        else:
            await ctx.send('UwU')

    @commands.command()
    @commands.guild_only()
    async def mine(self, ctx):
        '''Help QQ over Mine'''

        outs = ['Imperial Order', 'Cosmic Cyclone', 'Twin Twisters', 'Heavy Storm Duster', 'Harpie\'s Feather Duster', 'Mystical Space Typhoon', 'Lightning Storm', 'Spiritualism', 'Set Rotation', 'Prohibition', 'Ballista Squad', 'Galaxy Cyclone', 'Evenly Matched', 'Anti-Spell Fragrance', 'Full House', 'Double Cyclone', 'Unending Nightmare', 'Solemn Judgment', 'Cursed Seal of the Forbidden Spell', 'Ojama Trio', 'Dark Hole', 'Torrential Tribute', 'Spell Shattering Arrow', 'Spell Canceller', 'Field Barrier', 'Typhoon', 'Dicephoon', 'Burning Land', 'Magic Deflector', '... and many more']

        embed = discord.Embed(colour=discord.Colour.green(), description=''.join(f'{out}\n' for out in outs))
        embed.set_author(icon_url='https://cdn.discordapp.com/emojis/652241578433445919.png?size=240', name='Outs/Disruption to Mine to help your QQ')
        embed.set_thumbnail(url='https://storage.googleapis.com/ygoprodeck.com/pics_artgame/76375976.jpg')
        embed.set_footer(icon_url='https://cdn.discordapp.com/emojis/755679380705116201.png?size=240', text='Sponsored by Goddess Skuld\'s Oracle™')

        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def lootbox(self, ctx):
        '''Open a lootbox'''

        if ctx.message.author.id == constants.USER_SKY:
            await ctx.send('https://cdn.dribbble.com/users/1112010/screenshots/4559034/lootbox.gif')
        elif ctx.message.author.id == constants.USER_REN:
            await ctx.send('Cute, now put on the dress uwu')
        elif ctx.message.author.id == constants.USER_DOT:
            await ctx.send('Get back to work <:Whip:899655990587297842>')
        else:
            await ctx.send('Give Sky boba to unlock your lootbox <a:DrinkingBoba:733720154676002869>')

    @commands.command()
    @commands.guild_only()
    async def sky(self, ctx):
        await ctx.send('Sky is my master')

    @commands.command()
    @commands.guild_only()
    async def annie(self, ctx):
        await ctx.send('Hands off Annie or Sky literally kills you <:Reaper:641046300053471233>')

    @commands.command()
    @commands.guild_only()
    async def ren(self, ctx):
        await ctx.send('Ren is cute uwu')

    @commands.command()
    @commands.guild_only()
    async def dot(self, ctx):
        await ctx.send('Dot is Sky\'s slave')

    @commands.command()
    @commands.guild_only()
    async def yuw(self, ctx):
        await ctx.send('Cute :heart:')

    @commands.command()
    @commands.guild_only()
    async def moon(self, ctx):
        await ctx.send('Moon is a boomer')

    @commands.command()
    @commands.guild_only()
    async def phoenix(self, ctx):
        await ctx.send('https://www.youtube.com/watch?v=VuNIsY6JdUw')

    @commands.command()
    @commands.guild_only()
    async def sam(self, ctx):
        await ctx.send('Install gentoo')

    @commands.command()
    @commands.guild_only()
    async def ani(self, ctx):
        await ctx.send('🐒')

    @commands.command()
    @commands.guild_only()
    async def timbs(self, ctx):
        await ctx.send('Toy for lesbians')

    @commands.command()
    @commands.guild_only()
    async def luigi(self, ctx):
        await ctx.send('Luigi is baby')

command_bot.add_cog(Staff())
command_bot.add_cog(Nexus())
command_bot.add_cog(FAQ())
command_bot.add_cog(Fun())
