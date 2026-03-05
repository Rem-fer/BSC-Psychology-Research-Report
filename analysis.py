import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

def get_desciriptive_stats(df):
    """ Calculate the mean and standard deviation for columns relevant to the analysis
    Returns a DataFrame with descriptive statistics."""
    columns_to_analyse = ['maas_score', 'ios_pickups', 'non_ios_avg_pickups', 'inhibition_score']
    descriptive_stats = {}
    for col in columns_to_analyse:
        descriptive_stats[col] = {
            "mean": round(df[col].mean(), 2),
            "standard_deviation": round(df[col].std(), 2)
        }

    descriptive_df = pd.DataFrame(descriptive_stats).T # Transpose the DataFrame to have columns as rows and vice versa
    return descriptive_df

def get_normality_tests(df):
    """
    Run Shapiro-Wilk normality tests and calculate skewness and kurtosis 
    for key study variables. Returns a DataFrame with results for each variable.
    """
    columns_to_analyse = ['maas_score', 'ios_pickups', 'non_ios_avg_pickups', 'inhibition_score']
    normality_results = {}
    for col in columns_to_analyse:
        stat, p_value = stats.shapiro(df[col].dropna())
        normality_results[col] = {
            "skewness": round(df[col].skew(), 2),
            "kurtosis": round(df[col].kurtosis(), 2),
            "shapiro_statistic": round(stat, 4),
            "shapiro_p_value": round(p_value, 4),
            "normal": p_value > 0.05
        }
    normality_df = pd.DataFrame(normality_results).T
    return normality_df

def multiple_regression(df):
    """
    Run multiple regression with MAAS and inhibition as predictors of z_pickups.
    Returns R², F-statistic, p-value, and a DataFrame of coefficients.
    """
    model = smf.ols('z_pickups ~ maas_score + inhibition_score', data=df).fit()
    r_squared = round(model.rsquared, 3)
    f_stat = round(model.fvalue, 3)
    p_value = round(model.f_pvalue, 3)
    results_df = pd.DataFrame({
        'β': model.params.round(3),
        't': model.tvalues.round(3),
        'p-value': model.pvalues.round(3)
        }).drop('Intercept')
    return r_squared, f_stat, p_value, results_df

def simple_regression(df):
    """
    Run simple regression with MAAS as predictor of inhibition score.
    Returns R², F-statistic, p-value, and a DataFrame of coefficients.
    """
    model = smf.ols('inhibition_score ~ maas_score', data=df).fit()
    r_squared = round(model.rsquared, 3)
    f_stat = round(model.fvalue, 3)
    p_value = round(model.f_pvalue, 3)
    results_df = pd.DataFrame({
        'β': model.params.round(3),
        't': model.tvalues.round(3),
        'p-value': model.pvalues.round(3)
        }).drop('Intercept')
    return r_squared, f_stat, p_value, results_df

