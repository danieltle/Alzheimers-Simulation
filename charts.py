"""
charts.py

Author: Daniel Le
Date:   05.13.2025

All Matplotlib chart-rendering logic for the Alzheimer's simulation.
Each function receives the data it needs and the Axes/Canvas objects to draw on,
keeping chart logic cleanly separated from the Tkinter UI layer.
"""

def update_gender_chart(ax, chart_canvas, history_by_gender):
    """Redraws the historical progression line chart for gender diagnoses.

    Args:
        ax (matplotlib.axes.Axes): The target sub-plot plotting surface area.
        chart_canvas (matplotlib.backends.backend_tkagg.FigureCanvasTkAgg): The Tkinter 
            canvas wrapper engine that requires a fresh surface canvas draw invocation.
        history_by_gender (dict[str, list[float]]): Historical log maps of active percentage 
            levels. Expected schema lookups: {"Male": [...], "Female": [...]}.
    """
    # Clear the previous drawing state out from the axis layout
    ax.clear()
    ax.set_title("% Diagnosed by Gender")
    ax.set_ylabel("%")
    ax.set_xlabel("Year")
    ax.set_ylim(0, 100)

    # Plot progression lines sequentially for each demographic category
    for gender in ("Male", "Female"):
        ax.plot(history_by_gender[gender], label=gender)

    ax.legend()
    chart_canvas.draw()


def update_age_chart(ax, age_canvas, people):
    """Redraws the bar chart showing diagnosis distribution across age cohorts.

    Args:
        ax (matplotlib.axes.Axes): The target sub-plot plotting surface area.
        age_canvas (matplotlib.backends.backend_tkagg.FigureCanvasTkAgg): The Tkinter
            canvas wrapper engine that requires a fresh surface canvas draw invocation.
        people (list[Person]): Collection containing all active simulated patient objects.
    """
    ax.clear()

    # Bucket individual objects based on operational clinical ranges
    age_bins = {"65–74": [], "75–84": [], "85+": []}
    for p in people:
        age = p.getAge()
        if 65 <= age <= 74:
            age_bins["65–74"].append(p)
        elif 75 <= age <= 84:
            age_bins["75–84"].append(p)
        elif age >= 85:
            age_bins["85+"].append(p)

    # Compute ratio breakdowns for each age milestone cohort
    labels, percentages = [], []
    for label, group in age_bins.items():
        if group:
            pct = sum(1 for p in group if p.has_alzheimers) / len(group) * 100
        else:
            pct = 0
        labels.append(label)
        percentages.append(pct)

    # Generate layout structure and overlay precision data labels centered inside bars
    bars = ax.bar(labels, percentages, color=["#4c72b0", "#55a868", "#c44e52"])
    ax.set_title("Diagnosis Rate by Age Group")
    ax.set_ylabel("% Diagnosed")
    ax.set_ylim(0, 100)
    ax.bar_label(bars, fmt="%.1f%%", label_type="center", color="white", fontsize=10)
    
    age_canvas.draw()


def update_apoe_chart(ax, apoe_canvas, people):
    """Redraws the diagnostic comparison chart between APOE4 and Non-APOE4 carriers.

    Args:
        ax (matplotlib.axes.Axes): The target sub-plot plotting surface area.
        apoe_canvas (matplotlib.backends.backend_tkagg.FigureCanvasTkAgg): The Tkinter
            canvas wrapper engine that requires a fresh surface canvas draw invocation.
        people (list[Person]): Collection containing all active simulated patient objects.
    """
    ax.clear()

    # Distribute the cohort into genetic profile categories
    apoe_groups = {"APOE4": [], "Non-APOE4": []}
    for p in people:
        key = "APOE4" if p.apoe4 else "Non-APOE4"
        apoe_groups[key].append(p)

    # Compute individual risk category diagnosis metrics
    labels, percentages = [], []
    for label, group in apoe_groups.items():
        if group:
            pct = sum(1 for p in group if p.has_alzheimers) / len(group) * 100
        else:
            pct = 0
        labels.append(label)
        percentages.append(pct)

    # Render data configurations using a custom palette
    bars = ax.bar(labels, percentages, color=["#e377c2", "#17becf"])
    ax.set_title("Diagnosis Rate by APOE4 Status")
    ax.set_ylabel("% Diagnosed")
    ax.set_ylim(0, 100)
    ax.bar_label(bars, fmt="%.1f%%", label_type="center", color="white", fontsize=10)
    
    apoe_canvas.draw()


def update_stage_chart(ax, stage_canvas, people):
    """Redraws the bar chart showing clinical stage distribution among diagnosed cases.

    Args:
        ax (matplotlib.axes.Axes): The target sub-plot plotting surface area.
        stage_canvas (matplotlib.backends.backend_tkagg.FigureCanvasTkAgg): The Tkinter
            canvas wrapper engine that requires a fresh surface canvas draw invocation.
        people (list[Person]): Collection containing all active simulated patient objects.
    """
    ax.clear()

    stage_counts = {"Mild": 0, "Moderate": 0, "Severe": 0}
    total_with_alz = 0

    # Filter for active cases and tally severity distributions
    for p in people:
        if p.has_alzheimers:
            stage = p.getStage()
            if stage in stage_counts:
                stage_counts[stage] += 1
                total_with_alz += 1

    # Extract dynamic categories and calculate stage percentage proportions
    labels = list(stage_counts.keys())
    percentages = [
        (stage_counts[k] / total_with_alz * 100) if total_with_alz > 0 else 0
        for k in labels
    ]

    # Map tracking elements using a red heat-progression styling sequence
    bars = ax.bar(labels, percentages, color=["#ff9999", "#cc4444", "#660000"])
    ax.set_title("Alzheimer's Stages")
    ax.set_ylabel("% Diagnosed")
    ax.set_ylim(0, 100)
    ax.bar_label(bars, fmt="%.1f%%", label_type="center", color="white", fontsize=10)
    
    stage_canvas.draw()