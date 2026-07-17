import pandas as pd
import altair as alt
def create_chart(df):
    return alt.Chart(df).mark_bar().encode(x='category', y='amount').to_json()
