# Alzheimer's Disease Population Simulation Engine

A population-scale Alzheimer's disease simulation built in Python that models disease prevalence and progression across a synthetic population using demographic and genetic risk factors. The application combines object-oriented programming, stochastic simulation, interactive visualization, and a Tkinter-based graphical interface to explore how age, gender, APOE4 status, and family history influence Alzheimer's outcomes over time.

This project was built as the final project for **CS 152 (Computational Thinking: Science)** at Colby College.

## Features

- Simulates a population of 1,600 individuals on a 40×40 interactive grid
- Models Alzheimer's risk using:
  - Age-based risk profiles
  - Gender-specific prevalence rates
  - APOE4 genetic risk factors
  - Family history effects
- Tracks disease progression through brain-region degradation:
  - Hippocampus
  - Amygdala
  - Prefrontal Cortex
- Classifies disease severity into:
  - Mild
  - Moderate
  - Severe
- Interactive patient inspection with detailed demographic and health information
- Real-time simulation controls with customizable population parameters
- Dynamic statistical visualizations using Matplotlib
- Educational information panel describing Alzheimer's disease and risk factors

---

## Project Structure

```text
.
├── app.py           # Main application and simulation controller
├── population.py    # Population generation and simulation engine
├── persontype.py    # Person, APOE4Person, and FamilyHistoryPerson classes
├── charts.py        # Statistical visualization functions
├── ui.py            # Tkinter UI and interaction utilities
├── config.py        # Global configuration parameters
└── README.md
```

---

## Simulation Model

Each individual is represented as an object with:

- Age
- Gender
- APOE4 status
- Family history status
- Alzheimer's diagnosis state
- Brain-region activity levels

The simulation advances in yearly increments:

1. Individuals age by one year
2. Alzheimer's risk is evaluated probabilistically
3. Diagnosed individuals experience brain-region degradation
4. Disease stage is updated based on cognitive activity levels
5. Population-level statistics are recorded

### Risk Factors

| Factor | Effect |
|----------|----------|
| Age | Risk increases substantially after age 65 |
| Gender | Females have slightly higher baseline risk |
| APOE4 | Elevated probability of developing Alzheimer's |
| Family History | Additional hereditary risk adjustment |

---

## Visualizations

The simulator generates several real-time statistical dashboards:

### Diagnosis Rate by Gender
Tracks Alzheimer's prevalence among male and female populations over time.

### Diagnosis Rate by Age Group
Compares prevalence across:

- Ages 65–74
- Ages 75–84
- Ages 85+

### APOE4 Analysis
Measures diagnosis rates among APOE4 carriers versus non-carriers.

### Disease Stage Distribution
Displays the proportion of diagnosed individuals in:

- Mild stage
- Moderate stage
- Severe stage

---

## Technologies Used

- Python
- Tkinter
- Matplotlib
- Object-Oriented Programming (OOP)
- Stochastic Simulation
- Data Visualization

---

## Running the Project

### Clone the Repository

```bash
git clone https://github.com/yourusername/alzheimers-simulator.git
cd alzheimers-simulator
```

### Install Dependencies

```bash
pip install matplotlib
```

### Launch Application

```bash
python3 app.py
```

---

## Example Parameters

| Parameter | Default |
|------------|----------|
| Under 20 Population | 20% |
| Age 20–60 Population | 50% |
| Male Ratio | 50% |
| APOE4 Male | 30% |
| APOE4 Female | 40% |
| Family History | 25% |
| Brain Degradation Rate | 5% |
| Simulation Length | 10 Years |

---

## Key Software Design Decisions

- Modular architecture separating simulation, UI, visualization, and configuration logic
- Class inheritance for specialized demographic groups (`APOE4Person`, `FamilyHistoryPerson`)
- Encapsulation of disease progression within individual patient objects
- Independent chart-rendering layer for maintainability and extensibility
- Event-driven GUI built with Tkinter

---

## Future Improvements

- Lifestyle-based risk factors (sleep, smoking, exercise, diet)
- Additional neurological regions
- Mortality and life-expectancy modeling
- Exportable simulation datasets
- Longitudinal patient tracking
- Statistical confidence intervals and sensitivity analysis

---

## Data Sources

- [Alzheimer's Association — 2025 Alzheimer's Disease Facts and Figures](https://www.alz.org/getmedia/ef8f48f9-ad36-48ea-87f9-b74034635c1e/alzheimers-facts-and-figures.pdf)

---

## Author

**Daniel Le**

Mathematics & Statistics • Computer Science

Colby College
