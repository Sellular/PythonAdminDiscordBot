class AdminEvent:

    userID = ''
    guildID = ''
    eventCode = ''
    eventReason = None
    eventTimestamp = ''

    def __init__(self, userID, guildID, eventCode, eventReason, eventTimestamp):
        self.userID = userID
        self.guildID = guildID
        self.eventCode = eventCode
        self.eventReason = eventReason
        self.eventTimestamp = eventTimestamp