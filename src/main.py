import json
from fastapi import FastAPI
import uvicorn
from routes import router
from gprofiler import GProfiler

# Routing
app = FastAPI(
    title="Genome Browser API",
    description="...",
    version="1.0.0"
)
app.include_router(router, prefix="/api")

# Enable Swagger UI
app.openapi_url = "/openapi.json"
app.docs_url = "/docs"
app.redoc_url = "/redoc"

# MAIN
if __name__ == "__main__":

    gp = GProfiler(return_dataframe=True)
    data = gp.snpense(query=['rs11734132'])
    print(data['gene_names'])

    gp = GProfiler(return_dataframe=True)
    data = gp.convert(organism='hsapiens', query='*')
    print(data)

    # uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)