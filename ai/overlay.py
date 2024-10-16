from pynq import Overlay
from pynq import PL
from pynq import allocate
from sklearn.preprocessing import MinMaxScaler
from multiprocessing import *
import numpy as np
import csv
import time
import json

INPUT_SIZE = 60

# Define constants based on the HLS stream type
# DATA_WIDTH = 32 // 8  # 4 bytes
# USER_WIDTH = 2 // 8  # 1 bbyte
# LAST_WIDTH = 5 // 8  # 1 byte (this can be treated as a flag)
# ID_WIDTH = 6 // 8  # 1 byte

# Total size per element in bytes
# element_size = DATA_WIDTH + USER_WIDTH + LAST_WIDTH + ID_WIDTH  # Total size of a single stream element

# Create functions to extract features
def median(data):
  return np.median(data)

def iqr(data):
  return np.percentile(data, 75) - np.percentile(data, 25)

def mean_first_quarter(data):
  return np.mean(data[: len(data) // 4])

def mean_second_quarter(data):
  return np.mean(data[len(data) // 4 : len(data) // 2])

def zero_crossing_rate(data):
  return np.sum(np.diff(np.sign(data))) / (2 * len(data))


class ActionClassifier():
  def __init__(self, queue1, queue2):
    PL.reset()
    load_start = time.time()
    self.all_actions = {"0": "no_action", "1": "shield", "2": "bomb", "3": "reload", "4": "basket", "5": "soccer", "6": "volley", "7": "bowl", "8": "logout"}
    self.to_ai_queue = queue1
    self.ai_action_queue = queue2
    self.ol = Overlay('ai/predict3.bit')
    self.dma = self.ol.axi_dma_0
    self.nn = self.ol.predict_0
    self.nn.write(0x00, 0x81) # start and auto restart
    self.dma_send = self.dma.sendchannel
    self.dma_recv = self.dma.recvchannel
    print(self.dma_send.running)
    print(self.dma_recv.running)
    self.input_stream = allocate(shape=(INPUT_SIZE, ), dtype='float32')
    self.output_stream = allocate(shape=(1, ), dtype='int32')
    load_end = time.time()
    print(f"Loading time: {(load_end - load_start):.4f}s")


  def process_data(self, json_packet):
    imu_data = json_packet["imu_data"]

    features = []
    single_action = [[] for _ in range(12)]
    # Iterate over each sensor's data (each row in imu_data)
    for sensor_data in imu_data:
      # print(len(sensor_data))
      for i, value in enumerate(sensor_data):
        single_action[i].append(value)
    for sensor in single_action:
      # Compute the features
      sensor_iqr = iqr(sensor)
      sensor_median = median(sensor)
      first_quarter_mean = mean_first_quarter(sensor)
      second_quarter_mean = mean_second_quarter(sensor)
      zcr = zero_crossing_rate(sensor)

      # Append the features for this sensor
      features.extend([sensor_iqr, sensor_median, first_quarter_mean, second_quarter_mean, zcr])

    return features

  def infer(self, data):
    for i in range(INPUT_SIZE):
      self.input_stream[i] = data[i] * 65536.0
    
    print("Input Stream: ", self.input_stream)
    self.dma_send.transfer(self.input_stream) 
    self.dma_recv.transfer(self.output_stream)
    self.dma_send.wait()
    self.dma_recv.wait()
    print("Output stream:", self.output_stream)
    gesture = self.output_stream[0]
    return gesture

  def perform_inference_from_json(self):
    # For Actual
    json_packet = self.to_ai_queue.get()
    # with open(file, ) as test_data_json:
    #   json_packet = json.load(test_data_json)
    start_time = time.time()
    player_id = json_packet["player_id"]
    print("extracting features")
    extracted_features = self.process_data(json_packet)
    print("features processed")
    print("starting inference")
    predicted_output = self.infer(extracted_features)
    print("end inference")
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time: ", execution_time, "s")
    print("Prediction: ", predicted_output)
    print("Label: No_action")
    print("Action: ", self.all_actions[f"{predicted_output}"])
    json_sendback = {
      "player_id": player_id,
      "action": self.all_actions[f"{predicted_output}"]
    }
    self.ai_action_queue.put(json_sendback)

  # def perform_inference_from_json_multiple(self, file):
  #   start_time = time.time()
  #   with open(file) as test_data_json:
  #     json_data = json.load(test_data_json)
        
  #   for json_packet in json_data:
  #     player_id = json_packet["player_id"]
  #     extracted_features = self.process_data(json_packet)
  #     predicted_output = self.infer(extracted_features)

  #     print("Prediction: ", predicted_output)
  #     print("Label: ", json_packet["label"])
  #     print("Action: ", self.all_actions[f"{predicted_output}"])

  #   end_time = time.time()
  #   execution_time = end_time - start_time
  #   print("Total execution time for all samples: ", execution_time, "s")

