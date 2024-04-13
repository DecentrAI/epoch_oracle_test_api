import uuid
import random

from datetime import datetime, timedelta, timezone
from collections import defaultdict

import json

PREFIX = '0xai_'

class DummyEpochManager:
  """
  This is a dummy epoch manager that will be used to simulate the epoch manager in the actual system.
  
  """
  
  def __init__(self):
    self.__init_nodes()    
    return

  def __random_init_node(self, node_addr):
    if node_addr.startswith(PREFIX) and len(node_addr) >= 45: # 49 actually
      current_epoch = self.get_current_epoch()
      for x in range(1, current_epoch):
        self.nodes[node_addr][x] = random.randint(0, 255)
    return
  
  def __init_nodes(self, num_nodes=5):
    self.nodes = defaultdict(lambda: defaultdict(int))
    current_epoch = self.get_current_epoch()      
    self.nodes[PREFIX + '1' * 44] = {x : 255 for x in range(1, current_epoch)}
    for _ in range(num_nodes):
      node_addr = self.__generate_addr()
      self.__random_init_node(node_addr)
    return    
  
  def __generate_addr(self, seed:str=''):
    str_uid = str(uuid.uuid4()).replace('-', '') + str(uuid.uuid4()).replace('-', '')
    rest = 49 - len(PREFIX) - len(seed)   
    return PREFIX + str(seed) + str_uid[:rest]


  ## similar with original code
  
  def get_epoch_id(self, date):
    GENESYS_EPOCH_DATE = '2024-03-10 00:00:00'
    genesis_date = datetime.strptime(GENESYS_EPOCH_DATE, '%Y-%m-%d %H:%M:%S')
    genesis_date = genesis_date.replace(tzinfo=timezone.utc)
    
    elapsed = (date - genesis_date).days
    return elapsed
    
  def get_current_date(self):
    return datetime.now(timezone.utc)  
  
  ## end similar with original code


  # the actual api  

  def get_current_epoch(self):
    return self.get_epoch_id(self.get_current_date())
     
  def get_nodes_list(self):
    return list(self.nodes.keys())
  
  def get_node_epoch(self, node_addr, epoch):
    if node_addr not in self.nodes:
      return None
    return self.nodes[node_addr][epoch]
  
  def get_node_last_epoch(self, node_addr):
    current_epoch = self.get_current_epoch()
    result = self.get_node_epoch(node_addr, current_epoch - 1)
    return result
  
  def get_node_epochs(self, node_addr):
    if node_addr not in self.nodes:
      return None
    return self.nodes[node_addr]
  
  
  # other 
  def init_node(self, node_addr):
    """This actually is NOT a valid API in the actual system. This is a helper function for testing."""
    if node_addr not in self.nodes:
      if not node_addr.startswith(PREFIX) or len(node_addr) < 45:
        node_addr = PREFIX + node_addr + '0' * (44 - len(node_addr))
    self.__random_init_node(node_addr)
    data = self.get_node_epochs(node_addr)    
    return node_addr, data
  


if __name__ == '__main__':
  
  # here are a few tests
  
  eng = DummyEpochManager()
  print("Current epoch:", eng.get_current_epoch())
  nodes = eng.get_nodes_list()
  print("Nodes list:", nodes)
  print("Node {} last epoch: {}".format(nodes[0], eng.get_node_last_epoch(nodes[0])))
  print("Node {} last epoch: {}".format(nodes[-1], eng.get_node_last_epoch(nodes[-1])))
  # add a new node
  node_addr, data = eng.init_node("1234567890")
  print("Node {} epochs: {}".format(node_addr, json.dumps(eng.get_node_epochs(node_addr))))
  