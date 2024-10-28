
# L-in-Discord

This is a Discord bot inspired by **L** from *Death Note*, designed to provide responses with a personality that matches L's genius-level deduction skills, occasional trolling, and socially awkward style. Using the Google Gemini model for natural language responses, the bot engages in conversations in a way that mirrors L’s character.


![Alt Text](https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/L_Old_London.svg/330px-L_Old_London.svg.png)


## Features

- **L-themed Responses**: Delivers short, sharp, and sometimes cryptic responses inspired by L's personality.
- **Contextual Chat**: Maintains recent chat history for user-specific responses.

## Setup

### Requirements

- **Python** 3.8+
- **Discord.py**: Python library for interacting with Discord API.
- **Google Gemini**: For generating AI responses (requires an API key).

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/pr45h4nt/l-themed-discord-bot.git
   cd l-themed-discord-bot
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API Keys**

   modify the `config.py` file with your Discord bot token and Google Gemini API key:

   ```python
   # config.py
   discord_token = "YOUR_DISCORD_TOKEN"
   gemini_token = "YOUR_GEMINI_API_KEY"
   ```

4. **Run the Bot**

   ```bash
   python bot.py
   ```

## Usage

### Commands

- **`!Lanalyze <question>`**: Ask L a question, and he will reply based on recent conversation context.
- **`!Lclear_history`**: Clear your conversation history with the bot.
- **`!Lhelp`**: Clear your conversation history with the bot.

### Chat History Management

The bot keeps track of recent messages per user to maintain context for each conversation. When the message history for a user exceeds 10 messages, older messages are removed to optimize memory usage.

## File Overview

- `bot.py`: Main script for the bot that handles command processing and interaction logic.
- `get_response.py`: Generates responses from Google Gemini based on user input and chat history.
- `config.py`: Stores API keys and other configuration details like prompts.

## Troubleshooting

- **Command permissions**: Ensure the bot has necessary permissions in your server, such as reading messages and replying in channels.

## Contributing

Feel free to fork the repository and submit pull requests for new features, bug fixes, or improvements.


