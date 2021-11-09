from embed import decorate_embed

import json
import urllib.parse

import discord
import requests

def get_card_data(cardname):
    return json.loads(requests.get('https://web.duelistsunite.org/omega-api-db/search/{}'.format(urllib.parse.quote(cardname))).text)

def image_link(card):
    if not card['alias']:
        return card['images']['art']
    else:
        return 'https://storage.googleapis.com/ygoprodeck.com/pics_artgame/{}.jpg'.format(card['alias'])

def format_text(text):
    return text.replace('\'\'\'', '**')

def spell_type(card):
    if 'continuous' in card['type']:
        type_icon = 'https://static.wikia.nocookie.net/yugioh/images/7/78/Continuous.png/revision/latest/scale-to-width-down/34?cb=20140609023344'
    elif 'quickplay' in card['type']:
        type_icon = 'https://static.wikia.nocookie.net/yugioh/images/e/eb/Quick-Play.png/revision/latest/scale-to-width-down/34?cb=20140609023554'
    elif 'field' in card['type']:
        type_icon = 'https://static.wikia.nocookie.net/yugioh/images/f/f1/Field.png/revision/latest/scale-to-width-down/34?cb=20140609024006'
    elif 'equip' in card['type']:
        type_icon = 'https://static.wikia.nocookie.net/yugioh/images/5/56/Equip.png/revision/latest/scale-to-width-down/34?cb=20140609023741'
    elif 'ritual' in card['type']:
        type_icon = 'https://static.wikia.nocookie.net/yugioh/images/7/70/Ritual.png/revision/latest/scale-to-width-down/34?cb=20140609024036'
    else:
        type_icon = 'https://static.wikia.nocookie.net/yugioh/images/0/01/Normal.svg/revision/latest/scale-to-width-down/34?cb=20120920120539'

    return type_icon

def trap_type(card):
    if 'continuous' in card['type']:
        type_icon = 'https://static.wikia.nocookie.net/yugioh/images/7/78/Continuous.png/revision/latest/scale-to-width-down/34?cb=20140609023344'
    elif 'counter' in card['type']:
        type_icon = 'https://static.wikia.nocookie.net/yugioh/images/c/cc/Counter.png/revision/latest/scale-to-width-down/34?cb=20140609024545'
    else:
        type_icon = 'https://static.wikia.nocookie.net/yugioh/images/0/01/Normal.svg/revision/latest/scale-to-width-down/34?cb=20120920120539'

    return type_icon

def st_embed(colour, type_icon, cardname, art, effect, subtype_icon, id):
    embed = discord.Embed(colour=colour)

    embed.set_author(icon_url=type_icon, name=cardname)
    embed.set_thumbnail(url=art)
    embed.add_field(name='Effect', value=effect)
    embed.set_footer(icon_url=subtype_icon, text=str(id))

    return embed

def dispatch(cardname):
    # illegals + other formats
    # DL skills
    # Endymion, the Mighty Master of Magic - strip comma

    card = get_card_data(cardname)['data'][cardname]

    if card:
        if 'monster' in card['type']:
            pass
        elif 'spell' in card['type']:
            return st_embed(discord.Colour.green(), 'https://static.wikia.nocookie.net/yugioh/images/0/09/SPELL.svg/revision/latest/scale-to-width-down/300?cb=20120918121429', card['text']['en']['name'], image_link(card), format_text(card['text']['en']['desc']), spell_type(card), card['id'])
        elif 'trap' in card['type']:
            return st_embed(discord.Colour.purple(), 'https://static.wikia.nocookie.net/yugioh/images/2/28/TRAP.svg/revision/latest/scale-to-width-down/300?cb=20120918121520', card['text']['en']['name'], image_link(card), format_text(card['text']['en']['desc']), trap_type(card), card['id'])
