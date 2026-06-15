"""
ui.py

Author: Daniel Le
Date:   05.13.2025

Tkinter UI helpers for the Alzheimer's simulation:
- Drawing the bubble grid (population canvas)
- Handling bubble click events
- Person info popup
- Alzheimer's educational info window
"""

import math
import tkinter as tk
from tkinter import Toplevel

from config import (
    RADIUS, GRID_SIZE, CANVAS_WIDTH,
    COLOR_MALE, COLOR_FEMALE,
    COLOR_MILD, COLOR_MODERATE, COLOR_SEVERE,
    COLOR_SELECTED, COLOR_DEFAULT_OUTLINE, COLOR_BG,
)

def draw_population(canvas, people, bubble_refs, selected_index):
    """Redraws all individuals as colored tracking nodes on the simulation canvas.

    Args:
        canvas (tk.Canvas): The target graphic layout field.
        people (list[pt.Person]): Collection containing all active population profiles.
        bubble_refs (dict[tuple[int, int], int]): Reference dictionary mapping center-point 
            coordinate vectors (cx, cy) to their respective profile array indexes. Modified in-place.
        selected_index (int or None): The specific person array index currently selected 
            by the pointer tool to receive highlight strokes.
    """
    canvas.delete("all")
    bubble_refs.clear()

    # Calculate optimal pixel margin layouts for spacing grid items
    spacing = 2 * RADIUS
    margin  = (CANVAS_WIDTH - spacing * GRID_SIZE) // 2

    for i, person in enumerate(people):
        row = i // GRID_SIZE
        col = i % GRID_SIZE
        x   = margin + col * spacing + RADIUS
        y   = margin + row * spacing + RADIUS

        color = _bubble_color(person)

        # Apply distinct highlight strokes onto active selections
        if i == selected_index:
            outline, width = COLOR_SELECTED, 3
        else:
            outline, width = COLOR_DEFAULT_OUTLINE, 1

        canvas.create_oval(
            x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS,
            fill=color, outline=outline, width=width,
        )
        # Store layout vector anchors for click detection processing loops
        bubble_refs[(x, y)] = i


def _bubble_color(person):
    """Calculates the specific fill color for a person based on diagnostic properties.

    Args:
        person (pt.Person): The target individual profile reference.

    Returns:
        str: Hex color string or standard name assigned to the visual token.
    """
    if person.has_alzheimers:
        stage = person.getStage()
        return {
            "Mild":     COLOR_MILD,
            "Moderate": COLOR_MODERATE,
            "Severe":   COLOR_SEVERE,
        }.get(stage, COLOR_MILD)
    
    return COLOR_MALE if person.getGender() == "Male" else COLOR_FEMALE


def find_clicked_person(event, bubble_refs):
    """Resolves mouse click screen coordinates to extract the target node index.

    Args:
        event (tk.Event): Input event wrapper capturing local coordinates.
        bubble_refs (dict[tuple[int, int], int]): Spatial registration coordinate dictionary.

    Returns:
        int or None: The target collection index if verified inside item tracking ranges,
                     otherwise None.
    """
    x, y = event.x, event.y
    for (cx, cy), index in bubble_refs.items():
        # Evaluate standard physical boundaries using the distance formula
        if math.sqrt((cx - x) ** 2 + (cy - y) ** 2) <= RADIUS:
            return index
    return None

def show_person_popup(root, person, on_close):
    """Generates an auxiliary window overlay displaying profile diagnostics metrics.

    Args:
        root (tk.Tk): The parent Tkinter root execution canvas frame.
        person (pt.Person): The specific individual profile being inspected.
        on_close (callable): Call-back function handler triggered upon closure.

    Returns:
        tk.Toplevel: The active overlay auxiliary sub-window frame container handle.
    """
    # Fetch current layout pointers to place popup dynamically
    x = root.winfo_pointerx()
    y = root.winfo_pointery()

    popup = Toplevel(root)
    popup.geometry(f"+{x + 10}+{y + 10}")
    popup.title("Person Info")
    popup.geometry("200x165")
    popup.protocol("WM_DELETE_WINDOW", on_close)

    # Format clinical criteria details into readable block strings
    lines = [
        f"Age: {person.getAge()}",
        f"Gender: {person.getGender()}",
        f"Family History: {'Yes' if person.family_history else 'No'}",
        f"APOE4: {'Yes' if person.apoe4 else 'No'}",
        f"Status: {'Alzheimer\'s' if person.has_alzheimers else 'Healthy'}",
        f"Stage: {person.getStage() if person.has_alzheimers else 'N/A'}",
    ]
    # Append metabolic tissue region scores
    for region, value in person.brain.items():
        lines.append(f"{region.title()}: {value:.2f}")

    tk.Label(
        popup, text="\n".join(lines),
        justify="left", font=("Arial", 10),
    ).pack(padx=10, pady=10)

    return popup

def build_legend(parent):
    """Generates an embedded graphic map panel breakdown of canvas colors.

    Args:
        parent (tk.Frame): The target layout context frame where layout items reside.
    """
    legend_items = [
        ("Male",     COLOR_MALE),
        ("Female",   COLOR_FEMALE),
        ("Mild",     COLOR_MILD),
        ("Moderate", COLOR_MODERATE),
        ("Severe",   COLOR_SEVERE),
    ]
    for label, color in legend_items:
        # Generate inline icon layout containers
        dot = tk.Canvas(parent, width=12, height=12, bg=COLOR_BG, highlightthickness=0)
        dot.create_oval(2, 2, 12, 12, fill=color, outline="")
        dot.pack(side="left", padx=2)
        
        tk.Label(
            parent, text=label, fg="white", bg=COLOR_BG,
            font=("Arial", 10)
        ).pack(side="left", padx=4)

# Structured static information content utilized by reference informational sub-windows
INFO_TEXT = """
Alzheimer's disease is a progressive neurological disorder characterized by memory
loss, cognitive decline, and behavioral changes.

Early Symptoms:
- Frequent memory loss disrupting daily life.
- Difficulty planning or solving problems.
- Confusion with time or place.
- Difficulty completing familiar tasks.
- Problems with words in speaking or writing.

Risk Factors:
- Age (most significant, especially 65+).
- Genetics (APOE4 gene increases risk significantly).
- Family history of Alzheimer's.
- Cardiovascular conditions.
- Lifestyle factors such as poor diet, substance abuse, and physical inactivity.

Stages:
1. Mild: Initial memory loss, difficulty with complex tasks.
2. Moderate: Noticeable memory gaps, confusion, behavioral changes.
3. Severe: Significant memory loss, loss of physical abilities, high dependency.

Odds of Developing Alzheimer's:
- Ages 65–74: approximately 5%.
- Ages 75–84: approximately 13%.
- Ages 85 and older: approximately 33%.

Prevention & Management:
- Physical exercise and healthy diet (Mediterranean diet recommended).
- Cognitive activities (e.g., puzzles, games, learning new skills).
- Regular social interactions.
- Stress management and adequate sleep.

Treatment:
- Medications to manage cognitive symptoms (e.g., Cholinesterase inhibitors, Memantine).
- Non-drug therapies like cognitive stimulation therapy and occupational therapy.

Resources:
- Alzheimer's Association (alz.org)
- National Institute on Aging (nia.nih.gov)
- Alzheimer's Foundation of America (alzfdn.org)

Ongoing Research:
- Development of new treatments targeting amyloid plaques.
- Early diagnostic methods through biomarkers and imaging.
"""

def show_info_window(root):
    """Launches a scrollable informational display window detailing medical criteria.

    Args:
        root (tk.Tk): The parent Tkinter root execution canvas frame.
    """
    win = Toplevel(root)
    win.title("Alzheimer's Disease Information")
    win.geometry("560x400")

    # Construct scrollable scrolling canvas structures
    canvas    = tk.Canvas(win, borderwidth=0, background=COLOR_BG)
    frame     = tk.Frame(canvas, background=COLOR_BG)
    scrollbar = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Recalculate layout tracking metrics whenever structures are resized
    frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
    )

    tk.Label(
        frame, text=INFO_TEXT, justify="left",
        font=("Arial", 12), wraplength=520, background=COLOR_BG, fg="white",
    ).pack(padx=20, pady=20)