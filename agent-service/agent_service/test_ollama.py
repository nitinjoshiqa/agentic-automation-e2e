import sys
try:
    from langchain.llms import Ollama
except Exception as e:
    print('IMPORT_ERROR', e)
    sys.exit(2)

try:
    llm = Ollama(url='http://localhost:11434', model='mistral')
    out = llm('Say hello in one short sentence.')
    print('OK')
    print(out)
except Exception as e:
    print('LLM_ERROR', e)
    sys.exit(3)

