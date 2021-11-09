import websocket

def is_online(url):
    try:
        websocket.create_connection(url).close()
        return True
    except websocket._exceptions.WebSocketBadStatusException:
        return False

def check_servers():
    servers = ['wss://duelingnexus.com/lobby/', 'wss://eu.duelingnexus.com/gameserver/', 'wss://na.duelingnexus.com/gameserver/']

    return [is_online(server) for server in servers]

def status_message(servers):
    statuses = []

    for server in servers:
        if server:
            statuses.append('Online :green_circle:')
        else:
            statuses.append('Offline :red_circle:')

    return statuses
