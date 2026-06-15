"""
persontype.py

Author: Daniel Le
Date:   05.13.2025

This program stores the classes of different demographics in the population, which will be used in
the main Alzheimer's simulation.

To run the program, use the following command line in the terminal:
    python3 persontype.py
"""

import random


class Person:
    """Base class tracking normal demographic attributes and baseline cognitive health.

    Attributes:
        age (int): Current age of the person in years.
        gender (str): Binary sex marker assigned to the person ("Male" or "Female").
        has_alzheimers (bool): Diagnosis condition state flag.
        apoe4 (bool): Genetic mutation variant marker flag.
        family_history (bool): Multigenerational hereditary line risk flag.
        brain (dict[str, float]): Metabolic functional scores for critical regions.
            Tracks keys: 'hippocampus', 'amygdala', and 'prefrontal'.
    """

    def __init__(self, age, gender, apoe4=False, family_history=False):
        """Initializes a normal individual with default brain function profiles.

        Args:
            age (int): Initial age assigned to the person.
            gender (str): Gender identity designation ("Male" or "Female").
            apoe4 (bool, optional): Genetic risk presence. Defaults to False.
            family_history (bool, optional): Lineage history presence. Defaults to False.
        """
        self.age = age
        self.gender = gender
        self.has_alzheimers = False
        self.apoe4 = apoe4
        self.family_history = family_history

        # Initialize core brain region functionality multipliers at unit scale
        self.brain = {'hippocampus': 1.0, 'amygdala': 1.0, 'prefrontal': 1.0}
    
    def getAge(self):
        """Retrieves the person's current age.

        Returns:
            int: The active age value.
        """
        return self.age
    
    def getGender(self):
        """Retrieves the person's biological gender assignment.

        Returns:
            str: "Male" or "Female".
        """
        return self.gender
    
    def incrementAge(self, years=1):
        """Advances the individual's age attribute by a set number of years.

        Args:
            years (int, optional): The annual step count interval. Defaults to 1.
        """
        self.age += years

    def degrade_brain(self, rate=0.05):
        """Reduces the health metrics across all tracked brain regions.

        Args:
            rate (float, optional): The degradation step modifier. Defaults to 0.05.
        """
        if self.has_alzheimers:
            # Sequentially lower the functional capacity metrics across all regions
            for region in self.brain:
                self.brain[region] = max(0.0, self.brain[region] - rate)

    def getStage(self):
        """Calculates the current severity categorization of Alzheimer's disease.

        Computes the arithmetic mean of all functional brain regions to determine
        the clinical boundary classification.

        Returns:
            str or None: "Mild", "Moderate", or "Severe" based on functional capacity thresholds.
                         Returns None if the individual is undiagnosed.
        """
        if not self.has_alzheimers:
            return None
        
        # Calculate aggregate functional score average across tracked keys
        avg_activity = sum(self.brain.values()) / len(self.brain)

        # Map mean functionality levels directly to standardized clinical stages
        if avg_activity > 0.8:
            return "Mild"
        elif avg_activity > 0.5:
            return "Moderate"
        else:
            return "Severe"
        
    def familyHistory(self):
        """Checks the hereditary history marker status of the individual.

        Returns:
            bool: True if a historical lineage presence exists, otherwise False.
        """
        return self.family_history
    
    def maybe_develop_alzheimers(self):
        """Calculates baseline age and gender-stratified risks to determine condition onset.

        Performs a stochastic rollout check using standard demographic probabilities.
        If the random roll falls beneath the calculated risk value, the condition triggers.

        Returns:
            bool: True if a transition event occurred this loop, otherwise False.
        """
        if self.has_alzheimers:
            return False
        
        # Branch probabilities based on demographic properties
        if self.gender == "Male":
            if 65 <= self.age <= 74:
                risk = 0.045
            elif 75 <= self.age <= 84:
                risk = 0.06
            elif self.age >= 85:
                risk = 0.075
            else:
                risk = 0.001
        else:  # Female demographic data risk branches
            if 65 <= self.age <= 74:
                risk = 0.055
            elif 75 <= self.age <= 84:
                risk = 0.07
            elif self.age >= 85:
                risk = 0.085
            else:
                risk = 0.003

        # Clamp max threshold limits for normal risk classes
        risk = min(risk, 0.09)

        # Execute stochastic selection evaluation
        if random.random() < risk:
            self.has_alzheimers = True
            return True
        
        return False


class APOE4Person(Person):
    """Specialized demographic subclass modeling elevated genetic risk profiles.

    Inherits baseline metrics from Person, overriding risk values to model
    the structural vulnerability changes associated with the APOE4 allele mutation.
    """

    def __init__(self, age, gender):
        """Initializes an individual carrier with an active APOE4 genetic marker.

        Args:
            age (int): Initial age assigned to the person.
            gender (str): Gender identity designation ("Male" or "Female").
        """
        # Formally call super constructor to set structural defaults cleanly
        super().__init__(age, gender, apoe4=True, family_history=False)

    def maybe_develop_alzheimers(self):
        """Evaluates elevated probability criteria specific to APOE4 allele carriers.

        Returns:
            bool: True if a transition event occurred this loop, otherwise False.
        """
        if self.has_alzheimers:
            return False
        
        # Apply escalated risk factors scaled for genetic allele carriers
        if self.gender == "Male":
            if 65 <= self.age <= 74:
                risk = 0.065
            elif 75 <= self.age <= 84:
                risk = 0.08
            elif self.age >= 85:
                risk = 0.09
            else:
                risk = 0.005
        else:  # Female demographic tracking properties
            if 65 <= self.age <= 74:
                risk = 0.075
            elif 75 <= self.age <= 84:
                risk = 0.09
            elif self.age >= 85:
                risk = 0.095
            else:
                risk = 0.007

        # Enforce distinct ceiling restrictions for high-risk profiles
        risk = min(risk, 0.1)
        
        if random.random() < risk:
            self.has_alzheimers = True
            return True
        
        return False


class FamilyHistoryPerson(Person):
    """Specialized demographic subclass modeling historical ancestral risks.

    Modifies probability roll evaluations by layering custom hazard modifiers 
    on top of existing age, gender, and genetic traits.
    """

    def __init__(self, age, gender):
        """Initializes an individual with documented family history markers.

        Args:
            age (int): Initial age assigned to the person.
            gender (str): Gender identity designation ("Male" or "Female").
        """
        super().__init__(age, gender, apoe4=False, family_history=True)

    def maybe_develop_alzheimers(self):
        """Evaluates complex compounded conditional hazards including lineage modifiers.

        Processes baseline risk models and layers on a static 
        risk penalty before completing selection rollouts.

        Returns:
            bool: True if a transition event occurred this loop, otherwise False.
        """
        if self.has_alzheimers:
            return False

        # Extract risk curves based on current genetic allele properties
        if self.apoe4:
            if self.gender == "Male":
                if 65 <= self.age <= 74:
                    risk = 0.065
                elif 75 <= self.age <= 84:
                    risk = 0.08
                elif self.age >= 85:
                    risk = 0.09
                else:
                    risk = 0.005
            else:
                if 65 <= self.age <= 74:
                    risk = 0.075
                elif 75 <= self.age <= 84:
                    risk = 0.09
                elif self.age >= 85:
                    risk = 0.095
                else:
                    risk = 0.007
        else:
            # Fall back to baseline curves if non-carrier traits are set
            if self.gender == "Male":
                if 65 <= self.age <= 74:
                    risk = 0.045
                elif 75 <= self.age <= 84:
                    risk = 0.06
                elif self.age >= 85:
                    risk = 0.075
                else:
                    risk = 0.001
            else:
                if 65 <= self.age <= 74:
                    risk = 0.055
                elif 75 <= self.age <= 84:
                    risk = 0.07
                elif self.age >= 85:
                    risk = 0.085
                else:
                    risk = 0.003

        # Add additive systemic hereditary risk modifier (0.5% shift)
        risk += 0.005

        # Enforce baseline standardization capping constraints
        risk = min(risk, 0.09)

        if random.random() < risk:
            self.has_alzheimers = True
            return True
        return False