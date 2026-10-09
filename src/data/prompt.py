"""Shared zero-shot/SFT task instruction: only question and schema enter input."""
PROMPT_VERSION = 'sqlite_zero_shot_v1'
SYSTEM = 'You are an expert SQL generator.'


def messages(question, schema):
    return [{'role':'system','content':SYSTEM}, {'role':'user','content':
        'Given the following database schema:\n\n'+schema+'\n\nQuestion:\n'+question+
        '\n\nGenerate a valid SQLite SQL query that answers the question.\n'
        'Return only the SQL query without explanation or Markdown.'}]
