import streamlit as st
import pandas as pd
import plotly.express as px
import statsmodels.formula.api as smf
from scipy import stats
from analysis import get_desciriptive_stats, multiple_regression, simple_regression
from content import INTRO_TEXT, HYPOTHESES, MULTIPLE_REGRESSION_TEXT, SIMPLE_REGRESSION_TEXT
from llm import system_prompt, chat_with_model_stream, chat_with_model

#----------RESULSTS AND PLOTS RENDERING FUNCTIONS---------#

def render_multiple_regression_results(df):
    """
    Run multiple regression (MAAS + inhibition → z_pickups) and display 
    R², F-statistic, p-value, coefficients table, and scatter plots in Streamlit.
    """
    r_squared, f_stat, p_value, results_df = multiple_regression(df)
    # Displaying the R², F-statistic, and p-value
    col1, col2, col3 = st.columns(3)
    col1.metric("R²", r_squared)
    col2.metric("F-statistic", f_stat)
    col3.metric("p-value", p_value)

    st.dataframe(results_df)

    # st.markdown("### Scatter Plots with Regression Lines")
    st.plotly_chart(px.scatter(df, x='maas_score', y='z_pickups', trendline='ols', title='Z-Pickups vs MAAS Score'))
    st.plotly_chart(px.scatter(df, x='inhibition_score', y='z_pickups', trendline='ols', title='Z-Pickups vs Inhibition Score'))

def render_simple_regression_resulsts(df):
    """
    Run simple linear regression (MAAS → inhibition) and display
    R², F-statistic, p-value, coefficients table, and scatter plot in Streamlit.
    """
    r_squared, f_stat, p_value, results_df = simple_regression(df)
    # Displaying the R², F-statistic, and p-value
    col1, col2, col3 = st.columns(3)
    col1.metric("R²", r_squared)
    col2.metric("F-statistic", f_stat)
    col3.metric("p-value", p_value)

    # Displaying the coefficients, t-values, and p-values in a table
    st.dataframe(results_df)
    st.plotly_chart(px.scatter(df, x='maas_score', y='inhibition_score', trendline='ols', title='Inhibition Score vs MAAS Score'))


def render_distribution_plots(df, relevant_columns):
    """Render histogram and boxplot for each variable in Streamlit. """
    for col in relevant_columns:
        col_display_title = " ".join(col.split("_")).title()
        st.markdown(f"### {col_display_title} Distribution")
        col1, col2 = st.columns(2)
        col1.plotly_chart(px.histogram(df, x= col))
        col2.plotly_chart(px.box(df, y = col))   



# Load the data
with open("public_data_for_analysis.csv", "r") as f:
    df = pd.read_csv(f)

# Create a new column for z-scored pickups
df['z_pickups'] = None
df.loc[df['ios_pickups'].notna(), 'z_pickups'] = stats.zscore(df['ios_pickups'].dropna())
df.loc[df['non_ios_avg_pickups'].notna(), 'z_pickups'] = stats.zscore(df['non_ios_avg_pickups'].dropna())
df["z_pickups"] = pd.to_numeric(df["z_pickups"], errors='coerce')

# App title
st.set_page_config(page_title="Mindfulness, Inhibition & Phone Checking")

# TITLE
st.title("Exploring the relationship between trait mindfulness, inhibition, and phone checking frequency")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("", [
    "Overview",
    "Report", 
    "Chatbot"
])

# Overview page
if page == "Overview":
    st.title("Mindfulness, Inhibition & Phone Checking")
    st.markdown("""
    This dashboard presents the reanalysis and visualisation of a BSc Psychology research project 
    investigating the relationship between trait mindfulness, inhibitory control, and phone checking frequency.

    **Navigate using the sidebar:**
    - **Overview** — Study background, aims, and hypotheses
    - **Report** — Full analysis including descriptive statistics, normality checks, and regression results
    - **Chatbot** — Ask questions about the study and findings
    """)

# Report page
elif page == "Report":
    tab1, tab2, tab3, tab4 = st.tabs(["Intro", "Sample", "Descriptive", "Inferential Analysis"])

    with tab1:
        # INTRO
        st.markdown("# Introduction")
        st.markdown(f"{INTRO_TEXT}")

        ## Hypotheses
        st.markdown("## Hypotheses")
        for key, value in HYPOTHESES.items():
            st.markdown(f"**{key}**: {value}")

    with tab2:
        # SAMPLE
        st.markdown("# Sample Characteristics")
        ## Gender distribution
        st.plotly_chart(px.pie(df, names='gender', title='Gender Distribution'))
        ## Device usage distribution
        st.plotly_chart(px.bar(df, x='device', title='Device Usage Distribution'))
        # Age distribution
        st.plotly_chart(px.histogram(df, x='age', title='Age Distribution'))

    with tab3:
        # DESCRIPTIVE STATISTICS
        st.markdown("# Descriptive Statistics for Key Variables")
        st.table(get_desciriptive_stats(df))

        # DISTRIBUTIONS
        st.markdown("# Distributions of Key Variables")
        st.markdown("## Histohrams and box plots for MAAS scores, inhibition scores, and phone checking frequency.")
        relevant_columns = ['maas_score', 'ios_pickups', 'non_ios_avg_pickups', 'inhibition_score']
        render_distribution_plots(df,relevant_columns)

    with tab4:
        # INFERENTIAL ANALYSE
        st.markdown("# Regression Analysis")

        ## Multiple linear regression
        st.markdown("## Multiple Linear Regression")
        st.markdown(f"{MULTIPLE_REGRESSION_TEXT}")

        ### display_multiple_regression_results(df)
        st.markdown("### Regression Results")
        render_multiple_regression_results(df)

        ## Simple linear regression for H3
        st.markdown("## Simple Linear Regression for H3")
        st.markdown(f"{SIMPLE_REGRESSION_TEXT}")
        #### Display Simple Regression resulsts
        st.markdown("### Regression Results for H3")
        render_simple_regression_resulsts(df)

# LLM chatbot page
else:
    # with tab1:
    st.markdown("# LLM insight chat")
    st.divider()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about the study"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        messages = [{"role": "system", "content": system_prompt}] + st.session_state.messages

        with st.chat_message("assistant"):
            reply =  st.write_stream(chat_with_model_stream(messages))

        st.session_state.messages.append({"role": "assistant", "content": reply})

