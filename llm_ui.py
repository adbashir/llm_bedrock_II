import streamlit as st
import pandas as pd
from llm_utils import get_sql_and_natural_response
from athena_utils import run_athena_query, plot_subplots, NUMERIC_COLUMNS
from knowledge_base import retrieve_context

def run_llm_ui():
    user_q = st.text_input("Ask a question about your data:")
    if user_q:
        kb_context = retrieve_context(user_q)
        knowledge_text = "\\n".join(kb_context) if kb_context else None
        with st.spinner("Calling Bedrock LLM..."):
            sql, answer, token_info, response_text = get_sql_and_natural_response(user_q, knowledge_text)
        if sql and answer:
            st.code(sql, language="sql")
            st.write("LLM Answer:", answer)
            if token_info:
                st.info(f"Token usage info: {token_info}")
            # st.markdown("### Executing SQL Query:")
            # st.code(sql, language="sql")
            st.write("Querying Athena...")
            result = run_athena_query(sql)
            if result:
                header, data = result
                st.markdown("### Raw Athena Query Result:")
                st.write({"header": header, "data": data})
                df = pd.DataFrame(data, columns=header)
                num_rows = len(df)
                st.write(f"**Original prompt:** {user_q}")
                for col in NUMERIC_COLUMNS:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                st.markdown("**Result:**")
                if num_rows > 0:
                    st.markdown("**Row Details:**")
                    for col in df.columns:
                        st.markdown(f"- **{col}**: {df.iloc[0][col]}")
                    if num_rows > 1:
                        if 'time' in df.columns:
                            df['time'] = pd.to_datetime(df['time'], errors='coerce')
                        numeric_cols_in_df = [col for col in NUMERIC_COLUMNS if col in df.columns]
                        if numeric_cols_in_df:
                            plot_subplots(df, [numeric_cols_in_df[0]])
                        else:
                            st.write("No numeric column available for plotting.")
                    else:
                        st.write("Line chart skipped because only one data row is returned.")
                    st.table(df.head(10))
                else:
                    st.write("No data returned for the query.")
            st.markdown("### Raw Bedrock Response Text (for debugging)")
            st.text(response_text)
