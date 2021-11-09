import math
import sqlite3
import time

import constants

def connectdb():
    connection = sqlite3.connect(constants.STRIKES_DB_FILENAME)

    return (connection, connection.cursor())

def closedb(connection):
    connection.commit()
    connection.close()

###########
# Actions #
###########

def minor(id):
    connection, cursor = connectdb()

    cursor.execute(f'SELECT minors,tally FROM users WHERE id={id}')
    tuple = cursor.fetchone()

    if tuple is None:
        cursor.execute(f'INSERT INTO users VALUES ({id}, 1, 0, 1, 0, {math.floor(time.time())})')
    else:
        minors, tally = tuple

        cursor.execute(f'UPDATE users SET minors={minors + 1},tally={tally + 1},timestamp={math.floor(time.time())} WHERE id={id}')

    closedb(connection)

def major(id):
    connection, cursor = connectdb()

    cursor.execute(f'SELECT majors,tally FROM users WHERE id={id}')
    tuple = cursor.fetchone()

    if tuple is None:
        cursor.execute(f'INSERT INTO users VALUES ({id}, 0, 1, 1, 0, {math.floor(time.time())})')
    else:
        majors, tally = tuple

        cursor.execute(f'UPDATE users SET majors={majors + 1},tally={tally + 1},timestamp={math.floor(time.time())} WHERE id={id}')

    closedb(connection)

def mute(id, period):
    connection, cursor = connectdb()

    cursor.execute(f'SELECT mute FROM users WHERE id={id}')
    tuple = cursor.fetchone()

    if tuple is None:
        cursor.execute(f'INSERT INTO users VALUES ({id}, 0, 0, 0, {period}, {math.floor(time.time())})')
    else:
        mute = tuple[0]

        cursor.execute(f'UPDATE users SET mute={mute + period},timestamp={math.floor(time.time())} WHERE id={id}')

    closedb(connection)

def log(id, punishment, reason, issuer):
    connection, cursor = connectdb()

    cursor.execute(f'INSERT INTO reasons(userid, punishment, reason, issuer) VALUES(?, ?, ?, ?)', [id, punishment, reason, issuer])

    closedb(connection)

#########
# Loops #
#########

def remove_minor():
    connection, cursor = connectdb()

    # Change to 1 week
    week_ago = math.floor(time.time()) - 60

    cursor.execute(f'SELECT id,minors FROM users WHERE minors >= 1 AND timestamp <= {week_ago}')

    for id, minors in cursor.fetchall():
        cursor.execute(f'UPDATE users SET minors={minors - 1},timestamp={math.floor(time.time())} WHERE id={id}')

    closedb(connection)

def rollover():
    connection, cursor = connectdb()

    cursor.execute('SELECT id,minors,majors,tally FROM users WHERE minors=3 OR tally=3')
    tuples = cursor.fetchall()

    for id, minors, majors, tally in tuples:
        majors += minors // 3
        majors += tally // 3
        majors = min(majors, 3)

        minors %= 3
        tally %= 3

        cursor.execute(f'UPDATE users SET minors={minors},majors={majors},tally={tally} WHERE id={id}')

    closedb(connection)

def minor3():
    connection, cursor = connectdb()

    cursor.execute('SELECT id FROM users WHERE minors=3')
    muteids = [tuple[0] for tuple in cursor.fetchall()]

    closedb(connection)

    return muteids

def major3():
    connection, cursor = connectdb()

    cursor.execute('SELECT id FROM users WHERE majors=3')
    banids = [tuple[0] for tuple in cursor.fetchall()]

    for banid in banids:
        cursor.execute(f'DELETE FROM users WHERE id={banid}')

    closedb(connection)

    return banids

#########
# Query #
#########

def strikes(id):
    connection, cursor = connectdb()

    cursor.execute(f'SELECT minors,majors FROM users WHERE id={id}')
    tuple = cursor.fetchone()

    if tuple is None:
        return f'<@{id}> has no strikes'
    else:
        minors, majors = tuple

        output = f'<@{id}>\n**Minor Strikes:** {minors}\n**Major Strikes:** {majors}\n\n**Log:**\n'

        cursor.execute(f'SELECT punishment,reason,issuer FROM reasons WHERE userid={id}')

        for punishment, reason, issuer in cursor.fetchall():
            output += f'- {punishment} for `{reason}` by <@{issuer}>\n'

    closedb(connection)

    return output
