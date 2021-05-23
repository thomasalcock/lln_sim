import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import scipy.stats as sp
from utils import logger

# TODO: fix list types


class MetricStabilizationPlot:
    def __init__(
        self,
        min_n: int,
        max_n: int,
        step: int,
        dist_type: str = "pareto",
        metrics: list = ["mean", "std", "skewness", "kurtosis"],
        **kwargs,
    ) -> None:

        logger.info("Initialize instance of MetricStabilizationPlot")
        logger.info(f"min_n: {min_n}")
        logger.info(f"max_n: {max_n}")
        logger.info(f"step: {step}")
        logger.info(f"dist_type: {dist_type}")
        logger.info(f"selected metrics: {metrics}")
        logger.info(f"additional args: {kwargs}")

        self.min_n = min_n
        if not isinstance(self.min_n, int):
            raise ValueError("min_n must be of type int")

        self.max_n = max_n
        if not isinstance(self.max_n, int):
            raise ValueError("max_n must be of type int")

        self.step = step
        if not isinstance(self.step, int):
            raise ValueError("step must be of type int")

        self.dist_type = dist_type
        if not isinstance(self.dist_type, str):
            raise ValueError("dist_type must be of type str")

        self.metrics = metrics
        if not isinstance(self.metrics, list):
            raise ValueError("metrics must be of type list")

        self.kwargs = kwargs

    def createDrawSequence(self) -> list[int]:
        """Creates as list of the number of samples
        to be drawn from a probability distribution

        Returns:
            list: integers representing the number of samples
        """
        draws = np.arange(self.min_n, self.max_n + self.step, step=self.step, dtype=int)
        draws = [int(x) for x in draws]
        return list(draws)

    def createParetoSampleSequence(self) -> tuple[list[float], list[int]]:
        """Creates a list of samples draws from a pareto distribution.
        Output is regulated by the number of samples and the alpha parameter.

        Returns:
            tuple: list of samples and the draws themselves
        """
        draws = self.createDrawSequence()
        par_samples = [np.random.pareto(a=self.kwargs["alpha"], size=x) for x in draws]
        return par_samples, draws

    def createLogNormalSampleSequence(self) -> tuple[list[float], list[int]]:
        """Creates a list of samples draws from a lognormal distribution.
        Output is regulated by the number of samples and the mu and sigma parameter.

        Returns:
            tuple: list of samples and the draws themselves
        """
        draws = self.createDrawSequence()
        ln_samples = [
            np.random.lognormal(
                mean=self.kwargs["mu"], sigma=self.kwargs["sigma"], size=x
            )
            for x in draws
        ]
        return ln_samples, draws

    def createGaussianSampleSequence(self) -> tuple[list, list]:
        """Creates a list of samples draws from a gaussian distribution.
        Output is regulated by the number of samples and the mu and sigma parameters.

        Returns:
            tuple: list of samples and the draws themselves
        """
        draws = self.createDrawSequence()
        gauss_samples = [
            np.random.normal(loc=self.kwargs["mu"], scale=self.kwargs["sigma"], size=x)
            for x in draws
        ]
        return gauss_samples, draws

    def createSamplingDistribution(self) -> pd.DataFrame:
        """Generates a dataframe of metrics (mean, standard deviation, etc.) calculated at
        from differently sized samples.

        Returns:
            pandas.DataFrame: dataframe with number of draws and metrics calculated from samples
        """
        samples, draws = self.handleDistributionType()

        measures = {}
        if "mean" in self.metrics:
            logger.info(f"Calculating means for {len(samples)} sets of samples")
            measures["mean"] = [np.mean(x) for x in samples]

        if "std" in self.metrics:
            logger.info(
                f"Calculating standard deviations for {len(samples)} sets of samples"
            )
            measures["std"] = [np.std(x) for x in samples]

        if "skewness" in self.metrics:
            logger.info(f"Calculating skewness for {len(samples)} sets of samples")
            measures["skewness"] = [sp.skew(x) for x in samples]

        if "kurtosis" in self.metrics:
            logger.info(f"Calculating kurtosis for {len(samples)} sets of samples")
            measures["kurtosis"] = [sp.kurtosis(x) for x in samples]

        data_dict = {"n_draws": draws}
        data_dict.update(measures)
        df = pd.DataFrame(data_dict)
        logger.info(f"Returning data.frame with {df.shape[0]} rows")
        return df

    def handleDistributionType(self) -> list[float]:
        """Handler method to create sample sequences
        for different probability distributions.

        Returns:
            list: list of samples from a speficied probability distribution
        """
        logger.info(f"Generate samples for {self.dist_type} distribution")
        if self.dist_type == "pareto":
            return self.createParetoSampleSequence()
        elif self.dist_type == "gaussian":
            return self.createGaussianSampleSequence()
        elif self.dist_type == "lognormal":
            return self.createLogNormalSampleSequence()

    def handlePlotTitle(self, base_string="Sampling Metric Stabilization of") -> str:
        """Handler method to create plot title for different
        probability distributions.

        Returns:
            string: Title with name and specification of the probability distribution.
        """
        if self.dist_type == "pareto":
            return f"{base_string} Pareto Distribution (alpha = {self.kwargs['alpha']})"
        elif self.dist_type == "gaussian":
            return f"{base_string} Gaussian Distribution (mu = {self.kwargs['mu']}, sigma = {self.kwargs['sigma']})"
        elif self.dist_type == "lognormal":
            return f"{base_string} Lognormal Distribution (mu = {self.kwargs['mu']}, sigma = {self.kwargs['sigma']})"

    def createStabilizationPlot(self):
        """Method to create interactive plotly chart showing the specified metrics
        plotted against the number of draws.

        Returns:
            plotly.graph_objs._figure.Figure:
        """
        plot_title = self.handlePlotTitle()
        df = self.createSamplingDistribution()

        fig = go.Figure()

        if "mean" in self.metrics:
            logger.info("Add scatter trace for mean metric")
            fig.add_trace(go.Scatter(x=df["n_draws"], y=df["mean"], name="Mean"))

        if "std" in self.metrics:
            logger.info("Add scatter trace for std metric")
            fig.add_trace(
                go.Scatter(x=df["n_draws"], y=df["std"], name="Std. Deviation")
            )

        if "skewness" in self.metrics:
            logger.info("Add scatter trace for skewness metric")
            fig.add_trace(
                go.Scatter(x=df["n_draws"], y=df["skewness"], name="Skewness")
            )

        if "kurtosis" in self.metrics:
            logger.info("Add scatter trace for kurtosis metric")
            fig.add_trace(
                go.Scatter(x=df["n_draws"], y=df["kurtosis"], name="Kurtosis")
            )

        fig.update_layout(
            xaxis_title="Number of samples", yaxis_title="", title=plot_title
        )
        return fig

    def renderStabilizationPlot(self):
        """Renders the stabilitation plot"""
        fig = self.createStabilizationPlot()
        fig.show()

    def drawSample(self) -> list[float]:
        n = 10000
        if self.dist_type == "pareto":
            return np.random.pareto(a=self.kwargs["alpha"], size=n)
        elif self.dist_type == "lognormal":
            return np.random.lognormal(
                mean=self.kwargs["mu"], sigma=self.kwargs["sigma"], size=n
            )
        elif self.dist_type == "gaussian":
            return np.random.normal(
                loc=self.kwargs["mu"], scale=self.kwargs["sigma"], size=n
            )

    def createDistributionPlot(self):
        plot_title = self.handlePlotTitle(base_string="Long-run distribution of")
        df = [self.drawSample()]  # create_distplot only handles lists of lists
        group_labs = ["dist"]
        fig = ff.create_distplot(
            df,
            group_labels=group_labs,
            show_rug=False,
            show_hist=False,
        )
        fig.update_layout(xaxis_title="", yaxis_title="", title_text=plot_title)
        return fig
