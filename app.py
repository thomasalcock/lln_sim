import streamlit as st
import numpy as np
from metric_stabilization_plot import MetricStabilizationPlot

st.write(
    """ 
    # LLN Simulator
    This application simulates the sample metrics (mean, standard deviation) of 
    of random variates drawn from different distributions.
    """
)

st.sidebar.header("Configure Chart Properties")

dist = st.sidebar.selectbox("Choose distribution", ["gaussian", "lognormal", "pareto"])
min_n = int(
    np.round(
        st.sidebar.number_input(
            "Choose minimum sample size",
            min_value=10,
            max_value=100,
            value=10,
        ),
        0,
    )
)
max_n = int(
    np.round(
        st.sidebar.number_input(
            "Choose maximum sample size",
            min_value=1000,
            max_value=100000,
            value=5000,
        ),
        0,
    )
)
step = int(
    np.round(
        st.sidebar.number_input(
            "Choose step size",
            min_value=10,
            max_value=100,
            value=10,
        ),
        0,
    )
)
metrics = st.sidebar.multiselect(
    "Choose metrics", default=["mean"], options=["mean", "std", "skewness", "kurtosis"]
)


if dist == "gaussian":
    mu = st.sidebar.slider(
        "Speficy mu",
        min_value=-50.0,
        max_value=50.0,
        value=0.0,
        step=0.1,
    )
    sigma = st.sidebar.slider(
        "Specify sigma",
        min_value=1.0,
        max_value=50.0,
        value=1.0,
        step=0.1,
    )
    stabPlot = MetricStabilizationPlot(
        min_n,
        max_n,
        step,
        dist,
        mu=mu,
        sigma=sigma,
        metrics=metrics,
    )
    st.plotly_chart(stabPlot.createStabilizationPlot())
    st.plotly_chart(stabPlot.createDistributionPlot())
elif dist == "lognormal":
    mu = st.sidebar.slider(
        "Speficy mu",
        min_value=-50.0,
        max_value=50.0,
        value=0.0,
        step=0.1,
    )
    sigma = st.sidebar.slider(
        "Specify sigma",
        min_value=1.0,
        max_value=50.0,
        value=1.0,
        step=0.1,
    )
    stabPlot = MetricStabilizationPlot(
        min_n,
        max_n,
        step,
        dist,
        mu=mu,
        sigma=sigma,
        metrics=metrics,
    )
    st.plotly_chart(stabPlot.createStabilizationPlot())
    st.plotly_chart(stabPlot.createDistributionPlot())
elif dist == "pareto":
    alpha = st.sidebar.slider(
        "Specify alpha",
        min_value=0.01,
        max_value=5.0,
        value=2.0,
        step=0.05,
    )
    stabPlot = MetricStabilizationPlot(
        min_n,
        max_n,
        step,
        dist,
        alpha=alpha,
        metrics=metrics,
    )
    st.plotly_chart(stabPlot.createStabilizationPlot())
    st.plotly_chart(stabPlot.createDistributionPlot())
