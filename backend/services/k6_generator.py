def generate_k6(entries, correlations):
    script = """
import http from 'k6/http';
import { sleep } from 'k6';

export default function () {
"""

    for e in entries:
        if e["method"] == "GET":
            script += f'http.get("{e["url"]}");\n'
        else:
            script += f'http.post("{e["url"]}", {{}});\n'
        script += "sleep(1);\n"

    script += "}"
    return script