"""
app.py

Author: Daniel Le
Date:   05.13.2025

Entry point for the Alzheimer's Disease Progression Simulator.
The AlzheimerApp class wires together the GUI (ui.py), simulation
logic (population.py), and charts (charts.py) into one cohesive
Tkinter application.

To run:
    python3 app.py
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import config
import population as pop
import charts
import ui


class AlzheimerApp:
    """Main application class for the Alzheimer's Disease Progression Simulator.

    This class coordinates the initialization and interaction between the
    Tkinter-based Graphical User Interface (GUI), the demographic population 
    generation, the step-by-step state mechanics, and the final Matplotlib visualization 
    canvases.

    Attributes:
        root (tk.Tk): The root Tkinter window frame context.
        people (list): Collection of individual patient profile objects.
        selected_index (int or None): Index of the currently clicked/inspected person.
        bubble_refs (dict): Maps canvas graphic IDs to person entities.
        popup (tk.Toplevel or None): Active auxiliary detail window handle.
        history_by_gender (dict): Tracks active condition count arrays over time.
        new_cases (list): Sequential log tracking newly developed diagnoses.
        age_dist (dict): Map breaking down the target generation age spreads.
        gender_ratio (float): Probability constant assigned to creating males.
        apoe4_male_ratio (float): Relative likelihood of APOE4 gene presence in males.
        apoe4_female_ratio (float): Relative likelihood of APOE4 gene presence in females.
        family_history_ratio (float): Likelihood of existing ancestral patterns.
        degrade_rate (float): Base severity acceleration modifier per simulation loop.
    """

    def __init__(self, root):
        """Initializes the simulation app framework and renders standard layouts.

        Args:
            root (tk.Tk): The parent window instance.
        """
        self.root = root
        self.root.title("Alzheimer's Simulation")
        self.root.configure(bg=config.COLOR_BG)

        # Runtime state tracking vectors
        self.people         = []
        self.selected_index = None
        self.bubble_refs    = {}
        self.popup          = None
        self.history_by_gender = {"Male": [], "Female": []}
        self.new_cases         = []

        # Default demographic settings (overwritten later via set_distribution)
        self.age_dist             = {"under_20": config.DEFAULT_UNDER_20,
                                     "20_60":    config.DEFAULT_20_60,
                                     "over_60":  1 - config.DEFAULT_UNDER_20 - config.DEFAULT_20_60}
        self.gender_ratio         = config.DEFAULT_MALE_RATIO
        self.apoe4_male_ratio     = config.DEFAULT_APOE4_MALE
        self.apoe4_female_ratio   = config.DEFAULT_APOE4_FEMALE
        self.family_history_ratio = config.DEFAULT_FAMILY_HISTORY
        self.degrade_rate         = config.DEFAULT_DEGRADE_RATE

        # UI Architecture Assembly Steps
        self._build_tabs()
        self._build_canvas_tab()
        self._build_chart_tabs()

        # Seed structural components and display original cohort state
        self.set_distribution()
        self.init_population()

    def _build_tabs(self):
        """Creates the top-level ttk.Notebook container framework and layout fields."""
        self.tabs = ttk.Notebook(self.root)

        # Tab pane allocation instances
        self.canvas_tab = tk.Frame(self.tabs)
        self.stats_tab  = tk.Frame(self.tabs)
        self.age_tab    = tk.Frame(self.tabs)
        self.apoe_tab   = tk.Frame(self.tabs)
        self.stage_tab  = tk.Frame(self.tabs)

        # Adding allocations directly to tracking system
        self.tabs.add(self.canvas_tab, text="Simulation")
        self.tabs.add(self.stats_tab,  text="Gender Statistics")
        self.tabs.add(self.age_tab,    text="Age Group Rates")
        self.tabs.add(self.apoe_tab,   text="APOE4 Rates")
        self.tabs.add(self.stage_tab,  text="Stages")

        self.tabs.pack(fill="both", expand=True)

    def _build_canvas_tab(self):
        """Builds the core interactive simulation layout canvas, canvas grids, and buttons."""
        # Population layout viewport setup
        self.canvas = tk.Canvas(
            self.canvas_tab,
            width=config.CANVAS_WIDTH, height=config.CANVAS_HEIGHT,
            bg=config.COLOR_BG,
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_click)

        # Draw structural layout key legends
        legend_frame = tk.Frame(self.canvas_tab, bg=config.COLOR_BG)
        legend_frame.pack(pady=5)
        ui.build_legend(legend_frame)

        # Setup structural buttons frame
        self.controls = tk.Frame(self.canvas_tab)
        self.controls.pack()
        self._build_controls()

    def _build_controls(self):
        """Generates configuration control elements and default simulation entries."""
        c = self.controls   # Clean shorthand notation alias

        # Input entries instantiation
        self.entry1               = tk.Entry(c, width=5)
        self.entry2               = tk.Entry(c, width=5)
        self.gender_entry         = tk.Entry(c, width=5)
        self.apoe4_male_entry     = tk.Entry(c, width=5)
        self.apoe4_female_entry   = tk.Entry(c, width=5)
        self.degrade_entry        = tk.Entry(c, width=5)
        self.year_entry           = tk.Entry(c, width=5)
        self.family_history_entry = tk.Entry(c, width=5)

        # Inject original configurations into fields
        self.entry1.insert(0,               str(config.DEFAULT_UNDER_20))
        self.entry2.insert(0,               str(config.DEFAULT_20_60))
        self.gender_entry.insert(0,         str(config.DEFAULT_MALE_RATIO))
        self.apoe4_male_entry.insert(0,     str(config.DEFAULT_APOE4_MALE))
        self.apoe4_female_entry.insert(0,   str(config.DEFAULT_APOE4_FEMALE))
        self.degrade_entry.insert(0,        str(config.DEFAULT_DEGRADE_RATE))
        self.year_entry.insert(0,           str(config.DEFAULT_SIM_YEARS))
        self.family_history_entry.insert(0, str(config.DEFAULT_FAMILY_HISTORY))

        # Functional interaction nodes setup
        set_btn   = tk.Button(c, text="Apply Input Parameters",  command=self.set_distribution)
        step_btn  = tk.Button(c, text="One Year Simulation",     command=self.simulate_year)
        run_btn   = tk.Button(c, text="Run Full Simulation",     command=self.run_simulation)
        reset_btn = tk.Button(c, text="Reset Simulation",        command=self.init_population)
        info_btn  = tk.Button(c, text="Alzheimer's Information", command=lambda: ui.show_info_window(self.root))

        # Form instruction helper note
        tk.Label(
            c,
            text="*Attention: Please Ensure That All Input Parameters Are In Decimals (e.g., 0.25 for 25%).*",
            fg="white", bg=config.COLOR_BG, font=("Arial", 10, "italic"),
        ).grid(row=0, column=2, columnspan=7, sticky="w", padx=5, pady=2)

        # Structural alignment grid configuration labels
        for col, text in enumerate([
            "% Under 20", "% 20–60", "% Male",
            "% APOE4 Male", "% APOE4 Female", "% Family History", "Degradation Rate",
        ]):
            tk.Label(c, text=text).grid(row=1, column=col, padx=3, pady=2)

        # Layout entry mapping grids
        for col, entry in enumerate([
            self.entry1, self.entry2, self.gender_entry,
            self.apoe4_male_entry, self.apoe4_female_entry,
            self.family_history_entry, self.degrade_entry,
        ]):
            entry.grid(row=2, column=col, padx=5, pady=2)

        # Form layout organization geometry anchors
        set_btn.grid(row=3, column=2, columnspan=3, padx=5, pady=5)

        tk.Label(c, text="Years of Simulation:").grid(row=4, column=1, padx=5, pady=2)
        self.year_entry.grid(row=4, column=2, padx=5, pady=2)
        step_btn.grid(row=4,  column=3, padx=5, pady=2)
        run_btn.grid(row=4,   column=4, padx=5, pady=2)
        reset_btn.grid(row=4, column=5, padx=5, pady=2)
        info_btn.grid(row=5,  column=2, columnspan=3, padx=5, pady=5)

    def _build_chart_tabs(self):
        """Creates and renders basic figure subplots inside the Matplotlib containers."""
        # Gender demographics profile trendline plot layout
        self.fig, self.ax1 = plt.subplots(figsize=(6, 4))
        self.chart = FigureCanvasTkAgg(self.fig, master=self.stats_tab)
        self.chart.get_tk_widget().pack()

        # Age group specific spread metrics bar graph layout
        self.age_fig, self.age_ax = plt.subplots(figsize=(5.5, 4))
        self.age_canvas = FigureCanvasTkAgg(self.age_fig, master=self.age_tab)
        self.age_canvas.get_tk_widget().pack()

        # Specific APOE4 occurrence distribution display metrics panel
        self.apoe_fig, self.apoe_ax = plt.subplots(figsize=(5.5, 4))
        self.apoe_canvas = FigureCanvasTkAgg(self.apoe_fig, master=self.apoe_tab)
        self.apoe_canvas.get_tk_widget().pack()

        # Stage distribution bar overview map
        self.stage_fig, self.stage_ax = plt.subplots(figsize=(5.5, 4))
        self.stage_canvas = FigureCanvasTkAgg(self.stage_fig, master=self.stage_tab)
        self.stage_canvas.get_tk_widget().pack()

    def set_distribution(self):
        """Parses, type-checks, and validates parameter fields to refresh the simulation.

        Raises:
            ValueError: If individual parameter entries breach physical boundary values 
                        or logic sums surpass unit scale constraints.
        """
        try:
            under_20   = float(self.entry1.get())
            between    = float(self.entry2.get())
            male_ratio = float(self.gender_entry.get())

            # Boundary rules check validation step
            if under_20 + between >= 1 or not (0 <= male_ratio <= 1):
                raise ValueError("Age fractions must sum to < 1 and male ratio must be 0–1.")

            # Assign valid attributes inside properties
            self.age_dist = {
                "under_20": under_20,
                "20_60":    between,
                "over_60":  1 - under_20 - between,
            }
            self.gender_ratio         = male_ratio
            self.apoe4_male_ratio     = float(self.apoe4_male_entry.get())
            self.apoe4_female_ratio   = float(self.apoe4_female_entry.get())
            self.family_history_ratio = float(self.family_history_entry.get())
            self.degrade_rate         = float(self.degrade_entry.get())

            # Instantly update data layer structure
            self.init_population()

        except Exception:
            messagebox.showerror("Input Error", "Invalid values.")

    def init_population(self):
        """Wipes active iteration state history to generate a clean population grid."""
        self.people             = []
        self.bubble_refs        = {}
        self.history_by_gender  = {"Male": [], "Female": []}
        self.new_cases          = []
        self.selected_index     = None

        # Clean old popups safely
        if self.popup:
            self.popup.destroy()
            self.popup = None

        # Request new population generation tracking instances
        self.people = pop.generate_population(
            self.age_dist,
            self.gender_ratio,
            self.apoe4_male_ratio,
            self.apoe4_female_ratio,
            self.family_history_ratio,
        )

        # Push refreshed visual updates straight to simulation element canvas layouts
        ui.draw_population(self.canvas, self.people, self.bubble_refs, self.selected_index)

    def simulate_year(self):
        """Advances structural simulation age states forward by an annual milestone cycle."""
        pop.simulate_year(
            self.people,
            self.degrade_rate,
            self.history_by_gender,
            self.new_cases,
        )
        # Redraw active changes onto viewport
        ui.draw_population(self.canvas, self.people, self.bubble_refs, self.selected_index)

    def run_simulation(self):
        """Processes continuous, multi-step iterations with automated window state cycles."""
        years = int(self.year_entry.get())
        for _ in range(years):
            self.simulate_year()
            self.root.update()      # Forces immediate window interface redraw step
            self.root.after(300)    # Delays loop execution to keep animation fluid and trackable
        self._update_plots()

    def _update_plots(self):
        """Redraws updated vector data onto target tracking charts."""
        charts.update_gender_chart(self.ax1,     self.chart,        self.history_by_gender)
        charts.update_age_chart   (self.age_ax,  self.age_canvas,   self.people)
        charts.update_apoe_chart  (self.apoe_ax, self.apoe_canvas,  self.people)
        charts.update_stage_chart (self.stage_ax, self.stage_canvas, self.people)

    def _on_click(self, event):
        """Resolves target spatial grid coordinates to highlight selected patient properties.

        Args:
            event (tk.Event): Standard Mouse click click tracking context parameters.
        """
        index = ui.find_clicked_person(event, self.bubble_refs)
        if index is not None:
            self.selected_index = index
            # Visual highlight refresh step
            ui.draw_population(self.canvas, self.people, self.bubble_refs, self.selected_index)
            # Create interactive profile visualization popups
            self.popup = ui.show_person_popup(self.root, self.people[index], self._on_popup_close)

    def _on_popup_close(self):
        """Cleans lingering sub-window element states safely upon dismissal."""
        if self.popup:
            self.popup.destroy()
            self.popup = None
        self.selected_index = None
        # Remove individual graphical overlay highlights safely from canvas grids
        ui.draw_population(self.canvas, self.people, self.bubble_refs, self.selected_index)

def main():
    """Application engine initiation initialization sequence point."""
    root = tk.Tk()
    AlzheimerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()