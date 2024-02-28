# imports
import pandas as pd
import lets_plot as lp
import numpy as np
from shiny import App, Inputs, Outputs, Session, reactive, render, req, ui

# lets-plot setup
lp.LetsPlot.setup_html()

# create full and tidy data
nfl = pd.read_csv("data/nfl.csv")
teams = pd.read_csv("data/teams.csv")
nfl = nfl.merge(teams, how="left", left_on="team", right_on="full_name")
nfl.drop(["abbreviation", "full_name"], axis=1, inplace=True)

# get conference and division lists for dropdown menus
conferences = ["AFC", "NFC"]
divisions = nfl["division"].unique().tolist()

# calculate consistent limits for differential axis labels
diff_abs_max = np.max(np.abs([nfl["differential"].min(), nfl["differential"].max()]))
diff_min = -diff_abs_max
diff_max = diff_abs_max

# setup ui
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_selectize("conference", "Conference", conferences, selected="AFC"),
        ui.input_selectize("division", "Division", divisions, selected="East"),
        ui.input_slider("week", "Week", 1, 18, 18),
    ),
    ui.card(
        ui.output_ui("plot"),
    ),
    ui.card(
        ui.output_data_frame("division_table"),
    ),
)


# setup server
def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Calc
    def filtered_df() -> pd.DataFrame:

        df = nfl[nfl["conference"] == input.conference()]
        df = df[df["division"] == input.division()]
        return df

    @reactive.Calc
    def season_table() -> pd.DataFrame:

        df = filtered_df()
        df = df[df["week"] == input.week()]
        return df

    @render.ui
    def plot():
        p = (
            lp.ggplot(filtered_df(), lp.aes(x="week", y="differential", color="team"))
            + lp.geom_path(tooltips=lp.layer_tooltips().line("Team: @team").line("Record: @wins - @losses"))
            + lp.ggsize(width=1000, height=700)
            + lp.ylim(diff_min, diff_max)
            + lp.labs(x="Week", y="Win-Loss Differential")
        )
        phtml = lp._kbridge._generate_static_html_page(p.as_dict(), iframe=True)
        return ui.HTML(phtml)

    @render.data_frame
    def division_table():
        return render.DataGrid(season_table())


# run app
app = App(app_ui, server)
