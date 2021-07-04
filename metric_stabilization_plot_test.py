from numpy import int64, float64, ndarray
from pandas import DataFrame
from metric_stabilization_plot import MetricStabilizationPlot

stabPareto = MetricStabilizationPlot(
    min_n=10,
    max_n=5000,
    step=10,
    dist="pareto",
    alpha=3,
    metrics=["mean", "std", "skewness", "kurtosis"],
)

stabGaussian = MetricStabilizationPlot(
    min_n=10,
    max_n=5000,
    step=10,
    dist="gaussian",
    mu=0,
    sigma=1,
    metrics=["mean", "std", "skewness", "kurtosis"],
)


def all_same_type(some_list, dtype):
    return all(isinstance(x, dtype) for x in some_list)


def test_stab_pareto_draws_obj_type():
    out = stabPareto.createDrawSequence()
    assert isinstance(out, list)


def test_stab_pareto_draws_data_type():
    out = stabPareto.createDrawSequence()
    assert all_same_type(out, int)


def test_stab_pareto_sample_seq_type():
    out, draws = stabPareto.createParetoSampleSequence()
    assert isinstance(out, list)


def test_stab_pareto_sample_seq_data_type():
    out, draws = stabPareto.createParetoSampleSequence()
    assert all_same_type(out, ndarray)


def test_stab_pareto_sample_seq_sample_data_type():
    out, draws = stabPareto.createParetoSampleSequence()
    assert all_same_type(out[0], float)


def test_stab_pareto_sample_seq_metrics_type():
    df = stabPareto.createSamplingDistribution()
    assert isinstance(df, DataFrame)


def test_df_positive_means():
    df = stabPareto.createSamplingDistribution()
    assert all(df["mean"] >= 0)


def test_df_positive_sds():
    df = stabPareto.createSamplingDistribution()
    assert all(df["std"] >= 0)


def test_df_positive_skewness():
    df = stabPareto.createSamplingDistribution()
    assert all(df["skewness"] >= 0)


def test_stab_gaussian_draws_obj_type():
    out = stabGaussian.createDrawSequence()
    assert isinstance(out, list)


def test_stab_gaussian_draws_data_type():
    out = stabGaussian.createDrawSequence()
    assert all_same_type(out, int)


def test_stab_gaussian_sample_seq_type():
    out, draws = stabGaussian.createGaussianSampleSequence()
    assert isinstance(out, list)


def test_stab_gaussian_sample_seq_data_type():
    out, draws = stabGaussian.createGaussianSampleSequence()
    assert all_same_type(out, ndarray)


def test_stab_gaussian_sample_seq_sample_data_type():
    out, draws = stabGaussian.createGaussianSampleSequence()
    assert all_same_type(out[0], float)


def test_stab_gaussian_sample_seq_metrics_type():
    df = stabPareto.createSamplingDistribution()
    assert isinstance(df, DataFrame)
