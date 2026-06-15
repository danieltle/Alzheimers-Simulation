"""
config.py

Author: Daniel Le
Date:   05.13.2025

Global constants for the Alzheimer's Disease Progression Simulator.
This module stores configuration parameters, geometry sizes, population split 
defaults, genetic baseline ratios, and hexadecimal color codes utilized 
globally by GUI interfaces and background simulation classes alike.
"""

# Spatial layout canvas measurements
GRID_SIZE    = 40               # Number of tracking nodes per dimension grid row/column
POP_SIZE     = GRID_SIZE * GRID_SIZE  # Total active population sample volume size (1600)
RADIUS       = 7                # Structural pixel display radius width constraint of a single item
CANVAS_WIDTH  = 590             # Screen dimension width space limits for viewport drawing operations
CANVAS_HEIGHT = 590             # Screen dimension height space limits for viewport drawing operations

# Default baseline demographic data distributions
DEFAULT_UNDER_20        = 0.20  # Fractional probability index of initial cohort under age 20
DEFAULT_20_60           = 0.50  # Fractional probability index of initial cohort between ages 20 and 60
DEFAULT_MALE_RATIO      = 0.50  # Balanced default ratio constraint applied to determining binary male sex selection
DEFAULT_APOE4_MALE      = 0.30  # Estimated structural prevalence of APOE4 gene presence among baseline males
DEFAULT_APOE4_FEMALE    = 0.40  # Estimated structural prevalence of APOE4 gene presence among baseline females
DEFAULT_FAMILY_HISTORY  = 0.25  # Pre-conditioned family baseline multi-generational transmission risk spread index
DEFAULT_DEGRADE_RATE    = 0.05  # Standard clinical reduction multiplier applied annually to cognitive functional fields
DEFAULT_SIM_YEARS       = 10    # Standard temporal simulation step bounds limit counter execution scope

# UI visualization color maps
COLOR_MALE          = "skyblue"      # Canvas display filling tint mapped onto default male icons
COLOR_FEMALE        = "lightpink"    # Canvas display filling tint mapped onto default female icons
COLOR_MILD          = "#ff0000"      # State tracking warning tone for early disease indicators
COLOR_MODERATE      = "#b20002"      # High saturation alert tone signifying advancing cognitive complications
COLOR_SEVERE        = "#4a0100"      # Low-exposure warning shade assigned to systemic operational failure profiles
COLOR_SELECTED      = "yellow"       # Interface outline accent applied during click target detection cycles
COLOR_DEFAULT_OUTLINE = "gray"       # Standard separator frame background stroke applied inside normal bubbles
COLOR_BG            = "#323232"      # Low contrast theme base coat background layout tone