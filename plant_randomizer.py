import random
from typing import List, Tuple

from random_plants import (
    sun_producers,
    sun_plants,
    premium_plants,
    world_plants,
    mints,
    unobtainable_plants,
)


def _build_all_plants() -> List[str]:
    """Return a deduplicated list of all plants."""
    seen = set()
    result = []
    for plant in world_plants + premium_plants + mints:
        if plant not in seen:
            seen.add(plant)
            result.append(plant)
    return result


def _filter_pool(
    *,
    world_only: bool = False,
    no_mint: bool = False,
    only_obtainable: bool = False,
    exclude_sun: bool = False,
) -> List[str]:
    """Build and filter the plant pool based on flags."""
    pool = list(world_plants) if world_only else _build_all_plants()

    if no_mint:
        mint_set = set(mints)
        pool = [p for p in pool if p not in mint_set]

    if only_obtainable:
        unobtainable_set = set(unobtainable_plants)
        pool = [p for p in pool if p not in unobtainable_set]

    if exclude_sun:
        sun_set = set(sun_plants)
        pool = [p for p in pool if p not in sun_set]

    return pool


def random_plants(
    plant_count: int,
    *,
    forced_sun: bool = False,
    only_obtainable: bool = False,
    no_mint: bool = False,
    world_only: bool = False,
) -> Tuple[List[str], str | None]:
    """Pick *plant_count* random plants.

    Returns ``(chosen_plants, error_message)``.
    If *error_message* is not None the caller should display it.
    """
    pool = _filter_pool(
        world_only=world_only,
        no_mint=no_mint,
        only_obtainable=only_obtainable,
    )

    if forced_sun:
        # Sun producer must come from the pool too (respect filters)
        pool_set = set(pool)
        available_sun = [p for p in sun_producers if p in pool_set]
        if not available_sun:
            return [], "No available sun producers after filtering!"

        first = random.choice(available_sun)
        remaining_pool = [p for p in pool if p != first]

        needed = plant_count - 1
        if needed < 0:
            return [], "plant_count must be >= 1."
        if needed > len(remaining_pool):
            return [], (
                f"Not enough plants! Need {needed} more plants but only "
                f"{len(remaining_pool)} available."
            )

        rest = random.sample(remaining_pool, needed)
        return [first] + rest, None

    if plant_count > len(pool):
        return [], (
            f"Not enough plants! Need {plant_count} but only "
            f"{len(pool)} available."
        )
    if plant_count < 1:
        return [], "plant_count must be >= 1."

    return random.sample(pool, plant_count), None


def random_plants_no_sun(
    plant_count: int,
    *,
    only_obtainable: bool = False,
    no_mint: bool = False,
    world_only: bool = False,
) -> Tuple[List[str], str | None]:
    """Pick *plant_count* random plants, excluding all sun-related plants."""
    pool = _filter_pool(
        world_only=world_only,
        no_mint=no_mint,
        only_obtainable=only_obtainable,
        exclude_sun=True,
    )

    if plant_count < 1:
        return [], "plant_count must be >= 1."
    if plant_count > len(pool):
        return [], (
            f"Not enough plants! Need {plant_count} but only "
            f"{len(pool)} available (after excluding sun)."
        )

    return random.sample(pool, plant_count), None
