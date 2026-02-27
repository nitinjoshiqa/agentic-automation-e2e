import traceback
try:
    from .rag import RAGService
    print('IMPORT_OK')
except Exception as e:
    tb = traceback.format_exc()
    with open('rag_import_error.txt','w',encoding='utf-8') as f:
        f.write(tb)
    print('IMPORT_FAILED')
    print(tb)

