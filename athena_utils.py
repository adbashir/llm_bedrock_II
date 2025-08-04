import boto3
import time as t
import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

ATHENA_DB = "newdata"
ATHENA_OUTPUT = "s3://aws-athena-query-results-us-east-1-882540910495/"

NUMERIC_COLUMNS = [
    "temperature", "co", "hcho", "etoh", "humidity", "tvoc", "co2",
    "no2", "pm_1", "pm_25", "pm_10", "person_detection", "loitering",
    "aqi", "ehi", "noise_ratio", "crowd_count"
]

athena = boto3.client("athena", region_name="us-east-1")

def run_athena_query(query):
    exec_id = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': ATHENA_DB},
        ResultConfiguration={'OutputLocation': ATHENA_OUTPUT}
    )['QueryExecutionId']

    while True:
        status = athena.get_query_execution(QueryExecutionId=exec_id)
        state = status['QueryExecution']['Status']['State']
        if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        t.sleep(2)

    if state != 'SUCCEEDED':
        st.error(f"Query failed with state: {state}")
        return None

    result = athena.get_query_results(QueryExecutionId=exec_id)
    rows = result['ResultSet']['Rows']

    header = [col['VarCharValue'] for col in rows[0]['Data']]
    data = [[col.get('VarCharValue', '') for col in row['Data']] for row in rows[1:]]
    return header, data

def plot_subplots(df, numeric_cols):
    num_plots = len(numeric_cols)
    fig = make_subplots(
        rows=num_plots,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=[col.capitalize() for col in numeric_cols]
    )
    for i, col in enumerate(numeric_cols, start=1):
        fig.add_trace(
            go.Scatter(
                x=df['time'] if 'time' in df.columns else list(range(len(df))),
                y=df[col],
                mode='lines+markers',
                marker=dict(size=4),
                name=col
            ),
            row=i, col=1
        )
        fig.update_yaxes(title_text=col.capitalize(), row=i, col=1)
    fig.update_layout(
        height=250 * num_plots,
        width=800,
        title_text="Selected Variables over Time",
        showlegend=False,
        hovermode="x unified",
        margin=dict(t=50)
    )
    st.plotly_chart(fig, use_container_width=True)
