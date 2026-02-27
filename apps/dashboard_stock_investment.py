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

__generated_with = "0.20.2"
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
                    "#/page2": "Mortage cost",
                    "#/page3": "Info",
                    # "#/page4": "test",
                },
                orientation="vertical",
            ),
        ]
    )
    return


@app.cell
def _(page_mortgage, page_stock):
    # Route table: this is what changes when you click the menu
    mo.routes(
        {
            "#/": page_home,
            "#/page1": page_stock,
            "#/page2": page_mortgage,
            "#/page3": page_info,
            # "#/page4": page_test,

            mo.routes.CATCH_ALL: page_home,
        }
    )
    return


@app.function
def page_setup(header:str|None=None, text:any|None=None, page_content:any|None=None, footer:any|None=None):
    mo_elem = []
    if header:
        mo_elem.append(mo.md(f"## {header}"))
    if text:
        mo_elem.append(text)
    if page_content:
        mo_elem.append(page_content)
    if footer:
        mo_elem.append(footer)
    page = mo.vstack(
        items=mo_elem, align="center"
    )
    return page


@app.cell
def _():
    page_home()
    return


@app.function
def page_home():
    header_str = "Welcome to Invest Away!"
    text = mo.md(
        "Theis is a small app for playing around with parameters for financial settings, where you can also setup altenatives where you compare different scenarios easily! There are two calculators as of now that you find in the navigation menu."
    )

    page=page_setup(header=header_str,text=text, page_content=None,footer=None)

    return page


@app.function
def page_info():
    header_str = "Info"
    text = mo.md(
                "This app is made as a home project for fun, there are no garantees that the logic is sound."
            )
    
    page=page_setup(header=header_str,text=text, page_content=None,footer=None)

    return page


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Stock investment calculator
    """)
    return


@app.cell
def _(figure_stock, time_slider, ui_sliders_stock):
    def page_stock():
        header_text = mo.md("## Stock investment calculator")
        text = mo.md("The calculator shows you how big the difference really is when the assumptions change! See the difference clearly in the graph by adding the alternatives an set them up how you like. A small change can lead to big gains in the long run.")
        page = mo.vstack(
            items=[
                header_text,
                text,
                mo.hstack(items=[figure_stock, time_slider], align="center"),
                ui_sliders_stock,
            ], align="center"
        )
        return page

    return (page_stock,)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Mortgage calculator
    """)
    return


@app.cell
def _(figure_mortgage, ui_sliders_mortgage):
    def page_mortgage():
        header_text = mo.md("## Mortgage calculator")
        page = mo.vstack(
            items=[
                header_text,
                figure_mortgage,
                ui_sliders_mortgage,
            ], align="center"
        )
        return page

    return (page_mortgage,)


@app.cell
def _(figure_mortgage, ui_sliders_mortgage):
    page_mortgage2 = mo.vstack(
        items=[
            figure_mortgage,
            ui_sliders_mortgage,
        ]
    )
    page_mortgage2
    return


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
def _(create_add_remove_buttons):
    default_slider_vals_mortgage = {
        "loan_amount": 3_000_000,
        "annual_interest_rate": 4.0,
        "loan_term_years": 25,
        "annual_inflation": 2.0,
    }

    (
        get_scenarios_mortgage,
        set_scenarios_mortgage,
        get_visible_count_mortgage,
        set_visible_count_mortgage,
    ) = create_scenario_manager(default_slider_vals_mortgage)

    add_button_mortgage, remove_button_mortgage = create_add_remove_buttons(
        set_visible_count_mortgage
    )
    return (
        add_button_mortgage,
        get_scenarios_mortgage,
        get_visible_count_mortgage,
        remove_button_mortgage,
        set_scenarios_mortgage,
    )


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
def _(
    add_button_mortgage,
    alternatives_mortgage,
    create_slider_ui,
    get_visible_count_mortgage,
    remove_button_mortgage,
    render_scenario_sliders_mortgage,
):
    ui_sliders_mortgage = create_slider_ui(
        alternatives_mortgage,
        render_scenario_sliders_mortgage,
        get_visible_count_mortgage,
        add_button_mortgage,
        remove_button_mortgage,
    )
    return (ui_sliders_mortgage,)


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
                loan_amount=scenario["loan_amount"],
                anual_interest_rate=scenario["annual_interest_rate"],
                loan_term_years=scenario["loan_term_years"],
                annual_inflation=scenario["annual_inflation"],
                color_index=i,
                scenario_setter=set_scenarios_mortgage,
            )
            for i, scenario in enumerate(scenarios_mortgage[:visible_count_mortgage])
        ]
    )
    return (alternatives_mortgage,)


@app.cell
def _(creator_step_range):
    def create_scenario_sliders_mortgage(
        loan_amount,
        anual_interest_rate,
        loan_term_years,
        annual_inflation,
        color_index,
        scenario_setter,
    ):
        _show_value = True
        _full_width = True
        slider_dict = mo.ui.dictionary(
            {
                "loan_amount": mo.ui.slider(
                    steps=creator_step_range(min_val=1e6, max_val=1e8),
                    value=loan_amount,
                    debounce=True,
                    show_value=_show_value,
                    full_width=_full_width,
                    label=f"Loan amount",
                ),
                "annual_interest_rate": mo.ui.slider(
                    start=0.0,
                    stop=10.0,
                    step=0.25,
                    value=anual_interest_rate,
                    debounce=True,
                    show_value=_show_value,
                    full_width=_full_width,
                    label=f"Annual interest rate (%)",
                ),
                "loan_term_years": mo.ui.slider(
                    start=0.0,
                    stop=40.0,
                    value=loan_term_years,
                    step=1,
                    debounce=True,
                    show_value=_show_value,
                    full_width=_full_width,
                    label="Loan term years",
                ),
                "annual_inflation": mo.ui.slider(
                    start=0.0,
                    stop=10.0,
                    value=annual_inflation,
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
                    (new_vals if i == color_index else s) for i, s in enumerate(scenarios)
                ]
            ),
        )
        return slider_dict

    return (create_scenario_sliders_mortgage,)


@app.cell
def _(alternatives_mortgage, mortgage_monthly, pl, plot):
    df_alternatives_mortgage = []
    for j, _alternative in enumerate(alternatives_mortgage):
        df_mortgage = mortgage_monthly(
            loan_amount=_alternative["loan_amount"].value,
            annual_interest_rate=_alternative["annual_interest_rate"].value / 100,
            loan_term_years=int(_alternative["loan_term_years"].value),
            annual_inflation=_alternative["annual_inflation"].value / 100,
            rentefradrag=False,
        )
        df_mortgage = df_mortgage.with_columns(
            pl.lit(f"Alternative {j + 1}").alias("Alternative")
        )
        df_alternatives_mortgage.append(df_mortgage)

    figure_mortgage = plot(
        df_alternatives=df_alternatives_mortgage,
        metric_columns=["loan_balance", "principal_cum", "interest_cum"],
    )
    return (figure_mortgage,)


@app.cell(column=2, hide_code=True)
def _():
    mo.md(r"""
    # Code that runs
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Stock investment calculator
    """)
    return


@app.cell
def _(create_add_remove_buttons):
    default_slider_vals_stock = {
        "initial_stock_investment": 500_000,
        "monthly_stock_investment": 5_000,
        "annual_stock_return": 10.0,
        "annual_inflation": 2.0,
    }

    (
        get_scenarios_stock,
        set_scenarios_stock,
        get_visible_count_stock,
        set_visible_count_stock,
    ) = create_scenario_manager(default_slider_vals_stock)

    add_button_stock, remove_button_stock = create_add_remove_buttons(
        set_visible_count_stock
    )
    return (
        add_button_stock,
        get_scenarios_stock,
        get_visible_count_stock,
        remove_button_stock,
        set_scenarios_stock,
    )


@app.cell
def _(COLORS):
    def render_scenario_sliders_stock(scenario_dict, color_index):
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

    return (render_scenario_sliders_stock,)


@app.cell
def _(
    add_button_stock,
    alternatives_stock,
    create_slider_ui,
    get_visible_count_stock,
    remove_button_stock,
    render_scenario_sliders_stock,
):
    ui_sliders_stock = create_slider_ui(
        alternatives_stock,
        render_scenario_sliders_stock,
        get_visible_count_stock,
        add_button_stock,
        remove_button_stock,
    )
    return (ui_sliders_stock,)


@app.cell
def _(
    create_scenario_sliders_stock_investment,
    get_scenarios_stock,
    get_visible_count_stock,
    set_scenarios_stock,
):
    # === BUILD UI ===
    scenarios_stock = get_scenarios_stock()
    visible_count = get_visible_count_stock()

    alternatives_stock = mo.ui.array(
        [
            create_scenario_sliders_stock_investment(
                initial_stock_investment=scenario["initial_stock_investment"],
                monthly_stock_investment=scenario["monthly_stock_investment"],
                annual_stock_return=scenario["annual_stock_return"],
                annual_inflation=scenario["annual_inflation"],
                color_index=i,
                scenario_setter=set_scenarios_stock,
            )
            for i, scenario in enumerate(scenarios_stock[:visible_count])
        ]
    )
    return (alternatives_stock,)


@app.cell
def _(creator_step_range):
    # === SLIDER CREATOR ===
    def create_scenario_sliders_stock_investment(
        initial_stock_investment,
        monthly_stock_investment,
        annual_stock_return,
        annual_inflation,
        color_index,
        scenario_setter,
    ):
        _show_value = True
        _full_width = True
        slider_dict = mo.ui.dictionary(
            {
                "initial_stock_investment": mo.ui.slider(
                    steps=creator_step_range(min_val=1e4, max_val=1e7),
                    value=initial_stock_investment,
                    debounce=True,
                    show_value=_show_value,
                    full_width=_full_width,
                    label=f"Initial stock investment",
                ),
                "monthly_stock_investment": mo.ui.slider(
                    steps=creator_step_range(min_val=1e2, max_val=1e6),
                    value=monthly_stock_investment,
                    debounce=True,
                    show_value=_show_value,
                    full_width=_full_width,
                    label=f"Monthly stock investment",
                ),
                "annual_stock_return": mo.ui.slider(
                    start=0.0,
                    stop=15.0,
                    value=annual_stock_return,
                    step=0.5,
                    debounce=True,
                    show_value=_show_value,
                    full_width=_full_width,
                    label="Annual stock return (%)",
                ),
                "annual_inflation": mo.ui.slider(
                    start=0.0,
                    stop=10.0,
                    value=annual_inflation,
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
                    (new_vals if i == color_index else s) for i, s in enumerate(scenarios)
                ]
            ),
        )
        return slider_dict

    return (create_scenario_sliders_stock_investment,)


@app.cell
def _(alternatives_stock, pl, plot, stock_investment_monthly, time_slider):
    df_alternatives_stock = []
    for i, _alternative in enumerate(alternatives_stock):
        df_stock = stock_investment_monthly(
            initial_investment=_alternative["initial_stock_investment"].value,
            monthly_contribution=_alternative["monthly_stock_investment"].value,
            annual_return=_alternative["annual_stock_return"].value / 100,
            years=time_slider.value,
            annual_inflation=_alternative["annual_inflation"].value / 100,
        )
        df_stock = df_stock.with_columns(
            pl.lit(f"Alternative {i + 1}").alias("Alternative")
        )
        df_alternatives_stock.append(df_stock)

    figure_stock = plot(
        df_alternatives=df_alternatives_stock,
        metric_columns=["balance", "returns_cum", "contributions_cum"],
    )
    return (figure_stock,)


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


@app.cell(column=3, hide_code=True)
def _():
    mo.md(r"""
    # Common functions for scenario sliders
    """)
    return


@app.function
def create_scenario_manager(default_values, max_scenarios: int = 4):
    get_scenarios, set_scenarios = mo.state([default_values] * max_scenarios)
    get_visible_count, set_visible_count = mo.state(1)
    return get_scenarios, set_scenarios, get_visible_count, set_visible_count


@app.cell
def _(MAX_SCENARIOS, MIN_SCENARIOS):
    def create_add_remove_buttons(set_visible_count_fn):
        add_button = mo.ui.button(
            label="Add alternative",
            on_change=lambda _: set_visible_count_fn(
                lambda count: min(count + 1, MAX_SCENARIOS)
            ),
        )
        remove_button = mo.ui.button(
            label="Remove alternative",
            on_change=lambda _: set_visible_count_fn(
                lambda count: max(count - 1, MIN_SCENARIOS)
            ),
        )
        return add_button, remove_button

    return (create_add_remove_buttons,)


@app.cell
def _(MAX_SCENARIOS, MIN_SCENARIOS):
    def create_slider_ui(
        alternatives, render_fn, get_visible_count_fn, add_button, remove_button
    ):
        left_buttons = []
        right_buttons = []
        if get_visible_count_fn() < MAX_SCENARIOS:
            left_buttons.append(add_button)
        if get_visible_count_fn() > MIN_SCENARIOS:
            right_buttons.append(remove_button)

        ui_sliders_alternatives = mo.vstack(
            [
                *[render_fn(alternative, i) for i, alternative in enumerate(alternatives)],
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
        return ui_sliders_alternatives

    return (create_slider_ui,)


@app.cell(column=4, hide_code=True)
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
def _(COLORS, alt, pl):
    def plot(df_alternatives, metric_columns=None, COLORS=COLORS):
        full_df = pl.concat(df_alternatives)
        # Transform from wide to long
        long_df = full_df.unpivot(
            index=["month", "Alternative"],
            on=metric_columns,
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
                        domain=metric_columns,
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
        )

        return chart

    return (plot,)


@app.cell(column=5, hide_code=True)
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
                        * (((1 + monthly_return) ** pl.col("month") - 1) / monthly_return)
                    ).alias("balance"),
                    # Contributions: simple linear growth
                    (initial_investment + monthly_contribution * pl.col("month")).alias(
                        "contributions_cum"
                    ),
                ]
            )
            .with_columns(
                [
                    (pl.col("balance") - pl.col("contributions_cum")).alias("returns_cum"),
                ]
            )
            .with_columns(
                [
                    (pl.col("returns_cum") * (1 - tax_rate)).alias("returns_after_tax"),
                    (
                        pl.col("contributions_cum") + pl.col("returns_cum") * (1 - tax_rate)
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
        annual_interest_rate: float,  # insert the decimal, not the percentage
        loan_term_years: int,
        annual_inflation: float = 0.0,  # insert the decimal, not the percentage
        rentefradrag: bool = True,
    ) -> pl.DataFrame:
        n_months = loan_term_years * 12
        r_monthly = annual_interest_rate / 12.0

        # Handle division by zero
        if r_monthly == 0:
            loan_payment = loan_amount / n_months
        else:
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
