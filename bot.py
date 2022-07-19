from utils import DBUtils, SetupUtils, GeneralUtils

DBUtils.checkTables()

bot = SetupUtils.setupBot()
SetupUtils.importCogs(bot)

botConfig = GeneralUtils.getConfig('config.ini', 'bot')

bot.run(botConfig['token'])