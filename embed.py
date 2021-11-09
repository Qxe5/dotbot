import datetime

def decorate_embed(embed):
    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/557420699191476227/895266877918556180/Logo_Full.png')
    embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/557420699191476227/895005932545773568/square.png', text='Powered by Dueling Nexus • {}'.format(datetime.date.today().strftime('%-d %B %Y')))
