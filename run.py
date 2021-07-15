import uvicorn

if __name__ == "__main__":
    uvicorn.run("script:app", host="0.0.0.0", port=1087, log_level="info", reload=True)
