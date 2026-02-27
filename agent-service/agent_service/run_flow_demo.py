import json
import sys
import traceback
import os

RESULT_PATH = os.path.join(os.path.dirname(__file__), 'demo_result.json')
ERROR_PATH = os.path.join(os.path.dirname(__file__), 'demo_error.txt')

# Attempt to import the real RAGService
try:
    from .rag import RAGService
    real_available = True
except Exception as e:
    RAG_IMPORT_ERROR = e
    real_available = False

# fallback quick demo functions
from .quick_demo import write_feature, write_pages


def write_result(obj):
    try:
        with open(RESULT_PATH, 'w', encoding='utf-8') as f:
            json.dump(obj, f, indent=2)
    except Exception as e:
        print('Failed to write result file:', e)


def write_error(text):
    try:
        with open(ERROR_PATH, 'w', encoding='utf-8') as f:
            f.write(text)
    except Exception as e:
        print('Failed to write error file:', e)


def run_real_flow(requirement, module='demo'):
    try:
        rag = RAGService()
        print('INFO: Using real RAGService')
        out_features = rag.generate_features(requirement_text=requirement, module=module)
        written_features = out_features.get('written_features', [])
        page_hints = out_features.get('page_hints', [])
        written_pages = []
        if page_hints:
            pages_res = rag.generate_pages(page_hints=page_hints, module=module)
            written_pages = pages_res.get('written_pages', [])
        out = {'mode': 'real', 'written_features': written_features, 'written_pages': written_pages}
        print(json.dumps(out, indent=2))
        write_result(out)
        return 0
    except Exception as e:
        tb = traceback.format_exc()
        print('ERROR: RAG runtime error', e)
        print(tb)
        write_error('RAG runtime error:\n' + tb)
        return 2


def run_fallback(requirement, module='demo'):
    print('INFO: Using fallback quick_demo')
    feat = write_feature(module)
    pages = write_pages(module)
    out = {'mode': 'fallback', 'written_features': [os.path.abspath(feat)], 'written_pages': [os.path.abspath(p) for p in pages]}
    print(json.dumps(out, indent=2))
    write_result(out)
    return 0


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--module', default='demo')
    parser.add_argument('--requirement', default='As a user I want to log in with username and password so I can access inventory')
    args = parser.parse_args()

    if real_available:
        code = run_real_flow(args.requirement, args.module)
        if code != 0:
            print('Falling back to quick demo due to error')
            run_fallback(args.requirement, args.module)
    else:
        print('RAGService import failed:', repr(RAG_IMPORT_ERROR))
        write_error('IMPORT_ERROR:\n' + repr(RAG_IMPORT_ERROR))
        run_fallback(args.requirement, args.module)
