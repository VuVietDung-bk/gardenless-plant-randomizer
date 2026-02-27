# Gardendless Plant Randomer

A Discord bot that randomizes Plants vs Zombies 2 (PvZ2) plants with various filtering options.

## Features

- **`/randomplants`** - Randomize plants from the full PvZ2 list (gemium + epic + world + mints) with optional filters:
  - `plant_count` (required) - Number of plants to randomize
  - `forced_sun` - First plant will always be a sun producer
  - `only_obtainable` - Exclude unobtainable plants
  - `no_gem` - Exclude gemium plants
  - `no_epic` - Exclude epic plants
  - `no_mint` - Exclude all mint plants
  - `no_aquatic` - Exclude aquatic plants
  - `world_only` - Only select from world plants
  - `min_cost` - Minimum seed packet cost filter
  - `max_cost` - Maximum seed packet cost filter

- **`/randomplants_nosun`** - Randomize plants excluding all sun-related plants:
  - `plant_count` (required) - Number of plants to randomize
  - `only_obtainable` - Exclude unobtainable plants
  - `no_gem` - Exclude gemium plants
  - `no_epic` - Exclude epic plants
  - `no_mint` - Exclude all mint plants
  - `no_aquatic` - Exclude aquatic plants
  - `world_only` - Only select from world plants
  - `min_cost` - Minimum seed packet cost filter
  - `max_cost` - Maximum seed packet cost filter

- **`/help`** - Display the command guide and usage instructions

## Prerequisites

- Python 3.8 or higher
- `discord.py` library (2.0+)
- `python-dotenv` for environment variables

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd random-plants-ge-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:
   ```
   DISCORD_BOT_TOKEN=your_bot_token_here
   ```

4. Get your bot token:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Create a new application
   - Navigate to "Bot" section and create a bot
   - Copy the token and paste it in `.env`

5. Invite the bot to your server:
   - In Developer Portal, go to OAuth2 > URL Generator
   - Select scopes: `bot`
   - Select permissions: `Send Messages`, `Embed Links`
   - Copy the generated URL and open it in your browser to invite the bot

## Running the Bot

```bash
python3 main.py
```

The bot will start and automatically sync slash commands with Discord.

## Deploying on Render

### Setup Instructions

1. Push your code to GitHub
2. Go to [Render.com](https://render.com/) and create a new Web Service
3. Connect your GitHub repository
4. Configure the service:
   - **Build command**: `pip install -r requirements.txt`
   - **Start command**: `python3 main.py`
   - **Environment Variables**: Add `DISCORD_BOT_TOKEN` with your bot token value
5. Deploy!

### Troubleshooting Render Deployment

**If you get HTTPException at login:**
- ✓ Verify `DISCORD_BOT_TOKEN` is set in Render's Environment settings (not in the code)
- ✓ Check token has NO extra spaces or quotes
- ✓ Regenerate token in Discord Developer Portal if it's old
- ✓ Check main.py output for token validation messages

## File Structure

```
random-plants-ge-bot/
├── bot.py                 # Main bot class and slash commands
├── plant_randomizer.py    # Plant randomization logic
├── random_plants.py       # Plant data (sun producers, mints, etc.)
├── main.py               # Bot entry point
├── webserver.py          # Flask server for keeping bot alive
├── .env                  # Environment variables (create this)
└── README.md            # This file
```

## Plant Categories

The bot uses the following plant categories from `random_plants.py`:

- **sun_producers** - Plants that produce sun
- **sun_plants** - All sun-related plants
- **gemium_plants** - Gemium/premium tier plants
- **epic_plants** - Epic tier plants
- **world_plants** - Plants from world adventure
- **mints** - Mint plants
- **aquatic_plants** - Aquatic/water plants
- **unobtainable_plants** - Plants that cannot be obtained
- **sun_cost** - Dictionary with seed packet costs for each plant

## Usage Examples

### Randomize 5 plants
```
/randomplants plant_count: 5
```

### Randomize 5 plants with forced sun (must start with sun producer)
```
/randomplants plant_count: 5 forced_sun: true
```

### Randomize only obtainable plants, no mints
```
/randomplants plant_count: 3 only_obtainable: true no_mint: true
```

### Only world plants
```
/randomplants plant_count: 4 world_only: true
```

### Plants with cost between 50-200 sun
```
/randomplants plant_count: 5 min_cost: 50 max_cost: 200
```

### No gemium, no epic, no aquatic
```
/randomplants plant_count: 3 no_gem: true no_epic: true no_aquatic: true
```

### Randomize plants without any sun plants
```
/randomplants_nosun plant_count: 5
```

### World plants without sun, no mints, cost >= 100
```
/randomplants_nosun plant_count: 3 world_only: true no_mint: true min_cost: 100
```

### Complex mix: no gem, no epic, obtainable only (no sun)
```
/randomplants_nosun plant_count: 4 no_gem: true no_epic: true only_obtainable: true
```

## Filter Combinations

All flags can be freely combined:
- `forced_sun` + `no_mint` + `only_obtainable` + `world_only` ✓
- `no_gem` + `no_epic` + `min_cost: 100` + `max_cost: 300` ✓
- `no_aquatic` + `no_mint` + `world_only` ✓
- All other combinations work as well

**Filter logic:**
1. Rarity filters (`no_gem`, `no_epic`, `no_mint`) are applied first
2. Feature filters (`exclude_sun`, `no_aquatic`) are applied next
3. Obtainability filter (`only_obtainable`) is applied
4. Cost filters (`min_cost`, `max_cost`) are applied last

When filters conflict with available plants (e.g., requesting 100 plants when only 50 exist after filtering), the bot will return an error message.

## Command Responses

Commands return an embed with:
- Plant list (numbered)
- ☀️ symbol marking forced sun plant (if applicable)
- Active filter summary
- Footer with bot name

Error messages appear as ephemeral messages (only visible to the command user).

## Troubleshooting

### Bot doesn't respond
- Ensure `DISCORD_BOT_TOKEN` is set correctly in `.env`
- Check that the bot has permissions to send messages in the channel
- Verify the bot has the "Send Messages" and "Embed Links" permissions

### Slash commands not appearing
- Run `/sync` after starting the bot (check console for "Slash commands synced!")
- Wait a few seconds for Discord to sync commands
- Restart the bot if commands still don't appear

### Import errors
- Ensure all dependencies are installed: `pip install discord.py python-dotenv`
- Verify all Python files are in the same directory

## License

This project is provided as-is for educational and personal use.

## Contributing

Feel free to submit issues and enhancement requests!
