import boto3
import json
import re
import streamlit as st

# Bedrock client (region should match your Bedrock setup)
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

def get_sql_and_natural_response(question, knowledge_text=None):
    """
    Calls Bedrock LLM for Athena SQL + natural answer.
    Returns: sql, answer, token_info, response_text
    """
    # Build prompt
    prompt = (
        "You are an expert AWS Athena SQL assistant. "
        "The database is 'newdata' with tables:\n"
        "- heartbeats: time, temperature, co, hcho, etoh, humidity, tvoc, co2, no2, pm_1, pm_25, pm_10, person_detection, loitering, aqi, ehi, noise_ratio, crowd_count, device_id, date\n\n"
        "Always pick the most relevant table and column(s). "
        "ALWAYS use correct column names and this date format: 'YYYY-MM-DD'. "
        "ALWAYS include 'time' columns in your SQL if present. "
        "DO NOT use the database name as a table. "
        "ORDER BY TIME if possible. "
        "Respond ONLY in this JSON format: {\"sql\": \"...\", \"answer\": \"...\"}\n"
        "EXAMPLES:\n"
        "Q: Return temperature for first day of August 2025\n"
        "A: {\"sql\": \"SELECT temperature, time FROM heartbeats WHERE date = '2025-08-01';\", \"answer\": \"Temperature on 2025-08-01 from heartbeats table.\"}\n"
        "Q: List alert types for July 2025\n"
        "A: {\"sql\": \"SELECT alert_type, time FROM alerts WHERE date LIKE '2025-07%';\", \"answer\": \"All alert types for July 2025 from alerts table.\"}\n"
    )
    if knowledge_text:
        prompt = f"Knowledge Base:\n{knowledge_text}\n\n" + prompt
    prompt += f"Q: {question}\nA: "
    body = json.dumps({
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.2
    })

    response = bedrock.invoke_model(
        modelId="cohere.command-light-text-v14",
        contentType="application/json",
        accept="application/json",
        body=body
    )
    response_text = response['body'].read().decode()
    sql = None
    answer = None
    token_info = None

    # Try to directly parse as JSON (ideal case)
    try:
        resp_json = json.loads(response_text)
        # Sometimes the model responds as a dict
        if isinstance(resp_json, dict) and 'sql' in resp_json and 'answer' in resp_json:
            sql = resp_json['sql']
            answer = resp_json['answer']
        # Some Cohere/Anthropic models return in 'generations'
        elif isinstance(resp_json, dict) and 'generations' in resp_json:
            text = resp_json['generations'][0]['text']
            # Find JSON inside text using regex
            matches = re.findall(r'\{.*?\}', text, re.DOTALL)
            for m in matches:
                try:
                    j = json.loads(m)
                    if 'sql' in j:
                        sql = j['sql']
                    if 'answer' in j:
                        answer = j['answer']
                except Exception:
                    continue
        # Token usage info (optional, for reporting/monitoring)
        if 'usage' in resp_json:
            token_info = resp_json['usage']
        elif 'token_usage' in resp_json:
            token_info = resp_json['token_usage']
        elif 'total_tokens' in resp_json:
            token_info = {'total_tokens': resp_json['total_tokens']}
    except Exception:
        # If not valid JSON, try to parse raw response for JSON object(s)
        matches = re.findall(r'\{.*?\}', response_text, re.DOTALL)
        for m in matches:
            try:
                j = json.loads(m)
                if 'sql' in j:
                    sql = j['sql']
                if 'answer' in j:
                    answer = j['answer']
            except Exception:
                continue

    # If still missing, error out cleanly for Streamlit
    if not sql or not answer:
        st.error(f"Could not parse model output. Raw output: {response_text}")
        return None, None, None, response_text

    return sql, answer, token_info, response_text
