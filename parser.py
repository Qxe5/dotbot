import html.parser

import requests

class ChangeLogParser(html.parser.HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = []

    def handle_data(self, data):
        self.data.append(data)

    def get_data(self):
        return self.data

def get_data():
    response = requests.get('https://duelingnexus.com/change_log.php').text

    table = response[response.index('<table id="acp-table">') : response.index('</table>') + len('</table>')]

    parser = ChangeLogParser()
    parser.feed(table)

    return parser.get_data()

def filter_data(data):
    data = [data_point.replace(' has been added!', '') for data_point in data if '\t' not in data_point][4:]
    del data[::4] # Remove Dates
    del data[::3] # Remove IDs

    return data

def split_list(list):
    for i in range(0, len(list), 2):
        yield list[i : i + 2]

def group_data(data):
    data.reverse()

    card_generator = split_list(data)

    cg_cards = []
    rush_cards = []

    for card in card_generator:
        if card[0] == 'New Card' and card[1] not in cg_cards:
            cg_cards.append(card[1])
        elif card[0] == 'New Rush Card' and card[1] not in rush_cards:
            rush_cards.append(card[1])

    return [cg_cards, rush_cards]

def trim_old_data(data):
    cg_cards, rush_cards = data

    with open('last_cg_card') as last_cg_card_file:
        last_cg_card = last_cg_card_file.read().strip()
        cg_cards = cg_cards[cg_cards.index(last_cg_card) : ]
        cg_cards.remove(last_cg_card)
    with open('last_rush_card') as last_rush_card_file:
        last_rush_card = last_rush_card_file.read().strip()
        rush_cards = rush_cards[rush_cards.index(last_rush_card) : ]
        rush_cards.remove(last_rush_card)

    return [cg_cards, rush_cards]

def get_cards():
    return trim_old_data(group_data(filter_data(get_data())))
