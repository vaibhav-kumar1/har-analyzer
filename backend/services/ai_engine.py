import requests, json

GEMINI_API_KEY = "AIzaSyD7HmjFOo2LOCF2SIld8DQPM2IEs2u4_kk"

def analyze_with_ai(entries, correlations):
    prompt = f"""
    Analyze HAR:
    - Correlation rules
    - Parameterization
    - Flow

    ENTRIES: {json.dumps(entries)[:2000]}
    CORRELATIONS: {json.dumps(correlations)[:1000]}
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={AIzaSyD7HmjFOo2LOCF2SIld8DQPM2IEs2u4_kk}"

    try:
        res = requests.post(url, json={
            "contents": [{"parts": [{"text": prompt}]}]
        })
        return res.json()
    except:
        return {"error": "AI failed"}