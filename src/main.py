import uuid
import os
import signal

from fastapi import FastAPI, Request, Response, HTTPException
from starlette.responses import JSONResponse

from datetime import datetime, timedelta

from time import time

from dummy_epoch_manager import DummyEpochManager, __VER__

START_TIME = time()

WORKER_ID = "0xai_" + str(uuid.uuid4()).replace('-', '0') + str(uuid.uuid4()).replace('-', '1')
WORKER_ID = WORKER_ID[:49]

INFO = f"""
## Simple demo/mockup FastAPI application 

  - designed to be run in a Docker container and exposed to the internet using ngrok 
  - for development and testing purposes of the Epoch Oracle
  - can be used for smart contract testing and development

> Worker ID: {WORKER_ID}

"""

eng = DummyEpochManager()

app = FastAPI(
    title="Simple Epoch Oracle API",
    summary="Simple Epoch Oracle API using FastAPI, uvicorn, Docker and ngrok",
    description=INFO,
    version=__VER__,
    # terms_of_service="http://example.com/terms/",
    # contact={
    #     "name": "API Support",
    #     "url": "http://www.example.com/support",
    #     "email": "support@example.com",
    # },
    # license_info={
    #     "name": "Apache 2.0",
    #     "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    # },
)

# Simple in-memory rate limiter
REQUEST_LIMIT = 5 # demo limit
time_window = 10  # demo window in seconds
request_counts = {}


def get_response(dct_data: dict):
  str_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  dct_data['server_id'] = WORKER_ID
  dct_data['server_time'] = str_date
  dct_data['server_current_epoch'] = eng.get_current_epoch()
  uptime_seconds = round(time() - START_TIME, 2)
  dct_data['server_uptime'] = str(timedelta(seconds=uptime_seconds))
  return dct_data


@app.middleware("http")
async def naive_rate_limitter(request: Request, call_next):
  client_ip = request.client.host
  current_time = time()
  
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


@app.on_event("startup")
async def startup_event():
  # rectangle-print Starting up the app
  eng.P(f"Running server v{__VER__} worker ID {WORKER_ID}")
  eng.setup()
  return



@app.get("/")
async def root():
  return get_response({
    "msg": f"Epoch API Demo. Please use /docs for extended documentation.", 
    "version": __VER__
  })


@app.get("/node_epoch")
async def node_status(node_addr: str, epoch: int):
  """Get a particualar epoch status of a give node by its address and the epoch no."""
  result = eng.get_node_epoch(node_addr, epoch)  
  if result is None:
    raise HTTPException(status_code=404, detail=f"Node {node_addr}not found")
  return get_response({
    "node": node_addr, "epoch": epoch, "value": result,
  })


@app.get("/node_epochs")
async def node_status(node_addr: str):
  """Get all the epochs statuses of a give node by its address."""
  result = eng.get_node_epochs(node_addr)
  if result is None:
    raise HTTPException(status_code=404, detail=f"Node {node_addr} not found")
  return get_response({
    "node": node_addr, "epochs": result, 
  })


@app.get("/nodes_list")
async def nodes_list():
  """Get the list of all nodes"""
  nodes = eng.get_nodes_list()
  return get_response({
    "nodes": nodes, 
  })


@app.get("/node_last_epoch")
async def node_last_epoch(node_addr: str):
  """Get the last epoch status of a give node by its address."""
  result = eng.get_node_last_epoch(node_addr)
  if result is None:
    raise HTTPException(status_code=404, detail=f"Node {node_addr} not found")
  return get_response({
    "node": node_addr, 
    "last_epoch": result, 
    "last_epoch_prc" : round(result / 255, 4),
  })


@app.get("/init_node")
async def init_node(node_addr: str):
  """This NOT a valid API endpoint in the actual system. This is a helper function for testing/initing new addresses."""
  addr, epochs = eng.init_node(node_addr)
  return get_response({
    "node": addr, "status": "initialized", "epochs" : epochs
  })


@app.post("/oracle_restart")
async def shutdown_server():
  """This NOT a valid API endpoint in the actual system. This is a helper function for manual remote update."""
  # Schedule the server to be shut down
  os.kill(os.getpid(), signal.SIGTERM)
  # Return a response to the client (note: this response may not be sent successfully if the server shuts down too quickly)
  return Response(status_code=200, content=f'Server {WORKER_ID} v{__VER__} shutting down...')