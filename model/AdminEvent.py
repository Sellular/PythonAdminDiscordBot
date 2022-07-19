class AdminEvent:

    eventID = 0
    userID = ''
    guildID = ''
    submittedUserID = ''
    eventCode = ''
    eventReason = None
    eventTimestamp = ''

    def __init__(self, eventID, userID, guildID, submittedUserID, eventCode, eventReason, eventTimestamp):
        self.eventID = eventID
        self.userID = userID
        self.guildID = guildID
        self.submittedUserID = submittedUserID
        self.eventCode = eventCode
        self.eventReason = eventReason
        self.eventTimestamp = eventTimestamp