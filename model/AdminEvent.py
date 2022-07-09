class AdminEvent:

    id = 0
    userID = ''
    guildID = ''
    eventCode = ''
    eventReason = None
    eventTimestamp = ''

    def __init__(self, id, userID, guildID, eventCode, eventReason, eventTimestamp):
        self.id = id
        self.userID = userID
        self.guildID = guildID
        self.eventCode = eventCode
        self.eventReason = eventReason
        self.eventTimestamp = eventTimestamp