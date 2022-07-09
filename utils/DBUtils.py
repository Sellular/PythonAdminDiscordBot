from configparser import ConfigParser
import psycopg2

adminEventTableSql = """
    CREATE TABLE IF NOT EXISTS admin_events (
        event_id        INT         GENERATED ALWAYS AS IDENTITY,
        user_id         TEXT        NOT NULL,
        guild_id        TEXT        NOT NULL,
        event_code      VARCHAR(4)  NOT NULL,
        event_reason    TEXT,
        event_timestamp TIMESTAMP   NOT NULL 
                                    DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY(event_id),
        FOREIGN KEY(event_code) REFERENCES admin_event_codes(event_code)
    );
"""

adminEventCodeTableSql = """
    CREATE TABLE IF NOT EXISTS admin_event_codes (
        event_code          VARCHAR(4)  NOT NULL,
        event_description   TEXT        NOT NULL,

        PRIMARY KEY(event_code)   
    );
"""

adminEventCodeCheckSql = """
    SELECT * FROM admin_event_codes 
    FETCH FIRST ROW ONLY;
"""

adminEventCodeInsertsSql = """
    INSERT INTO admin_event_codes (event_code, event_description)
    VALUES
        ('WARN', 'User warned'),
        ('KICK', 'User kicked'),
        ('BAN', 'User banned'),
        ('MUTE', 'User muted');
"""

def getDBConnection(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    dbConfig = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            dbConfig[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    dbConnection = None

    try:
        dbConnection = psycopg2.connect(**dbConfig)

        return dbConnection
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        if dbConnection is not None:
            dbConnection.close()

def checkTables():
    dbConnection = getDBConnection()

    try:
        dbCursor = dbConnection.cursor()
        tableCommands = (adminEventCodeTableSql, adminEventTableSql)

        for command in tableCommands:
            dbCursor.execute(command)

        dbCursor.execute(adminEventCodeCheckSql)
        checkRow = dbCursor.fetchone()

        if checkRow is None:
            dbCursor.execute(adminEventCodeInsertsSql)

        dbConnection.commit()
        dbCursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise error
    finally:
        if dbConnection is not None:
            dbConnection.close()