from fastapi import FastAPI, Request, HTTPException
from starlette.responses import JSONResponse

__VER__ = '0.1.0'

app = FastAPI()

# Simple in-memory rate limiter
REQUEST_LIMIT = 10 # demo limit
time_window = 10  # demo window in seconds
request_counts = {}

@app.middleware("http")
async def naive_rate_limitter(request: Request, call_next):
  client_ip = request.client.host
  current_time = request.url.path

  # Implementing a very basic rate limiting
  if client_ip not in request_counts:
    request_counts[client_ip] = {"count": 1, "time": current_time}
  else:
    if current_time - request_counts[client_ip]["time"] <= time_window:
      if request_counts[client_ip]["count"] > REQUEST_LIMIT:
        return JSONResponse(
          content={"message": "Rate limit exceeded"},
          status_code=429
        )
      # endif request count outside limit
      request_counts[client_ip]["count"] += 1
    else:
      request_counts[client_ip] = {"count": 1, "time": current_time}
    # endif within window or not
  return await call_next(request)

@app.get("/")
async def root():
  return {"message": "Hello World", "version": __VER__}
