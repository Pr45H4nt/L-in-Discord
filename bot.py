import discord
from discord.ext import commands
from get_response import general , askl 
from config import discord_token , help_txt



# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent
intents.messages = True  # Make sure the bot can read messages
bot = commands.Bot(command_prefix="!L", intents=intents)


message_history = {}

def memory_management(author):
    if len(message_history[author]) > 15:
        message_history[author].pop(0)



# Event: When the bot is ready
@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    # Prevent the bot from replying to itself
    print(f"Received message: {message.content} from {message.author}")
    if bot.user.mention in message.content or bot.user in message.mentions:
        print(f"""

{message_history}



""")
        if message.author.id not in message_history:
            message_history[message.author.id] = []

        message_history[message.author.id].append(f'{message.author.global_name}:{ message.content}')
        memory_management(message.author.id)
        
        ai_reply = general(message_history[message.author.id])
        if ai_reply:
            message_history[message.author.id].append(f"L: {ai_reply}")

        await message.reply(ai_reply)
        
    # Process other bot commands
    await bot.process_commands(message)


@bot.command(name="analyze")
async def analyze(ctx, *, question):
    # Fetch recent history
    messages = [message async for message in ctx.channel.history(limit=20)]
    
    print(messages)
    # Format history for prompt
    chat_history = [f"{message.author.name}: {message.content}" for message in messages]
    user_question = f"User asked: {question}"

    # if ctx.author.id not in message_history:
    #     message_history[ctx.author.id] = []

    # message_history[ctx.author.id].append(f'{ctx.author.global_name}:{question}')
        
    
    # Prepare prompt with history
    prompt_with_history = f"Chat History:\n" + "\n".join(chat_history) + f"\n\nUser Question:\n{user_question}\n\n"
    ai_response = askl(prompt_with_history)
    
    # message_history[ctx.author.id].append(f'L: {question}')

    # memory_management(ctx.author.id)

    
    await ctx.send(f"{ai_response}")



@bot.command(name="clear_history")
async def clear_history(ctx):
    user_id = ctx.author.id
    if user_id in message_history:
        message_history[user_id] = []
    await ctx.send("Your Conversation history cleared!")

@bot.command(name="help")
async def help(ctx):
    ctx.reply(help_txt)
    


bot.run(discord_token)