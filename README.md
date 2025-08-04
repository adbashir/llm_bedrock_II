# TRITON INSIGHTS 2.0

A Streamlit-based analytics dashboard for querying, visualizing, and analyzing environmental sensor and alert data from AWS Athena and Bedrock LLM. Supports both LLM-based natural language queries and manual SQL filter selection.

![Logo](image.png)

---

## Features

- **Natural Language Data Querying:**  
  Query environmental and alert data using Bedrock LLM (Cohere Command-Light) for Athena SQL generation and natural language answers.

- **Manual Athena SQL Interface:**  
  Direct selection of device, columns, and date range with visualization and table export.

- **AWS Integration:**  
  - Athena for query execution  
  - S3 for result storage  
  - Glue Data Catalog  
  - (Optionally) Bedrock Vector Knowledge Base

- **Interactive Visualizations:**  
  Time series and multi-metric plots with Plotly in Streamlit.

---

## File Structure

- `main_app.py`   # Streamlit entrypoint (mode selector, logo, routing)
- `llm_ui.py`     # UI for LLM-driven (natural language) queries
- `nonllm_ui.py`   # UI for manual queries
- `athena_utils.py`  # Athena SQL runner, result handling, Plotly plotting
- `llm_utils.py`    # Bedrock LLM wrapper and prompt logic
- `knowledge_base.py` # Mappings and example queries for both tables
- `image.png`     # App logo

---

## Requirements

- Python 3.9+
- AWS credentials/configured for Athena, Bedrock, S3, Glue
- The following Python packages (see `requirements.txt`):

```text
streamlit
boto3
pandas
plotly
Pillow
