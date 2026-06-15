"""
population.py

Author: Daniel Le
Date:   05.13.2025

Handles population generation and year-by-year simulation logic.
All person creation and disease-progression steps live here,
keeping them separate from the GUI layer.
"""

import random
import persontype as pt
from config import POP_SIZE


def generate_population(age_dist, gender_ratio, apoe4_male_ratio,
                        apoe4_female_ratio, family_history_ratio):
    """Creates a complete population array populated by stratified demographic subclasses.

    Args:
        age_dist (dict[str, float]): Fractional breakdowns summing to 1.0. 
            Expected keys: 'under_20', '20_60', 'over_60'.
        gender_ratio (float): Probability bound (0-1) for evaluating male assignment.
        apoe4_male_ratio (float): Relative baseline presence of APOE4 among males.
        apoe4_female_ratio (float): Relative baseline presence of APOE4 among females.
        family_history_ratio (float): Percentage likelihood of lineage risk presence.

    Returns:
        list[pt.Person]: A mixed collection containing base Person, APOE4Person, 
            or FamilyHistoryPerson instances.
    """
    people = []

    for _ in range(POP_SIZE):
        age    = _random_age(age_dist)
        gender = "Male" if random.random() < gender_ratio else "Female"

        # Dynamically assign genetic mutation limits based on biological gender
        apoe4_rate = apoe4_male_ratio if gender == "Male" else apoe4_female_ratio
        has_apoe4  = random.random() < apoe4_rate

        # Determine the most accurate sub-class combination for the individual
        if has_apoe4 and random.random() < family_history_ratio:
            person = pt.FamilyHistoryPerson(age, gender)
            person.apoe4 = True          # Explicitly patch genetic flag missing in constructor
        elif has_apoe4:
            person = pt.APOE4Person(age, gender)
        elif random.random() < family_history_ratio:
            person = pt.FamilyHistoryPerson(age, gender)
        else:
            person = pt.Person(age, gender)

        people.append(person)

    return people


def _random_age(age_dist):
    """Samples a random chronological age based on specified demographic thresholds.

    Args:
        age_dist (dict[str, float]): Distribution boundaries configured for the runtime.

    Returns:
        int: A pseudo-random integer age mapping within the targeted bucket.
    """
    r = random.random()

    # Cumulative density evaluation across configured age groups
    if r < age_dist["under_20"]:
        return random.randint(1, 19)
    elif r < age_dist["under_20"] + age_dist["20_60"]:
        return random.randint(20, 60)
    else:
        return random.randint(61, 95)


def simulate_year(people, degrade_rate, history_by_gender, new_cases_log):
    """Advances the aggregate population model forward by a single annual tracking cycle.

    Args:
        people (list[pt.Person]): Active collection tracking current state variables.
        degrade_rate (float): Base decay modifier passed to cellular decrement systems.
        history_by_gender (dict[str, list[float]]): Global tracking vectors modified in-place.
        new_cases_log (list[int]): Linear chronological sequence log capturing annual incident shifts.

    Returns:
        int: Sum total of individual objects newly moving into a positive disease state.
    """
    new_cases = 0

    # Apply global timeline progressions to every tracking unit
    for person in people:
        person.incrementAge()

        # Check for incident condition transformation updates
        if person.maybe_develop_alzheimers():
            new_cases += 1

        # Process standard internal decay algorithms
        person.degrade_brain(rate=degrade_rate)

    # Store incident event counts for chart rendering modules
    new_cases_log.append(new_cases)

    # Re-calculate split percentage metrics across demographics
    for gender in ("Male", "Female"):
        group = [p for p in people if p.gender == gender]
        if group:
            percent = sum(1 for p in group if p.has_alzheimers) / len(group) * 100
        else:
            percent = 0
        history_by_gender[gender].append(percent)

    return new_cases