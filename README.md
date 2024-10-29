
# L-in-Discord

This is a Discord bot inspired by **L** from *Death Note*, designed to provide responses with a personality that matches L's genius-level deduction skills, occasional trolling, and socially awkward style. Using the Google Gemini model for natural language responses, the bot engages in conversations in a way that mirrors L’s character.


![Alt Text](https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/L_Old_London.svg/330px-L_Old_London.svg.png)

## 🔥 Features

- **Persona-Based Interactions**: Engage with L using commands like `!Lanalyze`, `!Ldeduce`, and more. Each response is crafted with L's iconic analytical and mysterious tone.
- **Dynamic Typing & Reactions**: Simulates realistic typing delays and adds reactions to messages, enhancing the immersion.
- **Contextual Memory**: Maintains recent conversation history to deliver responses with contextual understanding.
- **Adaptive Presence**: The bot updates its Discord status periodically to reflect actions that mimic L's personality.

## 📋 Setup

### Prerequisites

- **Python 3.12+**
- **Libraries**: `discord.py`, `dotenv`, `asyncio`

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pr45h4nt/L-in-Discord.git
   cd L-in-Discord
   ```

2. **Set up a virtual environment**:
   ```bash
   python3.12 -m venv .env
   source .env/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   - Create a `.env` file in the root directory with your Discord bot token and Gemini API token:
     ```plaintext
     discord_token=YOUR_DISCORD_TOKEN
     gemini_token=YOUR_GEMINI_API_TOKEN
     ```

### Running the Bot

To start the bot, activate your virtual environment and run the bot script:

```bash
source .env/bin/activate
python bot.py
```

## 🎮 Usage

### Commands Overview

| Command                | Description                                                                                             |
|------------------------|---------------------------------------------------------------------------------------------------------|
| **`!Lanalyze <text>`** | Have L analyze a question or situation, offering deductive insights with probability estimates.         |
| **`!Ldeduce [@user]`** | L makes a deduction about a server member based on account age, roles, and other details.               |
| **`!Lclear_history`**  | Clears conversation history for the user, resetting the context for future interactions.                |
| **`!Lhelpme`**         | Displays help text with an "L-like" persona, providing assistance in a cryptic, characteristic manner.  |

### Example Interactions

- **Dynamic Reactions**: SmartBot occasionally reacts with emojis such as 🍰, 🔍, or 🤔 to add a quirky touch.
- **Presence Updates**: L’s status alternates between activities like “Calculating probabilities…” or “Eating sweets,” updating every 5 minutes.
- **Realistic Typing Delays**: Response time is dynamically adjusted based on message length to simulate a natural typing delay.

## 🛠️ Code Structure

- **`bot.py`**: Main bot script defining commands, event handling, and memory management.
- **`config.py`**: Handles configuration, loading environment variables and the custom prompt for L's persona.
- **`get_response.py`**: Handles communication with the Gemini AI model, including API calls and response generation.
- **`requirements.txt`**: Lists required Python libraries for the project.

## 🚨 Logging and Debugging

- **Error Handling**: The bot uses comprehensive logging for all command events and interactions, ensuring any issues are easily traceable.
- **Timezone Compatibility**: UTC-based time handling prevents conflicts in date and time calculations across various Discord servers.

## 🔧 Troubleshooting

- **Command Not Responding**: Ensure `await` is used with asynchronous functions in commands.
- **Timezone Errors**: Offset-aware timestamps are used to avoid compatibility issues in date/time comparisons.
- **Rate Limit**: If you encounter rate limits, ensure that AI requests are spaced appropriately to respect API rate limits.

## 🤝 Contributing

Contributions are welcome! Fork the repository, make your updates, and submit a pull request. Help us make SmartBot even better!


---

Enjoy interacting with L, and let the deductions begin!
