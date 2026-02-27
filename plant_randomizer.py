import random
from typing import List, Tuple, Optional

from random_plants import (
    sun_producers,
    sun_plants,
    gemium_plants,
    epic_plants,
    world_plants,
    mints,
    aquatic_plants,
    unobtainable_plants,
    sun_cost,
)


def _build_all_plants() -> List[str]:
    """Return a deduplicated list of all plants (gemium + epic + world + mints)."""
    seen = set()
    result = []
    for plant in gemium_plants + epic_plants + world_plants + mints:
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
    no_aquatic: bool = False,
    min_cost: Optional[int] = None,
    max_cost: Optional[int] = None,
    no_epic: bool = False,
    no_gem: bool = False,
) -> List[str]:
    """Build and filter the plant pool based on flags."""
    # Start with world plants only or all plants
    if world_only:
        pool = list(world_plants)
    else:
        pool = _build_all_plants()

    # Apply rarity filters
    if no_gem:
        gem_set = set(gemium_plants)
        pool = [p for p in pool if p not in gem_set]

    if no_epic:
        epic_set = set(epic_plants)
        pool = [p for p in pool if p not in epic_set]

    if no_mint:
        mint_set = set(mints)
        pool = [p for p in pool if p not in mint_set]

    if exclude_sun:
        sun_set = set(sun_plants)
        pool = [p for p in pool if p not in sun_set]

    if no_aquatic:
        aquatic_set = set(aquatic_plants)
        pool = [p for p in pool if p not in aquatic_set]

    if only_obtainable:
        unobtainable_set = set(unobtainable_plants)
        pool = [p for p in pool if p not in unobtainable_set]

    # Apply cost filters
    if min_cost is not None or max_cost is not None:
        filtered = []
        for plant in pool:
            cost = sun_cost.get(plant, 0)
            if min_cost is not None and cost < min_cost:
                continue
            if max_cost is not None and cost > max_cost:
                continue
            filtered.append(plant)
        pool = filtered

    return pool


def random_plants(
    plant_count: int,
    *,
    forced_sun: bool = False,
    only_obtainable: bool = False,
    no_mint: bool = False,
    world_only: bool = False,
    no_aquatic: bool = False,
    min_cost: Optional[int] = None,
    max_cost: Optional[int] = None,
    no_epic: bool = False,
    no_gem: bool = False,
) -> Tuple[List[str], Optional[str]]:
    """Pick *plant_count* random plants.

    Returns ``(chosen_plants, error_message)``.
    If *error_message* is not None the caller should display it.
    """
    pool = _filter_pool(
        world_only=world_only,
        no_mint=no_mint,
        only_obtainable=only_obtainable,
        no_aquatic=no_aquatic,
        min_cost=min_cost,
        max_cost=max_cost,
        no_epic=no_epic,
        no_gem=no_gem,
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
    no_aquatic: bool = False,
    min_cost: Optional[int] = None,
    max_cost: Optional[int] = None,
    no_epic: bool = False,
    no_gem: bool = False,
) -> Tuple[List[str], Optional[str]]:
    """Pick *plant_count* random plants, excluding all sun-related plants."""
    pool = _filter_pool(
        world_only=world_only,
        no_mint=no_mint,
        only_obtainable=only_obtainable,
        exclude_sun=True,
        no_aquatic=no_aquatic,
        min_cost=min_cost,
        max_cost=max_cost,
        no_epic=no_epic,
        no_gem=no_gem,
    )

    if plant_count < 1:
        return [], "plant_count must be >= 1."
    if plant_count > len(pool):
        return [], (
            f"Not enough plants! Need {plant_count} but only "
            f"{len(pool)} available (after excluding sun)."
        )

    return random.sample(pool, plant_count), None
