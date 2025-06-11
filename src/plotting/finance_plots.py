import numpy as np
import pandas as pd
import altair as alt

from ..constants import PLOT_HEIGHT, PLOT_WIDTH


def simulated_portfolio_plot(
    simulated_balance: np.ndarray,
    dates,
    sims: int,
    title: str | None = None,
    ) -> alt.Chart:

    sims = min(sims, simulated_balance.shape[-1])

    df = (
        pd.concat([
            pd.DataFrame({
                'Date': dates,
                '$': simulated_balance[:, i],
                'Simulation': i
            })
            for i in range(sims)
        ], 
        ignore_index=True)
    )

    chart = (
        alt.Chart(df)
        .mark_line(
            strokeWidth=1,
            opacity=0.75
        )
        .encode(
            alt.X('Date:T', title=""),
            alt.Y('$:Q'),
            color=alt.Color('Simulation:N', legend=None),
        )
        .properties(
            title=title,
            height=PLOT_HEIGHT,
            width=PLOT_WIDTH,
        )
    )

    return chart
