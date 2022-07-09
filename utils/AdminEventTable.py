from distutils.log import error
from utils import DBUtils
from model.AdminEvent import AdminEvent
from psycopg2 import DatabaseError

adminEventInsertSql = """
    INSERT INTO admin_events (
        user_id,
        guild_id,
        event_code, 
        event_reason
    ) VALUES (
        %s,
        %s,
        %s,
        %s
    )
"""

adminEventSelectByUserSql = """
    SELECT *
    FROM admin_events 
    WHERE 
        user_id = %s AND
        guild_id = %s
    ORDER BY event_timestamp
"""

adminEventLimitSelectByUserSql = """
    SELECT *
    FROM (
        SELECT *
        FROM admin_events
        WHERE 
            user_id = %s AND
            guild_id = %s
        ORDER BY event_timestamp DESC
        LIMIT %s
    ) AS reversed
    ORDER BY event_timestamp
"""

adminEventSelectByIdSql = """
    SELECT *
    FROM admin_events
    WHERE event_id = %s
    ORDER BY event_timestamp
    FETCH FIRST ROW ONLY
"""

def insert(userID, guildID, eventCode, reason = None):
    dbConnection = DBUtils.getDBConnection()
    try:
        dbCursor = dbConnection.cursor()

        dbCursor.execute(adminEventInsertSql, (userID, guildID, eventCode, reason))

        dbConnection.commit()
        dbCursor.close()
    except (Exception, DatabaseError) as error:
        print(error)
        raise error
    finally:
        if dbConnection is not None:
            dbConnection.close()

def getEventById(id):
    dbConnection = DBUtils.getDBConnection()
    try:
        dbCursor = dbConnection.cursor()
        dbCursor.execute(adminEventSelectByIdSql, (id))

        row = dbCursor.fetchone()
        userEvent = None

        if row is not None:
            userEvent = AdminEvent(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5]
            )

        dbCursor.close()

        return userEvent
    except (Exception, DatabaseError) as error:
        print(error)
        raise error
    finally:
        if dbConnection is not None:
            dbConnection.close()

def getEventsByUserAndGuild(userID, guildID, limit):
    dbConnection = DBUtils.getDBConnection()
    try:
        dbCursor = dbConnection.cursor()
        
        if limit is not None:
            dbCursor.execute(adminEventLimitSelectByUserSql, (userID, guildID, limit))
        else:
            dbCursor.execute(adminEventSelectByUserSql, (userID, guildID))
        row = dbCursor.fetchone()

        userEvents = []
        while row is not None:
            userEvents.append(AdminEvent(
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5]
            ))
            row = dbCursor.fetchone()

        dbCursor.close()
        
        return userEvents
    except (Exception, DatabaseError) as error:
        print(error)
        raise error
    finally:
        if dbConnection is not None:
            dbConnection.close()

def formatEventToEmbedParms(event):
    eventParms = {
        "name": '',
        "value": '',
        "reason": ''
    }

    if (event.eventCode == 'WARN'):
        eventParms["name"] = "Warned"
    elif (event.eventCode == 'BAN'):
        eventParms["name"] = "Banned"
    elif (event.eventCode == 'KICK'):
        eventParms["name"] = "Kicked"
    elif (event.eventCode == 'MUTE'):
        eventParms["name"] = "Muted"

    eventParms["timestamp"] = event.eventTimestamp
    eventParms["reason"] = event.eventReason
    return eventParms