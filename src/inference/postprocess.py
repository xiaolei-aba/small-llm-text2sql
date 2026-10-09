"""Strip only a complete outer Markdown code fence; never repair SQL."""
import re


def extract_sql(raw):
    text = raw.strip()
    match = re.fullmatch(r'```(?:sql)?\s*\n?(.*?)\n?```', text, re.I | re.S)
    return match.group(1).strip() if match else text
