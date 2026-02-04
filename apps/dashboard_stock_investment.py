# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "altair>=6.0.0",
#     "marimo>=0.19.6",
#     "numpy>=2.4.1",
#     "polars>=1.37.1",
# ]
# ///

import marimo

__generated_with = "0.19.7"
app = marimo.App(
    width="columns",
    layout_file="layouts/dashboard_stock_investment.grid.json",
)

with app.setup:
    # for publishing on github pages it is recommended to have this in its own cell
    import marimo as mo


@app.cell
def _():
    import polars as pl
    import altair as alt
    import numpy as np
    import math
    import time
    import functools
    return alt, functools, math, np, pl, time


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # App elements
    """)
    return


@app.cell
def _():
    mo.sidebar(
        [
            mo.md("# Invest away"),
            mo.nav_menu(
                {
                    "#/": "Home",
                    "#/page1": "Stock investment",
                    "#/page2": "Mortage",
                    "#/page3": "Info",
                },
                orientation="vertical",
            ),
        ]
    )
    return


@app.cell
def _(page_mortgage, stock_page):
    # Page 2: info text
    def page2():
        return mo.vstack(
            [
                mo.md("## Info"),
                mo.md(
                    "App is created for testing and learning puroses, there are no garantee that there are no faults in the logic behind."
                ),
            ]
        )

    # Home page (optional)
    def home():
        header_text = mo.md("## Welcome to my investment calculator.")
        main_text = mo.md(
            "The only page that works for now is the stock investment page. It can show you how monthly investment can lead to big gains in the long run. You can also toy with alternative futures, by creating different scenarios and compare how the outcome changes in the long run."
        )

        return mo.vstack(items=[header_text, main_text])

    # Route table: this is what changes when you click the menu
    mo.routes(
        {
            "#/": home,
            "#/page1": stock_page,
            "#/page2": page_mortgage,
            "#/page3": page2,
            mo.routes.CATCH_ALL: home,
        }
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Stock investment calculator
    """)
    return


@app.cell
def _(figure, time_slider, ui_sliders_alternatives):
    stock_page = mo.vstack(
        items=[
            mo.hstack(items=[figure, time_slider], align="center"),
            ui_sliders_alternatives,
        ]
    )
    stock_page
    return (stock_page,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Mortgage calculator
    """)
    return


@app.cell
def _(figure, time_slider, ui_sliders_alternatives_mortgage):
    page_mortgage = mo.vstack(
        items=[
            mo.hstack(items=[figure, time_slider], align="center"),
            ui_sliders_alternatives_mortgage,
        ]
    )
    page_mortgage
    return (page_mortgage,)


@app.cell(column=1, hide_code=True)
def _():
    mo.md(r"""
    # Development
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Loan calculator
    """)
    return


@app.cell
def _(MAX_SCENARIOS):
    get_scenarios_mortgage, set_scenarios_mortgage = mo.state(
        [
            {
                "loan_amount": 3_000_000,
                "annual_interest_rate": 4.0,
                "loan_term_years": 25,
                "annual_inflation": 2.0,
            }
        ]
        * MAX_SCENARIOS
    )

    get_visible_count_mortgage, set_visible_count_mortgage = mo.state(1)
    return (
        get_scenarios_mortgage,
        get_visible_count_mortgage,
        set_scenarios_mortgage,
        set_visible_count_mortgage,
    )


@app.cell
def _(
    create_scenario_sliders_mortgage,
    get_scenarios_mortgage,
    get_visible_count_mortgage,
    set_scenarios_mortgage,
):
    scenarios_mortgage = get_scenarios_mortgage()
    visible_count_mortgage = get_visible_count_mortgage()

    alternatives_mortgage = mo.ui.array(
        [
            create_scenario_sliders_mortgage(
                values=s, color_index=i, scenario_setter=set_scenarios_mortgage
            )
            for i, s in enumerate(scenarios_mortgage[:visible_count_mortgage])
        ]
    )
    return (alternatives_mortgage,)


@app.cell
def _(creator_step_range):
    def create_scenario_sliders_mortgage(values, color_index, scenario_setter):
        _show_value = True
        _full_width = True
        slider_dict = mo.ui.dictionary(
            {
                "loan_amount": mo.ui.slider(
                    steps=creator_step_range(min_val=1e6, max_val=1e8),
                    value=values["loan_amount"],
                    debounce=True,
                    show_value=_show_value,
                    full_width=_full_width,
                    label=f"Loan amount",
                ),
                "annual_interest_rate": mo.ui.slider(
                    start=0.0,
                    stop=10.0,
                    step=0.25,
                    value=values["annual_interest_rate"],
                    debounce=True,
                    show_value=_show_value,
                    full_width=_full_width,
                    label=f"Annual interest rate (%)",
                ),
                "loan_term_years": mo.ui.slider(
                    start=0.0,
                    stop=40.0,
                    value=values["loan_term_years"],
                    step=1,
                    debounce=True,
                    show_value=_show_value,
                    full_width=_full_width,
                    label="Loan term years",
                ),
                "annual_inflation": mo.ui.slider(
                    start=0.0,
                    stop=10.0,
                    value=values["annual_inflation"],
                    step=0.1,
                    debounce=True,
                    show_value=_show_value,
                    full_width=_full_width,
                    label="Annual inflation (%)",
                ),
            },
            # Needed to not reset sliders when an alternative is added or removed
            on_change=lambda new_vals: scenario_setter(
                lambda scenarios: [
                    (new_vals if i == color_index else s)
                    for i, s in enumerate(scenarios)
                ]
            ),
        )
        return slider_dict
    return (create_scenario_sliders_mortgage,)


@app.cell
def _(alternatives_mortgage, mortgage_monthly, pl):
    df_alternatives_mortgage = []
    for j, alternative_mortgage in enumerate(alternatives_mortgage):
        df_mortgage = mortgage_monthly(
            loan_amount=alternative_mortgage["loan_amount"].value,
            annual_interest_rate=alternative_mortgage["annual_interest_rate"].value,
            loan_term_years=int(alternative_mortgage["loan_term_years"].value),
            annual_inflation=alternative_mortgage["annual_inflation"].value,
            rentefradrag=False,
        )
        df_mortgage = df_mortgage.with_columns(
            pl.lit(f"Alternative {j + 1}").alias("Alternative")
        )
        df_alternatives_mortgage.append(df_mortgage)
    return


@app.cell
def _(COLORS):
    def render_scenario_sliders_mortgage(scenario_dict, color_index):
        color = COLORS[color_index % len(COLORS)]
        rendered_sliders = mo.hstack(
            [
                scenario_dict["loan_amount"],
                scenario_dict["annual_interest_rate"],
                scenario_dict["loan_term_years"],
                scenario_dict["annual_inflation"],
            ]
        )
        # return rendered_sliders
        colored_sliders = mo.vstack([rendered_sliders]).style(
            {
                "border-left": f"4px solid {color}",
                "padding-left": "10px",
                "margin": "10px 0",
            }
        )
        return colored_sliders
    return (render_scenario_sliders_mortgage,)


@app.cell
def _(MAX_SCENARIOS, MIN_SCENARIOS, set_visible_count_mortgage):
    add_button_mortgage = mo.ui.button(
        label="Add alternative",
        on_change=lambda _: set_visible_count_mortgage(
            lambda count: min(count + 1, MAX_SCENARIOS)
        ),
    )

    remove_button_mortgage = mo.ui.button(
        label="Remove alternative",
        on_change=lambda _: set_visible_count_mortgage(
            lambda count: max(count - 1, MIN_SCENARIOS)
        ),
    )
    return add_button_mortgage, remove_button_mortgage


@app.cell
def _(
    MAX_SCENARIOS,
    MIN_SCENARIOS,
    add_button_mortgage,
    alternatives_mortgage,
    get_visible_count_mortgage,
    left_buttons,
    remove_button_mortgage,
    render_scenario_sliders_mortgage,
):
    left_buttons_mortgage = []
    right_buttons_mortgage = []

    if get_visible_count_mortgage() < MAX_SCENARIOS:
        left_buttons_mortgage.append(add_button_mortgage)
    if get_visible_count_mortgage() > MIN_SCENARIOS:
        right_buttons_mortgage.append(remove_button_mortgage)

    ui_sliders_alternatives_mortgage = mo.vstack(
        [
            *[
                render_scenario_sliders_mortgage(alternative, i)
                for i, alternative in enumerate(alternatives_mortgage)
            ],
            mo.hstack(
                [
                    mo.hstack(left_buttons_mortgage) if left_buttons else mo.Html(""),
                    mo.hstack(right_buttons_mortgage, justify="end")
                    if right_buttons_mortgage
                    else mo.Html(""),
                ]
            ),
        ]
    )
    return (ui_sliders_alternatives_mortgage,)


@app.cell
def _(ui_sliders_alternatives_mortgage):
    ui_sliders_alternatives_mortgage
    return


@app.cell(column=2, hide_code=True)
def _():
    mo.md(r"""
    # Code that runs
    """)
    return


@app.cell
def _(MAX_SCENARIOS):
    # === STATE ===
    get_scenarios, set_scenarios = mo.state(
        [
            {
                "initial_stock_investment": 500_000,
                "monthly_stock_investment": 5_000,
                "annual_stock_return": 10.0,
                "annual_inflation": 2.0,
            }
        ]
        * MAX_SCENARIOS
    )
    get_visible_count, set_visible_count = mo.state(1)
    return get_scenarios, get_visible_count, set_scenarios, set_visible_count


@app.cell
def _(MAX_SCENARIOS, MIN_SCENARIOS, set_visible_count):
    add_button = mo.ui.button(
        label="Add alternative",
        on_change=lambda _: set_visible_count(
            lambda count: min(count + 1, MAX_SCENARIOS)
        ),
    )

    remove_button = mo.ui.button(
        label="Remove alternative",
        on_change=lambda _: set_visible_count(
            lambda count: max(count - 1, MIN_SCENARIOS)
        ),
    )
    return add_button, remove_button


@app.cell
def _(
    create_scenario_sliders_stock_investment,
    get_scenarios,
    get_visible_count,
    set_scenarios,
):
    # === BUILD UI ===
    scenarios = get_scenarios()
    visible_count = get_visible_count()

    alternatives = mo.ui.array(
        [
            create_scenario_sliders_stock_investment(
                values=s, color_index=i, scenario_setter=set_scenarios
            )
            for i, s in enumerate(scenarios[:visible_count])
        ]
    )
    return (alternatives,)


@app.cell
def _(alternatives, pl, time_slider, wrapper_stock_investment_monthly):
    # === USE DATA ===
    df_alternatives = []
    for i, alternative in enumerate(alternatives):
        df = wrapper_stock_investment_monthly(alternative, time_slider)
        df = df.with_columns(pl.lit(f"Alternative {i + 1}").alias("Alternative"))
        df_alternatives.append(df)
    return (df_alternatives,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Sliders
    """)
    return


@app.cell
def _(FULL_WIDTH, SHOW_VALUE):
    time_slider = mo.ui.slider(
        start=1,
        stop=30,
        value=20,
        debounce=True,
        show_value=SHOW_VALUE,
        full_width=FULL_WIDTH,
        label="Projection horizon (years)",
    )
    return (time_slider,)


@app.cell
def _(
    MAX_SCENARIOS,
    MIN_SCENARIOS,
    add_button,
    alternatives,
    get_visible_count,
    remove_button,
    render_scenario_sliders,
):
    left_buttons = []
    right_buttons = []

    if get_visible_count() < MAX_SCENARIOS:
        left_buttons.append(add_button)
    if get_visible_count() > MIN_SCENARIOS:
        right_buttons.append(remove_button)

    ui_sliders_alternatives = mo.vstack(
        [
            *[
                render_scenario_sliders(alternative, i)
                for i, alternative in enumerate(alternatives)
            ],
            mo.hstack(
                [
                    mo.hstack(left_buttons) if left_buttons else mo.Html(""),
                    mo.hstack(right_buttons, justify="end")
                    if right_buttons
                    else mo.Html(""),
                ]
            ),
        ]
    )
    return left_buttons, ui_sliders_alternatives


@app.cell
def _(df_alternatives, plot):
    figure = plot(df_alternatives=df_alternatives)
    return (figure,)


@app.cell(column=3, hide_code=True)
def _():
    mo.md(r"""
    # Functions and imports
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Constants
    """)
    return


@app.cell
def _():
    MIN_SCENARIOS = 1
    MAX_SCENARIOS = 4

    COLORS = [
        "#3498db",  # blue
        "#e74c3c",  # red
        "#9b59b6",  # purple
        "#f39c12",  # orange
        "#2ecc71",  # green
        "#1abc9c",  # turquoise
        "#e67e22",  # dark orange
        "#95a5a6",  # gray
    ]

    SHOW_VALUE = True
    FULL_WIDTH = True
    return COLORS, FULL_WIDTH, MAX_SCENARIOS, MIN_SCENARIOS, SHOW_VALUE


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Stock investment elements
    """)
    return


@app.cell
def _(COLORS):
    def render_scenario_sliders(scenario_dict, color_index):
        color = COLORS[color_index % len(COLORS)]
        rendered_sliders = mo.hstack(
            [
                scenario_dict["initial_stock_investment"],
                scenario_dict["monthly_stock_investment"],
                scenario_dict["annual_stock_return"],
                scenario_dict["annual_inflation"],
            ]
        )
        # return rendered_sliders
        colored_sliders = mo.vstack([rendered_sliders]).style(
            {
                "border-left": f"4px solid {color}",
                "padding-left": "10px",
                "margin": "10px 0",
            }
        )
        return colored_sliders
    return (render_scenario_sliders,)


@app.cell
def _(math, np):
    def creator_step_range(min_val=1000, max_val=1e6):
        # zero is always included
        a = 1
        b = 2
        c = 4

        values = [0]

        if min_val > 0:
            magnitude = 10 ** (math.floor(math.log10(min_val)) - 1)
        else:
            magnitude = 1

        while magnitude <= max_val:
            # fine steps
            values.extend(np.arange(a * magnitude, b * magnitude, magnitude / 10))

            values.extend(np.arange(b * magnitude, c * magnitude, magnitude / 5))

            # coarser steps
            values.extend(np.arange(c * magnitude, a * magnitude * 10, magnitude / 2))

            magnitude *= 10

        # filter + clean
        values = np.array(values)
        values = values[(values == 0) | ((values >= min_val) & (values <= max_val))]
        return np.unique(values).tolist()
    return (creator_step_range,)


@app.cell
def _(creator_step_range):
    # === SLIDER CREATOR ===
    def create_scenario_sliders_stock_investment(values, color_index, scenario_setter):
        _show_value = True
        _full_width = True
        slider_dict = mo.ui.dictionary(
            {
                "initial_stock_investment": mo.ui.slider(
                    steps=creator_step_range(min_val=1e4, max_val=1e7),
                    value=values["initial_stock_investment"],
                    debounce=True,
                    show_value=_show_value,
                    full_width=_full_width,
                    label=f"Initial stock investment",
                ),
                "monthly_stock_investment": mo.ui.slider(
                    steps=creator_step_range(min_val=1e2, max_val=1e6),
                    value=values["monthly_stock_investment"],
                    debounce=True,
                    show_value=_show_value,
                    full_width=_full_width,
                    label=f"Monthly stock investment",
                ),
                "annual_stock_return": mo.ui.slider(
                    start=0.0,
                    stop=15.0,
                    value=values["annual_stock_return"],
                    step=0.5,
                    debounce=True,
                    show_value=_show_value,
                    full_width=_full_width,
                    label="Annual stock return (%)",
                ),
                "annual_inflation": mo.ui.slider(
                    start=0.0,
                    stop=10.0,
                    value=values["annual_inflation"],
                    step=0.1,
                    debounce=True,
                    show_value=_show_value,
                    full_width=_full_width,
                    label="Annual inflation (%)",
                ),
            },
            # When ANY slider changes, update ONLY this scenario's data
            on_change=lambda new_vals: scenario_setter(
                lambda scenarios: [
                    (new_vals if i == color_index else s)
                    for i, s in enumerate(scenarios)
                ]
            ),
        )
        return slider_dict
    return (create_scenario_sliders_stock_investment,)


@app.cell
def _(stock_investment_monthly):
    def wrapper_stock_investment_monthly(sliders, time_slider):
        df = stock_investment_monthly(
            initial_investment=sliders["initial_stock_investment"].value,
            monthly_contribution=sliders["monthly_stock_investment"].value,
            annual_return=sliders["annual_stock_return"].value / 100,
            years=time_slider.value,
            annual_inflation=sliders["annual_inflation"].value / 100,
        )
        return df
    return (wrapper_stock_investment_monthly,)


@app.cell
def _(COLORS, alt, pl):
    def plot(df_alternatives, COLORS=COLORS):
        full_df = pl.concat(df_alternatives)
        # Transform from wide to long
        long_df = full_df.unpivot(
            index=["month", "Alternative"],
            on=["balance", "returns_cum", "contributions_cum"],
            variable_name="Metric",
            value_name="Amount",
        )
        selection = alt.selection_point(
            fields=["Alternative"], bind="legend", toggle="true"
        )
        selection_metric = alt.selection_point(
            fields=["Metric"], bind="legend", toggle="true"
        )

        chart = (
            alt.Chart(long_df)
            .mark_line()
            .encode(
                x=alt.X(
                    "month:Q",
                    title="Year",
                    axis=alt.Axis(
                        labelExpr="datum.value / 12",
                        values=list(range(0, 1000, 12)),
                        format="d",
                    ),
                ),
                y=alt.Y("Amount:Q", title="Amount"),
                color=alt.Color(
                    "Alternative:N",
                    scale=alt.Scale(range=COLORS[: len(df_alternatives)]),
                    legend=alt.Legend(title="Scenario"),
                ),
                # This creates the second legend and controls line style
                strokeDash=alt.StrokeDash(
                    "Metric:N",
                    scale=alt.Scale(
                        domain=["balance", "returns_cum", "contributions_cum"],
                        range=[[], [5, 5], [2, 2]],  # Solid, Dashed, Dotted
                    ),
                    legend=alt.Legend(title="Metric Toggle"),
                ),
                tooltip=["Alternative:N", "Metric:N", "month:Q", "Amount:Q"],
                # Apply both interactive filters
                opacity=alt.condition(
                    selection & selection_metric, alt.value(1), alt.value(0.1)
                ),
            )
            .add_params(selection, selection_metric)  # Register both legends
            .properties(
                title="Portfolio Projections - All Alternatives", width=600, height=400
            )
            .interactive()
        )

        return chart
    return (plot,)


@app.cell(column=4, hide_code=True)
def _():
    mo.md(r"""
    # Functions that i have/had in src/utils.py
    """)
    return


@app.cell
def _(functools, time):
    def timer(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                elapsed = time.perf_counter() - start
                print(f"{func.__name__} took {elapsed:.6f}s")

        return wrapper
    return (timer,)


@app.cell
def _(pl):
    def apply_inflation(
        df: pl.DataFrame, annual_inflation: float, columns: list[str]
    ) -> pl.DataFrame:
        if annual_inflation == 0.0:
            return df

        monthly_inflation = (1 + annual_inflation) ** (1 / 12) - 1
        # Assumes df has a "month" column starting at 0. This speeds up computation.
        inflation_factor = (1 + monthly_inflation) ** pl.col("month")
        df = df.with_columns(
            [(pl.col(col) / inflation_factor).alias(col) for col in columns]
        )

        return df
    return (apply_inflation,)


@app.cell
def _(apply_inflation, pl, timer):
    @timer
    def stock_investment_monthly(
        initial_investment: float,
        monthly_contribution: float,
        annual_return: float,
        years: int,
        annual_inflation: float = 0.0,
        tax_rate: float = 0.3784,  # 37.84% tax on returns
    ) -> pl.DataFrame:
        n_months = years * 12
        monthly_return = (1 + annual_return) ** (1 / 12) - 1

        # Create base dataframe with months
        df = pl.DataFrame(
            {
                "month": pl.arange(0, n_months + 1, eager=True),
            }
        )

        df = (
            df.with_columns(
                [
                    (pl.col("month") // 12).alias("year"),
                    # Balance calculation using compound interest formula
                    (
                        initial_investment * ((1 + monthly_return) ** pl.col("month"))
                        + monthly_contribution
                        * (
                            ((1 + monthly_return) ** pl.col("month") - 1)
                            / monthly_return
                        )
                    ).alias("balance"),
                    # Contributions: simple linear growth
                    (initial_investment + monthly_contribution * pl.col("month")).alias(
                        "contributions_cum"
                    ),
                ]
            )
            .with_columns(
                [
                    (pl.col("balance") - pl.col("contributions_cum")).alias(
                        "returns_cum"
                    ),
                ]
            )
            .with_columns(
                [
                    (pl.col("returns_cum") * (1 - tax_rate)).alias("returns_after_tax"),
                    (
                        pl.col("contributions_cum")
                        + pl.col("returns_cum") * (1 - tax_rate)
                    ).alias("stock_equity"),
                ]
            )
        )
        df = apply_inflation(
            df,
            annual_inflation,
            [
                "balance",
                "contributions_cum",
                "returns_cum",
                "returns_after_tax",
                "stock_equity",
            ],
        )
        return df
    return (stock_investment_monthly,)


@app.cell
def _(apply_inflation, pl, timer):
    @timer
    def mortgage_monthly(
        loan_amount: float,
        annual_interest_rate: float,
        loan_term_years: int,
        annual_inflation: float = 0.0,
        rentefradrag: bool = True,
    ) -> pl.DataFrame:
        n_months = loan_term_years * 12
        r_monthly = annual_interest_rate / 12.0

        loan_payment = (
            loan_amount
            * r_monthly
            * (1 + r_monthly) ** n_months
            / ((1 + r_monthly) ** n_months - 1)
        )

        balance = [loan_amount]
        interest = [0.0]  # Interest paid each month
        tax_deductions = [0.0]  # Tax savings each month
        net_costs = [0.0]  # Net cost after tax savings
        principal_cum = [0.0]
        interest_cum = [0.0]

        for m in range(1, n_months + 1):
            interest_payment = balance[-1] * r_monthly
            principal_payment = loan_payment - interest_payment
            new_balance = max(0, balance[-1] - principal_payment)

            tax_deduction = interest_payment * 0.22 if rentefradrag else 0.0
            net_cost = loan_payment - tax_deduction

            balance.append(new_balance)
            interest.append(interest_payment)
            tax_deductions.append(tax_deduction)
            net_costs.append(net_cost)
            principal_cum.append(principal_cum[-1] + principal_payment)
            interest_cum.append(interest_cum[-1] + interest_payment)

        df = pl.DataFrame(
            {
                "month": list(range(n_months + 1)),
                "year": [m // 12 for m in range(n_months + 1)],
                "loan_payment": [0.0] + [loan_payment] * n_months,
                "interest": interest,
                "tax_deduction": tax_deductions,
                "net_cost": net_costs,  # What it actually costs you
                "loan_balance": balance,
                "principal_cum": principal_cum,
                "interest_cum": interest_cum,
            },
            schema={
                "month": pl.Int64,
                "year": pl.Int64,
                "loan_payment": pl.Float64,
                "interest": pl.Float64,
                "tax_deduction": pl.Float64,
                "net_cost": pl.Float64,
                "loan_balance": pl.Float64,
                "principal_cum": pl.Float64,
                "interest_cum": pl.Float64,
            },
        )

        df = apply_inflation(
            df,
            annual_inflation,
            [
                "loan_payment",
                "interest",
                "tax_deduction",
                "net_cost",
                "loan_balance",
                "principal_cum",
                "interest_cum",
            ],
        )

        return df
    return (mortgage_monthly,)


if __name__ == "__main__":
    app.run()
