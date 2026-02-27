from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from .rag import RAGService
from .prompts import FEATURE_SYSTEM_PROMPT, PAGE_OBJECT_SYSTEM_PROMPT
from .tools import run_maven_clean_verify

app = FastAPI(title="Agent Service")

# Initialize RAG service (singleton)
rag = RAGService()

class GenerateFeaturesRequest(BaseModel):
    requirement_text: str
    module: str = "generated"

class GeneratePagesRequest(BaseModel):
    page_hints: list
    module: str = "generated"

class IngestRequest(BaseModel):
    path: str

class RunTestsRequest(BaseModel):
    repo_root: str

class AnalyzeFailureRequest(BaseModel):
    failure_log: str

class RunFlowRequest(BaseModel):
    repo_root: str = ".."
    requirement_text: str = None
    module: str = "generated"
    site_url: str = None
    # flags to control steps
    do_ingest: bool = True
    do_generate_features: bool = True
    do_generate_pages: bool = True
    do_dedupe: bool = True
    do_run_tests: bool = False
    do_analyze_failure: bool = False
    use_scanner: bool = False

@app.get('/health')
async def health():
    return {"status": "ok"}

@app.post('/ingest')
async def ingest(req: IngestRequest):
    try:
        result = rag.ingest_directory(req.path)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/generate-features')
async def generate_features(req: GenerateFeaturesRequest):
    try:
        result = rag.generate_features(requirement_text=req.requirement_text, module=req.module)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/generate-pages')
async def generate_pages(req: GeneratePagesRequest):
    try:
        result = rag.generate_pages(page_hints=req.page_hints, module=req.module)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/dedupe-pages')
async def dedupe_pages(module: str = 'generated'):
    try:
        result = rag.dedupe_pages(module=module)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/run-tests')
async def run_tests(req: RunTestsRequest):
    try:
        code, out, err = run_maven_clean_verify(req.repo_root)
        return {'returncode': code, 'stdout': out, 'stderr': err}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/analyze-failure')
async def analyze_failure(req: AnalyzeFailureRequest):
    try:
        result = rag.analyze_failure(req.failure_log)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post('/run-flow')
async def run_flow(req: RunFlowRequest):
    """Master orchestrator to run pipeline phases based on flags.
    Returns a combined report with outputs for each executed step.
    """
    report = {'steps': []}
    try:
        # 1) Ingest
        if req.do_ingest:
            ingest_path = req.repo_root
            ingest_result = rag.ingest_directory(ingest_path)
            report['steps'].append({'ingest': ingest_result})

        # 2) Generate features
        features_output = None
        if req.do_generate_features:
            if not req.requirement_text:
                raise HTTPException(status_code=400, detail='requirement_text is required when do_generate_features is true')
            features_output = rag.generate_features(requirement_text=req.requirement_text, module=req.module)
            report['steps'].append({'generate_features': features_output})

        # 3) Generate pages (use page_hints from features if available)
        pages_output = None
        if req.do_generate_pages:
            page_hints = []
            if features_output:
                page_hints = features_output.get('page_hints', [])
            pages_output = rag.generate_pages(page_hints=page_hints, module=req.module, use_scanner=req.use_scanner, site_url=req.site_url)
            report['steps'].append({'generate_pages': pages_output})

        # 4) Dedupe
        if req.do_dedupe:
            dedupe_report = rag.dedupe_pages(module=req.module)
            report['steps'].append({'dedupe': dedupe_report})

        # 5) Run tests
        test_result = None
        if req.do_run_tests:
            code, out, err = run_maven_clean_verify(req.repo_root)
            test_result = {'returncode': code, 'stdout': out, 'stderr': err}
            report['steps'].append({'run_tests': test_result})

            # 6) Analyze failures if requested
            if req.do_analyze_failure and code != 0:
                # pass stderr to analyzer
                analysis = rag.analyze_failure(err)
                report['steps'].append({'analyze_failure': analysis})

        return report
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    uvicorn.run('agent_service.main:app', host='0.0.0.0', port=8080, reload=True)
