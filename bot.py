from dotenv import dotenv_values
envValues = dotenv_values(".env")

from utils import DBUtils, SetupUtils

DBUtils.checkTables()

bot = SetupUtils.setupBot()
SetupUtils.importCogs(bot)

bot.run(envValues["DISCORD_TOKEN"])