from fastapi import FastAPI
import uvicorn

import routes


app = FastAPI()
app.include_router(routes.router)
DETA_PROJECT_KEY= "a01rek6x_uoMgF7eRCoDyPAPzfAJQNXTsVAyCcb4s"

if __name__ == "__main__":
    uvicorn.run("app:app", port=9000, reload=True)
