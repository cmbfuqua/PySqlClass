# Data Cleaning and Visualization

## Overview
Data science, analytics, and robust software engineering all rely heavily on the assumption that the underlying data being processed is accurate, consistent, and logically sound. However, in the real world, raw data is almost never perfect. It is often messy, incomplete, containing missing values (NaN/Nulls), duplicate records, incorrect formatting, or extreme outliers. The process of taking this raw, messy data and transforming it into a clean, structured format is known as **Data Cleaning** (or data wrangling/munging).

Once the data is clean, the next critical step is **Data Visualization**. Staring at a massive table of numbers rarely yields immediate insights, especially for non-technical stakeholders. Visualizations—such as line charts, bar graphs, scatter plots, and heatmaps—translate abstract data points into visual patterns, trends, and outliers that the human brain can process instantly. 

In the Python ecosystem, the `pandas` library is the undisputed king of data manipulation. It introduces the DataFrame, a highly optimized, two-dimensional table structure that makes filtering, grouping, merging, and cleaning data remarkably intuitive and fast. For visualization, libraries like `matplotlib`, `seaborn`, and `altair` provide vast capabilities for turning those DataFrames into expressive, publication-ready charts.

## Why it's important
The axiom "Garbage In, Garbage Out" (GIGO) perfectly encapsulates why data cleaning is the most important step in any analytical pipeline. If you train a complex machine learning model or build a business intelligence dashboard on top of uncleaned data, the results will be mathematically precise but fundamentally incorrect. It leads to poor business decisions, loss of revenue, and a collapse of trust in the data team.

Consider a scenario where you are analyzing customer lifetime value. If your database has three different entries for "John Doe" because of slight spelling variations or separate guest checkouts, treating them as three different customers will drastically skew your metrics. Consolidating duplicates and normalizing data ensures your foundational metrics represent reality.

Visualization is equally important because it acts as the bridge between the data engineer and the business stakeholder. A well-crafted visualization tells a compelling story, highlights anomalies that need immediate attention, and makes the results of complex statistical analysis accessible to everyone in an organization.

## Common Pitfalls
1. **Ignoring the Nuance of Missing Data (NaN)**: Missing data can mean different things. Does a missing 'age' field mean the user refused to provide it, or does it mean the data collection form was broken that day? Simply deleting all rows with missing data (using `dropna()`) might accidentally delete half your dataset and introduce severe bias. Sometimes, imputing (filling) missing data with a median or a placeholder is better than dropping it.
2. **Type Coercion Failures**: Often, numerical columns like 'revenue' are imported as strings (objects) because one single row had the value `"N/A"` or `"$500"`. If you attempt to calculate the mean of this column, Pandas will either crash or attempt to concatenate strings. You must explicitly clean characters like `$` or `,` and convert the column using `pd.to_numeric()`.
3. **Misleading Visualizations**: When creating charts, failing to start the Y-axis at zero (in bar charts), using non-proportional areas in pie charts, or picking inaccessible color palettes (for colorblind viewers) can inadvertently deceive the audience. A visualization should clarify, not obfuscate.
4. **Performance Issues with Loops**: Pandas is optimized for "vectorized" operations, meaning it applies operations to entire columns simultaneously at the C-language level. A major pitfall for beginners is iterating over a DataFrame row-by-row using a standard Python `for` loop or `iterrows()`. This is exceptionally slow. Always prefer built-in pandas methods and vectorization.

## Advanced Edge Cases
- **Time Series Anomalies**: When cleaning time-series data, you might encounter daylight saving time shifts, different time zones, or irregular sampling intervals. Pandas provides advanced tools like `.tz_localize()`, `.resample()`, and `.interpolate()` to standardize time series data before visualization.
- **High-Dimensional Categorical Data**: If you have a column with 500 unique categorical values, standard one-hot encoding will explode your DataFrame's memory footprint, and a bar chart with 500 bars is unreadable. Advanced cleaning involves grouping rare categories into an "Other" bucket before visualizing.

## Examples

### Example 1: Comprehensive Data Cleaning with Pandas
This example demonstrates a typical data cleaning pipeline, addressing missing values, duplicates, and incorrect data types.

```python
import pandas as pd
import numpy as np

def clean_sales_data(filepath):
    # 1. Load the raw data
    df = pd.read_csv(filepath)
    
    # 2. Inspect the raw shape and missing values
    print("Original Shape:", df.shape)
    
    # 3. Handle duplicates
    # Keep the last transaction if a transaction_id is duplicated
    df = df.drop_duplicates(subset=['transaction_id'], keep='last')
    
    # 4. Handle incorrect data types
    # Assume 'revenue' has strings like "$1,000.50". We need to strip $ and ,
    df['revenue'] = df['revenue'].replace({'\$': '', ',': ''}, regex=True)
    # Coerce errors to NaN so we don't crash on completely invalid text
    df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce')
    
    # 5. Handle missing values
    # Drop rows where critical information like 'transaction_id' is missing
    df = df.dropna(subset=['transaction_id'])
    
    # Fill missing 'customer_age' with the median age of the dataset
    median_age = df['customer_age'].median()
    df['customer_age'] = df['customer_age'].fillna(median_age)
    
    # 6. Date parsing
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    
    print("Cleaned Shape:", df.shape)
    return df
```

### Example 2: Aggregation and Visualization Preparation
Often, clean data is still too granular for a clear visualization. We must aggregate it first.

```python
def prepare_monthly_summary(df):
    # Extract the month and year into a new column for grouping
    df['month_year'] = df['purchase_date'].dt.to_period('M')
    
    # Group by the new period and sum the revenue
    # reset_index() flattens the result back into a standard DataFrame
    monthly_summary = df.groupby('month_year')['revenue'].sum().reset_index()
    
    # Convert period back to timestamp for easier plotting in some libraries
    monthly_summary['month_year'] = monthly_summary['month_year'].dt.to_timestamp()
    
    return monthly_summary
```

### Example 3: Declarative Visualization with Altair
Altair uses a declarative syntax, meaning you describe *what* you want the chart to look like, rather than writing a loop to draw it.

```python
import altair as alt

def plot_sales_trend(summary_df):
    # We define the chart, passing in the aggregated DataFrame
    chart = alt.Chart(summary_df).mark_line(
        point=True, # Add points to the line for clarity
        color='blue',
        strokeWidth=3
    ).encode(
        # Map columns to visual channels (x, y, tooltip)
        x=alt.X('month_year:T', title='Month'), # :T indicates Temporal (time) data
        y=alt.Y('revenue:Q', title='Total Revenue ($)'), # :Q indicates Quantitative data
        tooltip=['month_year:T', 'revenue:Q'] # Interactive hover tooltips
    ).properties(
        title='Monthly Sales Revenue Trend',
        width=600,
        height=400
    ).interactive() # Allows zooming and panning
    
    # In a real environment, you might save this to HTML or display in a notebook
    # chart.save('sales_trend.html')
    return chart
```
