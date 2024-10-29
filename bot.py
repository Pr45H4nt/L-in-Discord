# bot.py
import discord
from discord.ext import commands
import asyncio
import random
import logging 
from datetime import datetime, timedelta , timezone
from get_response import general, askl
from config import discord_token, help_txt

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.messages = True
        intents.members = True  # Enable member intents
        
        super().__init__(command_prefix="!L", intents=intents)
        self.message_history = {}
        self.user_states = {}  # Track user interaction states
        self.last_interaction = {}  # Track timing of interactions
        
    async def setup_hook(self):
        # Add background task
        self.bg_task = self.loop.create_task(self.periodic_presence_update())
        
    async def periodic_presence_update(self):
        """Updates bot's presence with L-like status messages"""
        await self.wait_until_ready()
        presence_messages = [
            "Calculating probabilities...",
            "Observing human behavior",
            "Analyzing patterns",
            "Eating sweets",
            f"Solving cases ({len(self.guilds)} servers)",
        ]
        
        while not self.is_closed():
            status = random.choice(presence_messages)
            await self.change_presence(activity=discord.Game(name=status))
            await asyncio.sleep(300)  # Change every 5 minutes

    def memory_management(self, author_id):
        """Enhanced memory management with time-based cleanup"""
        if author_id not in self.message_history:
            self.message_history[author_id] = []
        
        # Keep only messages from last 24 hours and maximum 15 messages
        current_time = datetime.now()
        self.message_history[author_id] = [
            msg for msg in self.message_history[author_id][-15:]
            if current_time - msg.get('timestamp', current_time) < timedelta(hours=24)
        ]

    async def get_typing_delay(self, message_length):
        """Simulate realistic typing delays based on message length"""
        base_delay = 1
        char_delay = message_length * 0.02  # 20ms per character
        return min(base_delay + char_delay, 5)  # Cap at 5 seconds

bot = LBot()

@bot.event
async def on_ready():
    print(f'Detective L is online. Logged in as {bot.user}')
    print(f'Connected to {len(bot.guilds)} servers')
    
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Add quirky reactions randomly (1% chance)
    if random.random() < 0.01:
        reactions = ['🍰', '🍬', '🔍', '🤔', '📝']
        await message.add_reaction(random.choice(reactions))

    if bot.user.mention in message.content or bot.user in message.mentions or message.guild is None:
        # Add typing indicator
        async with message.channel.typing():
            if message.author.id not in bot.message_history:
                bot.message_history[message.author.id] = []

            # Store message with timestamp
            bot.message_history[message.author.id].append({
                'content': f'{message.author.global_name}: {message.content}',
                'timestamp': datetime.now()
            })
            
            bot.memory_management(message.author.id)
            
            # Get history content for AI
            history_content = [msg['content'] for msg in bot.message_history[message.author.id]]
            
            ai_reply = await general(history_content)
            
            if ai_reply:
                bot.message_history[message.author.id].append({
                    'content': f"L: {ai_reply}",
                    'timestamp': datetime.now()
                })
                
                # Add realistic typing delay
                delay = await bot.get_typing_delay(len(ai_reply))
                await asyncio.sleep(delay)
                
                await message.reply(ai_reply)

    await bot.process_commands(message)

@bot.command(name="analyze")
@commands.cooldown(1, 30, commands.BucketType.user)  # Rate limit: 1 use per 30 seconds per user
async def analyze(ctx, *, question):
    async with ctx.channel.typing():
        messages = [message async for message in ctx.channel.history(limit=20)]
        
        # Format history with timestamps
        chat_history = []
        for message in messages:
            formatted_time = message.created_at.strftime("%H:%M:%S")
            chat_history.append(f"[{formatted_time}] {message.author.name}: {message.content}")
        
        prompt_with_history = (
            f"Chat History:\n{'-' * 40}\n" +
            "\n".join(reversed(chat_history)) +
            f"\n{'-' * 40}\nQuestion for analysis: {question}\n\n"
        )
        
        ai_response = await askl(prompt_with_history)
        
        # Add realistic typing delay
        delay = await bot.get_typing_delay(len(ai_response))
        await asyncio.sleep(delay)
        
        await ctx.reply(ai_response)


@bot.command(name="deduce")
async def deduce(ctx, member: discord.Member = None):
    """L attempts to make deductions about a server member"""
    logger.info(f"Deduce command called by {ctx.author} for target {'self' if member is None else member}")

    try:
        # If no member is specified or member lookup fails, use the author
        target_member = member or ctx.author
        logger.info(f"Analyzing member: {target_member}")
        
        async with ctx.channel.typing():
            # Basic user information we can access

            created_at = target_member.created_at
            account_age = (datetime.now(timezone.utc) - created_at).days

            roles = [role.name for role in target_member.roles if role.name != "@everyone"]
            
            logger.info(f"Collected data - Account age: {account_age}, Roles: {roles}")
            
            # Craft the prompt
            deduction_prompt = f"""
            Subject Analysis Required:
            
            Observable Data:
            - Identity: {target_member.display_name}
            - Account Age: {account_age} days
            - Roles: {', '.join(roles)}
            - Status: {str(target_member.status) if hasattr(target_member, 'status') else 'Unknown'}
            
            As L, provide a short but insightful deduction about this user. Focus on subtle patterns and unexpected connections. Be mysterious and slightly unsettling, but avoid being hostile.
            """
            
            logger.info("Sending prompt to AI")
            
            try:
                # Get AI response with timeout
                ai_response = await askl(deduction_prompt)
                logger.info("Received AI response")
                
                # Add dramatic pause
                await asyncio.sleep(1.5)
                
                # Format and send response
                formatted_response = f"I am going to adjust my siting position while analyzing {target_member.display_name}*\n\n{ai_response}"
                await ctx.reply(formatted_response)
                
            except Exception as e:
                logger.error(f"Error in AI response generation: {str(e)}")
                await ctx.reply("*stares at monitor* The probability of a successful analysis has decreased significantly...")
                
    except discord.errors.Forbidden as e:
        logger.error(f"Permission error: {str(e)}")
        await ctx.reply("*frowns* I lack the necessary permissions to observe this subject.")
        
    except Exception as e:
        logger.error(f"Unexpected error in deduce command: {str(e)}")
        await ctx.reply(f"*nibbles on candy* Something unexpected has occurred. This is... intriguing.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply(help_txt)
    elif isinstance(error, commands.CommandOnCooldown):
        remaining = round(error.retry_after)
        await ctx.reply(f"Your eagerness is... interesting. Wait {remaining} seconds.")

@bot.command(name="clear_history")
async def clear_history(ctx):
    user_id = ctx.author.id
    if user_id in bot.message_history:
        bot.message_history[user_id] = []
    await ctx.send("*arranges sugar cubes while erasing our conversation history*")

@bot.command(name="helpme")
async def lhelp(ctx):
    await ctx.reply(help_txt)

# Run the bot
bot.run(discord_token)