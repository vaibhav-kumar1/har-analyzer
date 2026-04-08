def generate_jmx(entries):
    xml = "<jmeterTestPlan>\n"
    for e in entries:
        xml += f"""
<HTTPSamplerProxy>
<stringProp name="HTTPSampler.path">{e['url']}</stringProp>
<stringProp name="HTTPSampler.method">{e['method']}</stringProp>
</HTTPSamplerProxy>
"""
    xml += "</jmeterTestPlan>"
    return xml