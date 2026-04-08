import json

def extract_values(obj, prefix=""):
    values = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            values.update(extract_values(v, prefix + k + "."))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            values.update(extract_values(v, prefix + str(i) + "."))
    else:
        values[prefix[:-1]] = str(obj)
    return values


def build_correlation(entries):
    value_map = {}
    correlations = []

    for i, e in enumerate(entries):
        resp_values = extract_values(e["response"])
        for k, v in resp_values.items():
            if len(v) > 6:
                value_map[v] = (i, k)

    for i, e in enumerate(entries):
        req_str = json.dumps(e["request"])
        for val, (src, key) in value_map.items():
            if val in req_str and src < i:
                correlations.append({
                    "value": val,
                    "source": src,
                    "target": i,
                    "variable": f"var_{key.replace('.', '_')}"
                })

    return correlations