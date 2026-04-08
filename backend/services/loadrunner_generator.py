def generate_loadrunner(entries, correlations=[]):
    """
    entries: list of dicts with keys: method, url
    correlations: list of dicts with keys: variable, value, source_step
    """
    script = '#include "lrun.h"\n#include "web_api.h"\n\nAction()\n{\n'

    # Add correlations
    for c in correlations:
        script += f'''
web_reg_save_param("{c['variable']}",
    "LB=",
    "RB=",
    LAST);
'''

    # Add requests
    for i, e in enumerate(entries):
        url = e.get("url", "")
        method = e.get("method", "GET").upper()

        # Replace correlated values
        for c in correlations:
            if c['value'] in url:
                url = url.replace(c['value'], f'{{{c["variable"]}}}')

        if method == "GET":
            script += f'''
web_url("step{i}",
    "URL={url}",
    LAST);
'''
        elif method == "POST":
            script += f'''
web_submit_data("step{i}",
    "Action={url}",
    "Method=POST",
    LAST);
'''

    script += "\nreturn 0;\n}"
    return script