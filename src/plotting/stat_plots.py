import altair as alt
import numpy as np
import pandas as pd

from ..constants import PLOT_HEIGHT, PLOT_WIDTH


def pairplot(
    df: pd.DataFrame, color: str = "dodgerblue", opacity: float = 0.25, width: int = 180
) -> alt.RepeatChart:
    return (
        alt.Chart(df)
        .mark_circle(color=color, opacity=opacity)
        .encode(
            alt.X(
                alt.repeat("column"), type="quantitative", scale=alt.Scale(zero=False)
            ),
            alt.Y(alt.repeat("row"), type="quantitative", scale=alt.Scale(zero=False)),
        )
        .properties(
            height=PLOT_HEIGHT / 3,
            width=width,
        )
        .repeat(row=list(df.columns), column=list(df.columns))
    )


def disrete_histogram(
    df: pd.DataFrame, col: str, color: str = "dodgerblue", opacity: float = 0.75
) -> alt.Chart:
    return (
        alt.Chart(df)
        .mark_bar(color=color, opacity=opacity)
        .encode(
            alt.X(
                f"{col}:Q",
                bin=alt.Bin(step=1),
            ),
            alt.Y("count():Q"),
        )
        .properties(height=PLOT_HEIGHT, width=PLOT_WIDTH)
    )


def hist_dist_plot(
    df: pd.DataFrame,
    col: str,
    scipy_dist,
    title: str | None = None,
    hist_color: str = "dodgerblue",
    hist_opacity: float = 0.75,
    pdf_color: str = "red",
) -> alt.LayerChart:
    """
    Take a pd.Series from a DataFrame and a scipy distribution and create a histogram
    and pdf plot showing the quality of the distribution fit.
    """

    # Data histogram
    histplot = (
        alt.Chart(df)
        .mark_bar(color=hist_color, opacity=hist_opacity)
        .encode(
            alt.X(f"value:Q"),
            alt.Y(
                "density:Q",
                title="",
                axis=alt.Axis(labels=False, ticks=False, grid=False, domain=False),
            ),
        )
        .transform_density(col, as_=["value", "density"])
        .properties(
            title=title if title else "",
            height=PLOT_HEIGHT,
            width=PLOT_WIDTH,
        )
    )

    # Fitted PDF
    x_range = np.linspace(df[col].min(), df[col].max(), 250)

    distplot = (
        alt.Chart(pd.DataFrame({col: x_range, "PDF": scipy_dist.pdf(x_range)}))
        .mark_line(color=pdf_color)
        .encode(
            alt.X(f"{col}:Q"),
            alt.Y(
                "PDF:Q",
                title="",
                axis=alt.Axis(labels=False, ticks=False, title=None),
            ),
        )
    )

    return (histplot + distplot).resolve_axis(x="shared", y="independent")
