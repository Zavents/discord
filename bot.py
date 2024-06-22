import discord
import os
import random
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from discord.ext import commands
import operator
import re
from googletrans import Translator

# Define the image URLs
image_urls = [
    'https://cdn.discordapp.com/attachments/1041302483470925836/1253359377260216451/Screenshot_2024-06-20_192123.png?ex=66759161&is=66743fe1&hm=ad5511bc90e7b39293f730f02febaeb42fd81ce70f044ec5affa7761b5262266&',
    'https://cdn.discordapp.com/attachments/1041302483470925836/1253359377532977162/Screenshot_2024-06-20_194610.png?ex=66759161&is=66743fe1&hm=fc3dc5c7a7f79702787224ed5d86956ad53ecc34f797159d2feb70de58d5bd6c&',
    'https://cdn.discordapp.com/attachments/1041302483470925836/1230902057309835354/image.png?ex=6674f29f&is=6673a11f&hm=b7990928986778b3f82cf206d106fe5f4b28580989bb02ab83ddf047e1da665a&',
    'https://cdn.discordapp.com/attachments/1041302483470925836/1230517921642578046/image.png?ex=6675871e&is=6674359e&hm=bb7a0d9fe8820ce10845ca31bd7a2766758edb823ab3b4ab5f0b9a0c9ea9b54b&'
]

async def send_random_image(channel):
    try:
        image_url = random.choice(image_urls)
        await channel.send(image_url)
    except Exception as e:
        print(f"Error sending image: {e}")

async def send_message(channel, message):
    try:
        await channel.send(message)
    except Exception as e:
        print(f"Error sending message: {e}")

def run_discord_bot():
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')  # Retrieve bot token from environment variable

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix='==', intents=intents)
    scheduler = AsyncIOScheduler()
    translator = Translator()

    @bot.event
    async def on_ready():
        print(f'{bot.user} is now running!')

        # Retrieve the specific channel by its ID
        channel = bot.get_channel(1041302483470925836)  # Replace with your channel ID
        
        # Send a random image upon startup
        # await send_random_image(channel)

        # Set bot's status
        await bot.change_presence(activity=discord.Game(name="Zavents :3"))
        
        # Schedule the job to run between 1 AM and 1 PM Indonesia time
        jakarta_tz = pytz.timezone('Asia/Jakarta')
        for hour in range(1, 14):  # From 1 AM to 1 PM
            trigger = CronTrigger(hour=hour, minute=0, second=0, timezone=jakarta_tz)
            scheduler.add_job(send_random_image, trigger, args=[channel])

        scheduler.start()

    def evaluate_expression(expression):
        try:
            # Replace the caret symbol with the exponentiation operator
            expression = expression.replace('^', '**')
            # Evaluate the expression using eval in a restricted environment
            result = eval(expression, {'__builtins__': None}, {
                'add': operator.add,
                'sub': operator.sub,
                'mul': operator.mul,
                'truediv': operator.truediv,
                'pow': operator.pow
            })
            return result
        except ZeroDivisionError:
            return "Error: Division by zero is not allowed."
        except Exception as e:
            return f"Error: {e}"

    @bot.command(name='math')
    async def math(ctx, *, expression: str = None):
        if expression is None:
            await ctx.send("Usage: `==math <number1> <operator> <number2> <operator> <number3> ...`\n"
                           "Operators: +, -, *, /, ^ (for exponentiation)")
            return

        expression = re.sub(r'[^0-9+\-*/.^ ]', '', expression)  # Sanitize input
        result = evaluate_expression(expression)
        await ctx.send(f"Result: {result}")

    @bot.command(name='t')
    async def translate(ctx, *, text: str = None):
        if text is None:
            await ctx.send("Usage: `==t <text>`")
            return

        try:
            translated = translator.translate(text, dest='en')
            target_lang = 'en' if translated.src != 'en' else 'ja'
            translated = translator.translate(text, dest=target_lang)
            embed = discord.Embed(title="Translation", color=discord.Color.blue())
            embed.add_field(name="Translation", value=translated.text, inline=False)
            embed.add_field(name="Languages", value=f"Original: {translated.src.capitalize()} | Result: {'English' if target_lang == 'en' else 'Japanese'}", inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @bot.command(name='command')
    async def cmmd(ctx):
        embed = discord.Embed(title=f"Commands of {bot.user.name}", color=discord.Color.blue())
        embed.add_field(name="==math", value="Usage: `==math <number1> <operator> <number2> ...`", inline=False)
        embed.add_field(name="==t", value="Usage: `==t <text>`", inline=False)
        embed.add_field(name="==cmd", value="Shows this message.", inline=False)
        await ctx.send(embed=embed)

    bot.run(TOKEN)

if __name__ == '__main__':
    run_discord_bot()
