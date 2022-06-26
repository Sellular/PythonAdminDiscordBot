from utils.DBUtils import DBUtils
from data.AdminEvent import AdminEvent
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
    SELECT 
        event_code,
        event_reason, 
        event_timestamp 
    FROM admin_events 
    WHERE 
        user_id = %s AND
        guild_id = %s
    ORDER BY event_timestamp
"""

class AdminEventTable:

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

    def getUserEvents(userID, guildID):
        dbConnection = DBUtils.getDBConnection()
        try:
            dbCursor = dbConnection.cursor()
            
            dbCursor.execute(adminEventSelectByUserSql, (userID, guildID))
            row = dbCursor.fetchone()

            userEvents = []
            while row is not None:
                userEvents.append(AdminEvent(
                    userID,
                    guildID,
                    row[0],
                    row[1],
                    row[2]
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