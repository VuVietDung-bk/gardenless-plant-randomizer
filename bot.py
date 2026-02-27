import discord
from discord import app_commands
from discord.ext import commands

from plant_randomizer import random_plants, random_plants_no_sun


class GardendlessBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(
            command_prefix="g!",
            intents=intents,
            help_command=None,
        )

    async def setup_hook(self):
        self.tree.add_command(_random_plants)
        self.tree.add_command(_random_plants_no_sun)
        self.tree.add_command(_help)
        await self.tree.sync()
        print("Slash commands synced!")

    async def on_ready(self):
        print(f"{self.user} is online! 🌱")


# ── Helpers ────────────────────────────────────────────────────────────


def _build_embed(title: str, plants: list[str], forced_sun: bool = False) -> discord.Embed:
    embed = discord.Embed(
        title=title,
        color=discord.Color.green(),
    )
    lines: list[str] = []
    for idx, plant in enumerate(plants, 1):
        tag = " ☀️" if idx == 1 and forced_sun else ""
        lines.append(f"**{idx}.** {plant}{tag}")
    embed.description = "\n".join(lines)
    embed.set_footer(text="Gardendless Plant Randomer 🌻")
    return embed


def _flags_text(
    forced_sun: bool = False,
    only_obtainable: bool = False,
    no_mint: bool = False,
    world_only: bool = False,
    no_sun: bool = False,
    no_aquatic: bool = False,
    min_cost: int | None = None,
    max_cost: int | None = None,
    no_epic: bool = False,
    no_gem: bool = False,
) -> str:
    parts: list[str] = []
    if forced_sun:
        parts.append("☀️ Forced Sun")
    if no_sun:
        parts.append("🚫☀️ No Sun")
    if world_only:
        parts.append("🌍 World Only")
    if no_gem:
        parts.append("💎❌ No Gemium")
    if no_epic:
        parts.append("⭐❌ No Epic")
    if no_mint:
        parts.append("🍃 No Mint")
    if no_aquatic:
        parts.append("💧❌ No Aquatic")
    if only_obtainable:
        parts.append("✅ Obtainable Only")
    if min_cost is not None:
        parts.append(f"≥${min_cost}")
    if max_cost is not None:
        parts.append(f"≤${max_cost}")
    return " · ".join(parts) if parts else "No filters"


# ── Slash commands ─────────────────────────────────────────────────────


@app_commands.command(
    name="randomplants",
    description="Randomize a plant list from PvZ2.",
)
@app_commands.describe(
    plant_count="Number of plants to randomize",
    forced_sun="First plant will be a sun producer",
    only_obtainable="Only select obtainable plants",
    no_mint="Exclude all mints",
    world_only="Only select from world plants",
    no_aquatic="Exclude aquatic plants",
    min_cost="Minimum seed packet cost",
    max_cost="Maximum seed packet cost",
    no_epic="Exclude epic plants",
    no_gem="Exclude gemium plants",
)
async def _random_plants(
    interaction: discord.Interaction,
    plant_count: int,
    forced_sun: bool = False,
    only_obtainable: bool = False,
    no_mint: bool = False,
    world_only: bool = False,
    no_aquatic: bool = False,
    min_cost: int | None = None,
    max_cost: int | None = None,
    no_epic: bool = False,
    no_gem: bool = False,
):
    plants, error = random_plants(
        plant_count,
        forced_sun=forced_sun,
        only_obtainable=only_obtainable,
        no_mint=no_mint,
        world_only=world_only,
        no_aquatic=no_aquatic,
        min_cost=min_cost,
        max_cost=max_cost,
        no_epic=no_epic,
        no_gem=no_gem,
    )

    if error:
        await interaction.response.send_message(f"❌ {error}", ephemeral=True)
        return

    flags = _flags_text(
        forced_sun=forced_sun,
        only_obtainable=only_obtainable,
        no_mint=no_mint,
        world_only=world_only,
        no_aquatic=no_aquatic,
        min_cost=min_cost,
        max_cost=max_cost,
        no_epic=no_epic,
        no_gem=no_gem,
    )
    embed = _build_embed(
        f"🌱 Random Plants ({plant_count})",
        plants,
        forced_sun=forced_sun,
    )
    embed.add_field(name="Filters", value=flags, inline=False)
    await interaction.response.send_message(embed=embed)


@app_commands.command(
    name="randomplants_nosun",
    description="Randomize plants (excluding sun plants).",
)
@app_commands.describe(
    plant_count="Number of plants to randomize",
    only_obtainable="Only select obtainable plants",
    no_mint="Exclude all mints",
    world_only="Only select from world plants",
    no_aquatic="Exclude aquatic plants",
    min_cost="Minimum seed packet cost",
    max_cost="Maximum seed packet cost",
    no_epic="Exclude epic plants",
    no_gem="Exclude gemium plants",
)
async def _random_plants_no_sun(
    interaction: discord.Interaction,
    plant_count: int,
    only_obtainable: bool = False,
    no_mint: bool = False,
    world_only: bool = False,
    no_aquatic: bool = False,
    min_cost: int | None = None,
    max_cost: int | None = None,
    no_epic: bool = False,
    no_gem: bool = False,
):
    plants, error = random_plants_no_sun(
        plant_count,
        only_obtainable=only_obtainable,
        no_mint=no_mint,
        world_only=world_only,
        no_aquatic=no_aquatic,
        min_cost=min_cost,
        max_cost=max_cost,
        no_epic=no_epic,
        no_gem=no_gem,
    )

    if error:
        await interaction.response.send_message(f"❌ {error}", ephemeral=True)
        return

    flags = _flags_text(
        only_obtainable=only_obtainable,
        no_mint=no_mint,
        world_only=world_only,
        no_aquatic=no_aquatic,
        min_cost=min_cost,
        max_cost=max_cost,
        no_epic=no_epic,
        no_gem=no_gem,
        no_sun=True,
    )
    embed = _build_embed(f"🌱 Random Plants – No Sun ({plant_count})", plants)
    embed.add_field(name="Filters", value=flags, inline=False)
    await interaction.response.send_message(embed=embed)


@app_commands.command(
    name="help",
    description="Display usage guide for Gardendless Plant Randomer.",
)
async def _help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📖 Gardendless Plant Randomer – Guide",
        color=discord.Color.blurple(),
    )

    embed.add_field(
        name="/randomplants",
        value=(
            "Randomize plants from the entire PvZ2 list.\n"
            "**Parameters:**\n"
            "• `plant_count` – Number of plants to randomize *(required)*\n"
            "• `forced_sun` – First plant will be a sun producer\n"
            "• `only_obtainable` – Exclude unobtainable plants\n"
            "• `no_mint` – Exclude all mints\n"
            "• `no_gem` – Exclude gemium plants\n"
            "• `no_epic` – Exclude epic plants\n"
            "• `no_aquatic` – Exclude aquatic plants\n"
            "• `world_only` – Only select from world plants\n"
            "• `min_cost` – Minimum seed packet cost\n"
            "• `max_cost` – Maximum seed packet cost"
        ),
        inline=False,
    )

    embed.add_field(
        name="/randomplants_nosun",
        value=(
            "Randomize plants **excluding** sun plants.\n"
            "**Parameters:**\n"
            "• `plant_count` – Number of plants to randomize *(required)*\n"
            "• `only_obtainable` – Exclude unobtainable plants\n"
            "• `no_mint` – Exclude all mints\n"
            "• `no_gem` – Exclude gemium plants\n"
            "• `no_epic` – Exclude epic plants\n"
            "• `no_aquatic` – Exclude aquatic plants\n"
            "• `world_only` – Only select from world plants\n"
            "• `min_cost` – Minimum seed packet cost\n"
            "• `max_cost` – Maximum seed packet cost"
        ),
        inline=False,
    )

    embed.set_footer(text="Gardendless Plant Randomer 🌻")
    await interaction.response.send_message(embed=embed, ephemeral=True)
