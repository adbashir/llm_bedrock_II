# knowledge_base = [
#     "Table: heartbeats. Columns: time, temperature, humidity, co2, pm_1, pm_25, pm_10, person_detection, crowd_count, device_id, date.",
#     "Example: Get temperature for July 1, 2025: SELECT time, temperature FROM heartbeats WHERE date = '2025-07-01';",
#     "Column: crowd_count. Description: Number of people detected per sensor, per minute.",
#     "Column: person_detection. Integer count of people detected by the device.",
# ]
knowledge_base = [
    # Table descriptions
    "Table: heartbeats. Columns: time (string, 'YYYY-MM-DD HH:MM:SS'), temperature (float, °C), co (float, ppm), hcho (float, ppb), etoh (float, ppb), humidity (float, %RH), tvoc (float, ppb), co2 (float, ppm), no2 (float, ppb), pm_1 (float, µg/m³), pm_25 (float, µg/m³), pm_10 (float, µg/m³), person_detection (int), loitering (int), aqi (float), ehi (float), noise_ratio (float), crowd_count (int), device_id (string), date (string, 'YYYY-MM-DD').",
    "Table: alerts. Columns: time (string, 'YYYY-MM-DD HH:MM:SS'), alert_type (string), alert_threshold (float), alert_value (float), device_name (string), date (string, 'YYYY-MM-DD').",

    # Field descriptions
    "Field mapping: For 'heartbeats', map 'temperature' (highest/lowest/hottest/coldest) to temperature, 'most crowded'/'busiest' to crowd_count, 'people detected' to person_detection, 'air quality' to aqi, 'noise' to noise_ratio, 'humidity' to humidity, 'co2' to co2, 'fine particulate' or 'PM2.5' to pm_25, 'device' to device_id.",
    "For 'alerts', 'alert type' is alert_type, 'alert threshold' is alert_threshold, 'alert value' is alert_value, 'device' or 'sensor' is device_name. Always include time for temporal queries.",

    # Natural language mapping
    "Natural language: 'highest temperature'→MAX(temperature), 'most crowded'→MAX(crowd_count), 'minimum CO2'→MIN(co2), 'alert types'→alert_type, 'all alerts'→SELECT * FROM alerts, 'alert times'→time column.",

    # Example queries for heartbeats (always include time, order by time)
    "Example: Temperature for July 1, 2025: SELECT time, temperature FROM heartbeats WHERE date = '2025-07-01' ORDER BY time;",
    "Example: Maximum temperature in August 2025: SELECT time, temperature FROM heartbeats WHERE date LIKE '2025-08%' ORDER BY temperature DESC, time LIMIT 1;",
    "Example: All crowd counts for June 2025: SELECT time, crowd_count FROM heartbeats WHERE date LIKE '2025-06%' ORDER BY time;",
    "Example: Times and values for highest PM2.5 in March 2025: SELECT time, pm_25 FROM heartbeats WHERE date LIKE '2025-03%' ORDER BY pm_25 DESC, time LIMIT 1;",
    "Example: Daily average CO2 in May 2025: SELECT date, AVG(co2) AS avg_co2 FROM heartbeats WHERE date LIKE '2025-05%' GROUP BY date ORDER BY date;",
    "Example: All readings for device 'XYZ123' on March 10, 2025: SELECT time, temperature, co2, humidity FROM heartbeats WHERE date = '2025-03-10' AND device_id = 'XYZ123' ORDER BY time;",
    "Example: List all loitering events on April 15, 2025: SELECT time, loitering FROM heartbeats WHERE date = '2025-04-15' AND loitering > 0 ORDER BY time;",
    "Example: All AQI values for July 2025: SELECT time, aqi FROM heartbeats WHERE date LIKE '2025-07%' ORDER BY time;",
    "Example: Noise ratio and time for first day of August 2025: SELECT time, noise_ratio FROM heartbeats WHERE date = '2025-08-01' ORDER BY time;",

    # Column descriptions
    "Column: time. Format: 'YYYY-MM-DD HH:MM:SS'. Timestamp of the measurement.",
    "Column: temperature. Ambient temperature in Celsius (°C). Use for highest/lowest temperature queries.",
    "Column: co. Carbon monoxide concentration, parts per million (ppm).",
    "Column: hcho. Formaldehyde concentration, parts per billion (ppb).",
    "Column: etoh. Ethanol (alcohol) concentration, parts per billion (ppb).",
    "Column: humidity. Relative humidity, percentage (%RH).",
    "Column: tvoc. Total volatile organic compounds, parts per billion (ppb).",
    "Column: co2. Carbon dioxide concentration, parts per million (ppm).",
    "Column: no2. Nitrogen dioxide concentration, parts per billion (ppb).",
    "Column: pm_1. Particulate matter ≤1.0µm, micrograms per cubic meter (µg/m³).",
    "Column: pm_25. Particulate matter ≤2.5µm, micrograms per cubic meter (µg/m³).",
    "Column: pm_10. Particulate matter ≤10µm, micrograms per cubic meter (µg/m³).",
    "Column: person_detection. Integer count of people detected by the device at each time.",
    "Column: loitering. Integer indicator of loitering events.",
    "Column: aqi. Air Quality Index (float, calculated).",
    "Column: ehi. Environmental Health Index (float, calculated).",
    "Column: noise_ratio. Ratio or metric for noise in the environment.",
    "Column: crowd_count. Number of people detected per sensor, per minute. Use for 'most crowded', 'busiest', or occupancy queries.",
    "Column: device_id. Unique device identifier (string).",
    "Column: date. Date of measurement, string, 'YYYY-MM-DD'. Use for filtering by day.",

    # Natural language mapping to SQL columns
    "Natural language mapping:",
    "- 'Highest temperature', 'hottest', 'maximum temperature' ⇒ temperature column, use MAX().",
    "- 'Lowest temperature', 'coldest', 'minimum temperature' ⇒ temperature column, use MIN().",
    "- 'Most crowded', 'highest occupancy', 'maximum crowd' ⇒ crowd_count column, use MAX().",
    "- 'Least crowded', 'minimum occupancy' ⇒ crowd_count column, use MIN().",
    "- 'People detected', 'number of people', 'person count' ⇒ crowd_count or person_detection, context-dependent.",
    "- 'Air quality', 'pollution', 'AQI' ⇒ aqi column.",
    "- 'Noise', 'noise ratio' ⇒ noise_ratio column.",
    "- 'Humidity' ⇒ humidity column.",
    "- 'CO2 level' ⇒ co2 column.",
    "- 'Fine particulate', 'PM2.5', 'PM 2.5' ⇒ pm_25 column.",
    "- 'Device', 'sensor' ⇒ device_id.",
    "- Always filter by date using 'date' column (format: 'YYYY-MM-DD').",
    "- Always return time column for time-resolved queries.",

    # Examples for alerts table (always include time, order by time)
    "Example: All alert types and times for July 2025: SELECT time, alert_type FROM alerts WHERE date LIKE '2025-07%' ORDER BY time;",
    "Example: All alerts for device 'ABC1' on 2025-08-04: SELECT time, alert_type, alert_value FROM alerts WHERE date = '2025-08-04' AND device_name = 'ABC1' ORDER BY time;",
    "Example: All alerts of type 'HighTemp' for June 2025: SELECT time, alert_type, alert_value FROM alerts WHERE date LIKE '2025-06%' AND alert_type = 'HighTemp' ORDER BY time;",
    "Example: List all alert thresholds for May 2025: SELECT time, alert_type, alert_threshold FROM alerts WHERE date LIKE '2025-05%' ORDER BY time;",
    "Example: Times when alert value exceeded threshold in July 2025: SELECT time, alert_type, alert_value FROM alerts WHERE date LIKE '2025-07%' AND alert_value > alert_threshold ORDER BY time;",
    "Example: Alerts with value above 80 for August 2025: SELECT time, alert_type, alert_value FROM alerts WHERE date LIKE '2025-08%' AND alert_value > 80 ORDER BY time;",
    "Example: First alert on August 2, 2025: SELECT time, alert_type, alert_value FROM alerts WHERE date = '2025-08-02' ORDER BY time LIMIT 1;",
    "Example: Last alert of July 2025: SELECT time, alert_type FROM alerts WHERE date LIKE '2025-07%' ORDER BY time DESC LIMIT 1;",
    "Example: All alert values for device 'Room101' in May 2025: SELECT time, alert_type, alert_value FROM alerts WHERE date LIKE '2025-05%' AND device_name = 'Room101' ORDER BY time;",
    "Example: List of unique alert types for June 2025: SELECT DISTINCT alert_type FROM alerts WHERE date LIKE '2025-06%';",
    "Example: Time and value of maximum alert in July 2025: SELECT time, alert_value FROM alerts WHERE date LIKE '2025-07%' ORDER BY alert_value DESC, time LIMIT 1;",
    "Example: All alert times and values where alert type is 'CO2High': SELECT time, alert_value FROM alerts WHERE alert_type = 'CO2High' ORDER BY time;",
    "Example: Alerts per device for July 2025: SELECT device_name, COUNT(*) AS alert_count FROM alerts WHERE date LIKE '2025-07%' GROUP BY device_name ORDER BY alert_count DESC;",
    "Example: All alerts between 9 AM and 12 PM on August 4, 2025: SELECT time, alert_type FROM alerts WHERE date = '2025-08-04' AND time BETWEEN '2025-08-04 09:00:00' AND '2025-08-04 12:00:00' ORDER BY time;",
    "Example: All alert values above 100: SELECT time, alert_type, alert_value FROM alerts WHERE alert_value > 100 ORDER BY time;",
    "Example: Times and types for all alerts for a specific device: SELECT time, alert_type FROM alerts WHERE device_name = 'XYZ123' ORDER BY time;",
    "Example: List alert values for a specific day: SELECT time, alert_type, alert_value FROM alerts WHERE date = '2025-07-15' ORDER BY time;",
    "Example: All alerts of type 'Loitering' for June 2025: SELECT time, alert_type, alert_value FROM alerts WHERE date LIKE '2025-06%' AND alert_type = 'Loitering' ORDER BY time;",
    "Example: All alert types, thresholds, and values for July 2025: SELECT time, alert_type, alert_threshold, alert_value FROM alerts WHERE date LIKE '2025-07%' ORDER BY time;",
    "Example: Time and alert value of minimum alert in July 2025: SELECT time, alert_value FROM alerts WHERE date LIKE '2025-07%' ORDER BY alert_value ASC, time LIMIT 1;",
    "Example: All alert types and values for August 2025: SELECT time, alert_type, alert_value FROM alerts WHERE date LIKE '2025-08%' ORDER BY time;",
    "Example: Number of alerts per alert type in July 2025: SELECT alert_type, COUNT(*) AS alert_count FROM alerts WHERE date LIKE '2025-07%' GROUP BY alert_type ORDER BY alert_count DESC;",
    "Example: Earliest alert in the system: SELECT time, alert_type FROM alerts ORDER BY time ASC LIMIT 1;",
    "Example: Latest alert in the system: SELECT time, alert_type FROM alerts ORDER BY time DESC LIMIT 1;"
]


def retrieve_context(user_question, kb=knowledge_base, top_k=3):
    scored = []
    user_words = set(user_question.lower().split())
    for entry in kb:
        entry_words = set(entry.lower().split())
        score = len(user_words & entry_words)
        scored.append((score, entry))
    scored.sort(reverse=True)
    return [entry for score, entry in scored[:top_k] if score > 0]



# import boto3
# import json
# import pandas as pd

# class BedrockKnowledgeBase:
#     """
#     Simple interface to query AWS Bedrock Knowledge Base (Vector type).
#     """
#     def __init__(self, kb_id, region="us-east-1"):
#         self.kb_id = kb_id
#         self.bedrock = boto3.client("bedrock-agent-runtime", region_name=region)

#     def query(self, query_text, top_k=5, return_sources=True):
#         """
#         Query Bedrock KB with a natural language question.
#         Returns full API response.
#         """
#         payload = {
#             "knowledgeBaseId": self.kb_id,
#             "query": query_text,
#             "retrievalConfiguration": {
#                 "vectorSearchConfiguration": {
#                     "numberOfResults": top_k
#                 }
#             },
#             "returnSourceDocuments": return_sources
#         }
#         response = self.bedrock.retrieve_and_generate(**payload)
#         return response

#     def get_answers(self, query_text):
#         """
#         Return simplified list of answers for use in app UI.
#         """
#         resp = self.query(query_text)
#         if resp and "output" in resp:
#             answers = resp["output"].get("answers", [])
#             return [a.get("text", "") for a in answers]
#         return []

#     def get_sources(self, query_text):
#         """
#         Return the retrieved source documents (optional, for explainability).
#         """
#         resp = self.query(query_text)
#         if resp and "output" in resp:
#             return resp["output"].get("sourceDocuments", [])
#         return []

# # Optional Athena fallback for structured SQL queries
# class AthenaQuery:
#     def __init__(self, db, output, region="us-east-1"):
#         self.athena = boto3.client("athena", region_name=region)
#         self.db = db
#         self.output = output

#     def run_query(self, query):
#         exec_id = self.athena.start_query_execution(
#             QueryString=query,
#             QueryExecutionContext={'Database': self.db},
#             ResultConfiguration={'OutputLocation': self.output}
#         )['QueryExecutionId']
#         import time
#         while True:
#             status = self.athena.get_query_execution(QueryExecutionId=exec_id)
#             state = status['QueryExecution']['Status']['State']
#             if state in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
#                 break
#             time.sleep(2)
#         if state != 'SUCCEEDED':
#             return None
#         result = self.athena.get_query_results(QueryExecutionId=exec_id)
#         rows = result['ResultSet']['Rows']
#         header = [col['VarCharValue'] for col in rows[0]['Data']]
#         data = [ [col.get('VarCharValue', '') for col in row['Data']] for row in rows[1:]]
#         df = pd.DataFrame(data, columns=header)
#         return df

# # --- Usage Example (uncomment for quick test) ---

# kb = BedrockKnowledgeBase(kb_id="your-kb-id")
# answers = kb.get_answers("What is the highest temperature recorded?")
# print("Answers:", answers)

# athena = AthenaQuery(db="newdata", output="s3://aws-athena-query-results-yourbucket/")
# df = athena.run_query("SELECT * FROM heartbeats WHERE date='2025-07-10';")
# print(df)
