import os
import bot

from dotenv import load_dotenv  # Import dotenv to load environment variables
from bot import run_discord_bot  # Import the function to run Discord bot


load_dotenv()

# Set the environment variable
os.environ['DISCORD_BOT_TOKEN'] = 'MTI1MzM1MDg3NDEwMTcxNTAzNg.G8LZwq.xt4pA_ukPSUNrJ0VBho147WovT23OR5HvNm0I8'

# Run the bot
if __name__ == '__main__':
    bot.run_discord_bot()
