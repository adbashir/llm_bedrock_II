import streamlit as st
import pandas as pd
from athena_utils import run_athena_query, plot_subplots, NUMERIC_COLUMNS

def run_nonllm_ui():
    HEARTBEATS_COLUMNS = [
        "time", "temperature", "co", "hcho", "etoh", "humidity", "tvoc", "co2",
        "no2", "pm_1", "pm_25", "pm_10", "person_detection", "loitering", "aqi",
        "ehi", "noise_ratio", "crowd_count", "device_id", "date"
    ]
    device_ids = [
        "02AAAAAAA003", "02AAAAAAA005", "02AAAAAAA007", "02AAAAAAA009",
        "02AAAAAAA011", "02AAAAAAA013", "02AAAAAAA015", "02AAAAAAA017",
        "02AAAAAAA019", "02BBBBBBB003"
    ]

    st.subheader("Select date range, device ID and columns")
    col1, col2 = st.columns(2)
    from datetime import date
    with col1:
        start_date = st.date_input(
            "Start date",
            value=date(2025, 7, 1),
            min_value=date(2025, 6, 1),
            max_value=date(2025, 7, 31)
        )
    with col2:
        end_date = st.date_input(
            "End date",
            value=date(2025, 7, 20),
            min_value=date(2025, 6, 1),
            max_value=date(2025, 7, 31)
        )

    device_id = st.selectbox("Select device ID", device_ids)
    default_cols = [col for col in HEARTBEATS_COLUMNS if col not in ['device_id', 'date']]
    selected_cols = st.multiselect(
        "Select columns to query and display",
        options=default_cols,
    )
    if "time" not in selected_cols:
        selected_cols.insert(0, "time")

    if start_date > end_date:
        st.error("Start date must be before or equal to End date.")
    else:
        if st.button("Run Query"):
            start_str = start_date.strftime("%Y-%m-%d")
            end_str = end_date.strftime("%Y-%m-%d")
            cols_str = ", ".join(selected_cols)
            sql = f"""
            SELECT {cols_str}, device_id, date FROM heartbeats
            WHERE device_id = '{device_id}'
            AND date BETWEEN '{start_str}' AND '{end_str}'
            ORDER BY date, time
            """
            st.code(sql, language="sql")
            st.write(f"Querying Athena for device {device_id} from {start_str} to {end_str}...")
            result = run_athena_query(sql)
            if result:
                header, data = result
                df = pd.DataFrame(data, columns=header)
                num_rows = len(df)
                st.markdown("**Query Result:**")
                if num_rows > 0:
                    for col in selected_cols:
                        if col in NUMERIC_COLUMNS and col in df.columns:
                            df[col] = pd.to_numeric(df[col], errors='coerce')
                    if 'time' in df.columns:
                        df['time'] = pd.to_datetime(df['time'], errors='coerce')
                    st.markdown("**Row Details:**")
                    for col in df.columns:
                        st.markdown(f"- **{col}**: {df.iloc[0][col]}")
                    numeric_selected = [c for c in selected_cols if c in NUMERIC_COLUMNS][:5]
                    if num_rows > 1 and numeric_selected:
                        plot_subplots(df, numeric_selected)
                    else:
                        st.write("Line chart skipped because only one data row is returned or no numeric columns selected.")
                    st.table(df[selected_cols].head(10))
                else:
                    st.write("No data found for the selected parameters.")
