import cardsearch
import constants
import punishment
import roles
import serverstatus
from embed import decorate_embed
from parser import get_cards

import datetime
import os
import json
import re

import discord
from discord.ext import tasks

class Bot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.update_server_status.start()
        self.card_update.start()
        self.unarchive_threads.start()
        self.remove_ad_optout.start()

        self.remove_minor.start()
        self.rollover.start()
        self.major3.start()

    async def on_ready(self):
        print('Logged in as', self.user, '[Task]')

    #################
    # Server Status #
    #################

    @tasks.loop(minutes=10)
    async def update_server_status(self):
        with open('last_server_status') as last_server_status_file:
            last_statuses = eval(last_server_status_file.read().strip())

        statuses = serverstatus.check_servers()

        if last_statuses != statuses:
            statuses_str = serverstatus.status_message(statuses)

            message = '**Lobby Server:** {}\n\n**EU Duel Server:** {}\n\n**NA Duel Server:** {}'.format(statuses_str[0], statuses_str[1], statuses_str[2])

            channel = self.get_channel(constants.SERVER_STATUS_CHANNEL)
            await channel.purge()
            message = await channel.send(message)
            await message.publish()

            with open('last_server_status', 'w') as last_server_status_file:
                last_server_status_file.write(str(statuses))

    @update_server_status.before_loop
    async def before_update_server_status(self):
        await self.wait_until_ready()

    #################
    # Card Releases #
    #################

    @tasks.loop(hours=1)
    async def card_update(self):
        cg_cards, rush_cards = get_cards()
        channel = self.get_channel(constants.PATCH_NOTES_CHANNEL)

        if cg_cards or rush_cards:
            await channel.send('@everyone')

        while len(cg_cards):
            cards_tosend = None

            if len(cg_cards) <= constants.NUM_CARDS:
                cards_tosend = cg_cards
                cg_cards = []
            else:
                cards_tosend = cg_cards[:constants.NUM_CARDS]
                cg_cards = cg_cards[constants.NUM_CARDS:]

            cg_cards_embed = discord.Embed(colour=discord.Colour.purple(), description=''.join(sorted(['{}\n'.format(card) for card in cards_tosend])))
            cg_cards_embed.set_author(icon_url='https://cdn.discordapp.com/attachments/557420699191476227/895029003667251240/CG_Icon.png', name='New TCG/OCG Card Releases')
            decorate_embed(cg_cards_embed)

            message = await channel.send(embed=cg_cards_embed)
            await message.publish()

            with open('last_cg_card', 'w') as last_cg_card_file:
                last_cg_card_file.write(cards_tosend[-1])
        while len(rush_cards):
            cards_tosend = None

            if len(rush_cards) <= constants.NUM_CARDS:
                cards_tosend = rush_cards
                rush_cards = []
            else:
                cards_tosend = rush_cards[:constants.NUM_CARDS]
                rush_cards = rush_cards[constants.NUM_CARDS:]

            rush_cards_embed = discord.Embed(colour=discord.Colour.red(), description=''.join(sorted(['{}\n'.format(card) for card in cards_tosend])))
            rush_cards_embed.set_author(icon_url='https://cdn.discordapp.com/attachments/557420699191476227/895010641260191804/Rush_Icon.png', name='New Rush Card Releases')
            decorate_embed(rush_cards_embed)

            message = await channel.send(embed=rush_cards_embed)
            await message.publish()

            with open('last_rush_card', 'w') as last_rush_card_file:
                last_rush_card_file.write(cards_tosend[-1])

    @card_update.before_loop
    async def before_card_update(self):
        await self.wait_until_ready()

    ################################
    # Manage 'Opt Out Of Ads' Role #
    ################################

    @tasks.loop(hours=24)
    async def remove_ad_optout(self):
        for member in self.get_all_members():
            member_roles = roles.roles_tostring(member.roles)

            if 'Opt Out Of Ads' in member_roles and 'Nitro Booster' not in member_roles and 'Ko-Fi Subscriber' not in member_roles:
                await member.remove_roles(roles.get_role('Opt Out Of Ads', member.roles), reason='Not a Nitro Booster or a Ko-Fi Subscriber')

                channel = self.get_channel(constants.ADMIN_LOGS_CHANNEL)
                await channel.send('Removed `@Opt Out Of Ads` from <@{}>'.format(member.id))

    @remove_ad_optout.before_loop
    async def before_remove_ad_optout(self):
        await self.wait_until_ready()

    ######################
    # Unarchive Threads  #
    ######################

    @tasks.loop(hours=1)
    async def unarchive_threads(self):
        channels = [constants.KNOWN_BUGS_CHANNEL, constants.SERVER_GUIDE_CHANNEL, constants.STAFF_INFO_CHANNEL, constants.AD_CHANNEL, constants.LOUNGE_CHANNEL]

        for channel in channels:
            threads = self.get_channel(channel).archived_threads()

            async for thread in threads:
                await thread.edit(archived=False)

    @unarchive_threads.before_loop
    async def before_unarchive_threads(self):
        await self.wait_until_ready()

    #################
    # Strike System #
    #################

    @tasks.loop(seconds=1)
    async def remove_minor(self):
        punishment.remove_minor()

    @remove_minor.before_loop
    async def before_remove_minor(self):
        await self.wait_until_ready()

    @tasks.loop(seconds=1)
    async def rollover(self):
        muteids = punishment.minor3()
        server = self.guilds[0]

        for muteid in muteids:
            await server.fetch_member(muteid).add_roles(roles.get_role('Mute', server.roles), reason='3 Minor Strikes')

            channel = self.get_channel(557420699191476227)
            await channel.send(f'<@{muteid}>\nMuted for 3 Minor Strikes')

        punishment.rollover()

    @rollover.before_loop
    async def before_rollover(self):
        await self.wait_until_ready()

    @tasks.loop(seconds=1)
    async def major3(self):
        banids = punishment.major3()

        for banid in banids:
            channel = self.get_channel(557420699191476227)
            await channel.send(f'<@{banid}>\nBanned for 3 Major Strikes')

    @major3.before_loop
    async def before_major3(self):
        await self.wait_until_ready()

    ###################
    # Handle Messages #
    ###################

    async def on_message(self, message):
        if message.author == self.user:
            return

        if isinstance(message.channel, discord.DMChannel):
            return

        ##################
        # Scam Detection #
        ##################

        '''
        - Edit message
        '''
        if ( isinstance(message.author, discord.User) or not any([roles.isTrainee(message.author), roles.isStaff(message.author), roles.isMod(message.author)]) ) and 'nitro' in message.content.lower() and re.findall(r'https?:\/\/', message.content.lower()):
            channel = self.get_channel(constants.ADMIN_LOGS_CHANNEL)
            await channel.send('<@{}> Banned for scam\n\n```{}```\n**Channel:** <#{}>'.format(message.author.id, message.content, message.channel.id))

            await self.guilds[0].ban(discord.Object(message.author.id), delete_message_days=7, reason='Scam')

        ###############
        # Card Search #
        ###############

        elif message.content.startswith('{') and message.content.endswith('}'):
            cardname = message.content[1:-1]

            if cardname:
                embed = cardsearch.dispatch(cardname)

                if embed:
                    await message.channel.send(embed=embed)
                else:
                    await message.add_reaction('❌')
