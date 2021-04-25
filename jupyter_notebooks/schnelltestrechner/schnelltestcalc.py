import numpy as np
from ipywidgets import interact
import altair as alt
import pandas as pd
import scipy.stats
import logging

logger = logging


def normal_dens(mu, sigma, x):
    return (
        1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
    )


@interact(
    inzidenz=(1, 100_000),
    sensitivity=(0.0, 0.99, 0.01),
    specificity=(0.0, 0.99, 0.01),
    group_size=(1, 100_000),
)
def schnelltest_calculator(inzidenz=200, sensitivity=0.97, specificity=0.99, group_size=5_000):

    # inzident bedeutet infizierte je 100.000 Einwohner. 
    # Richtigerweise müssten wir die tatsächliche Anzahl infizierter wissen, 
    # da dies jedoch unbekannt ist nehmen wir die Inzidenz als Schätzer.
    
    anteil_positiv = inzidenz / 100_000

    # => tp je 100_000 Einwohner
    p = anteil_positiv * group_size
    n = group_size - p

    tp = sensitivity * p
    tn = specificity * n

    fn = p - tp
    fp = n - tn

    def f_sensitivity(tp, fn):
        return tp / (tp + fn)

    def f_specificity(tn, fp):
        return tn / (tn + fp)

    axis2 = np.linspace(-6, 6, num=128)

    shift_fn = -scipy.stats.norm.ppf(sensitivity)
    shift_fp = -scipy.stats.norm.ppf(1 - specificity)

    p_chart = (
        alt.Chart(
            pd.DataFrame(
                {
                    "x": axis2, 
                    "y": anteil_positiv * normal_dens(0, 1, axis2 - shift_fn),
                    "tp":tp
                }
            )
        )
        .mark_area(opacity=0.5, color="red")
        .encode(
            x="x", 
            y="y",
            tooltip = [alt.Tooltip('tp', title='Anzahl positiver Test und positv (TP)')]
        )
    )

    fn_chart = (
        alt.Chart(
            pd.DataFrame(
                {
                    "x": axis2,
                    "y": anteil_positiv
                    * normal_dens(0, 1, axis2 - shift_fn)
                    * (axis2 > 0),
                    "fn": fn
                }
            )
        )
        .mark_area(opacity=0.5, color="darkred")
        .encode(
            x="x", 
            y="y",
            tooltip = [alt.Tooltip('fn', title='Anzahl negativer Test obwohl positv (FN)')]
        )
    )

    n_chart = (
        alt.Chart(
            pd.DataFrame(
                {
                    "x": axis2,
                    "y": (1 - anteil_positiv) * normal_dens(0, 1, axis2 - shift_fp),
                    "tn":tn
                }
            )
        )
        .mark_area(opacity=0.5, color="blue")
        .encode(
            x="x", 
            y="y",
            tooltip = [alt.Tooltip('tn', title='Anzahl negativer Test und negativ (TN)')]
        )
    )

    fp_chart = (
        alt.Chart(
            pd.DataFrame(
                {
                    "x": axis2,
                    "y": (1 - anteil_positiv)
                    * normal_dens(0, 1, axis2 - shift_fp)
                    * (axis2 < 0),
                    "fp":fp
                }
            )
        )
        .mark_area(opacity=0.5, color="darkblue")
        .encode(
            alt.X("x", axis=alt.Axis(title="Maßeinheit des Tests")),
            alt.Y("y", axis=alt.Axis(title="Anteil")),
            tooltip = [alt.Tooltip('fp', title='Anzahl positver Test obwohl negativ (FP)')]
        )
    )

    cutoff = alt.Chart(pd.DataFrame({"x": [0]})).mark_rule().encode(
        x="x",
        tooltip = [alt.Tooltip('x', title='cutoff')]
    )
    


    (p_chart + fn_chart + n_chart + fp_chart + cutoff).display()

    logger.debug("p " + str(p))
    logger.debug("n " + str(n))
    logger.debug("anteil " + str(anteil_positiv))
    logger.debug("FP: " + str(fp))
    logger.debug("FN: " + str(fn))
    logger.debug("TP: " + str(tp))
    logger.debug("TN: " + str(tn))
    logger.debug("TP: " + str(tp))
    logger.debug("TN: " + str(tn))
    logger.debug(12 * p * np.mean(normal_dens(0, 1, axis2 - shift_fn) * (axis2 > 0)))
    logger.debug(12 * n * np.mean(normal_dens(0, 1, axis2 - shift_fp) * (axis2 < 0)))

    print(
        f"""Von {str(group_size)} getestet Personen erwarten wir dass mindestens {str(int(np.floor(fn)))} Tests negativ 
sind, obwohl die getesteten Personen in Wahrheit positv sind.
        
"""
    )
    print(
        f"""Von {str(group_size)} getestet Personen erwarten wir dass mindestens {str(int(np.floor(fp)))} Tests positiv 
sind, obwohl die getesteten Personen in Wahrheit negativ sind.

"""
    )

    praevalenz = anteil_positiv
    ppv = (sensitivity * praevalenz) / (
        sensitivity * praevalenz + (1 - specificity) * (1 - praevalenz)
    )
    npv = (specificity * (1 - praevalenz)) / (
        specificity * (1 - praevalenz) + (1 - sensitivity) * praevalenz
    )

    print(
        f"""Ein positiv getesterer ist mit {str(np.round(ppv * 100, 3))}% wirklich positiv."""
    )
    print(
        f"""Ein negativ getesterer ist mit {str(np.round(npv * 100, 3))} % wirklich negativ."""
    )
