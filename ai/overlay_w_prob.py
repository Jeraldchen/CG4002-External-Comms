from pynq import Overlay
from pynq import PL
from pynq import allocate
from sklearn.metrics import confusion_matrix
from multiprocessing import *
from scipy.fft import fft
import numpy as np
import csv
import time
import json
import tkinter as tk


INPUT_SIZE = 96
OUTPUT_SIZE = 9
OTHERS_THRESHOLD_VALUE = 0.85
SHIELD_THRESHOLD_VALUE = 0.83
BOMB_THRESHOLD_VALUE = 0.9
VOLLEY_THRESHOLD_VALUE = 0.7

def median(data):
  data = np.array(data) 
  return float(np.median(data))  # Ensure the return type is float

def iqr(data):
  # Convert input to NumPy array if it isn't already
  data = np.array(data)
  return float(np.percentile(data, 75) - np.percentile(data, 25))  # Ensure the return type is float

def mean_first_quarter(data):
  # Convert input to NumPy array if it isn't already
  data = np.array(data)
  return float(np.mean(data[: len(data) // 4]))  # Ensure the return type is float

def mean_second_quarter(data):
  # Convert input to NumPy array if it isn't already
  data = np.array(data)
  return float(np.mean(data[len(data) // 4 : len(data) // 2]))  # Ensure the return type is float

def zero_crossing_rate(data):
  # Convert input to NumPy array if it isn't already
  data = np.array(data)
  return float(np.sum(np.diff(np.sign(data))) / (2 * len(data)))  # Ensure the return type is float

def rms(data):
  data = np.array(data)
  return np.sqrt(np.mean(data ** 2))

def jerk_mean(data):
  data = np.array(data)
  return np.mean(np.diff(data))

def jerk_std(data):
  data = np.array(data)
  return np.std(np.diff(data))

def peak_to_peak(data):
  data = np.array(data)
  return np.ptp(data)

def autocorrelation(data):
  data = np.array(data)
  return np.correlate(data, data, mode='full')[len(data) - 1]

def fft_std(data):
  fft_values = fft(data)
  fft_magnitude = np.abs(fft_values)
  return np.std(fft_magnitude)

def energy(data):
  return np.sum(data ** 2) / len(data)

def fft_range(data):
  fft_values = fft(data)
  fft_magnitude = np.abs(fft_values)
  return np.max(fft_magnitude) - np.min(fft_magnitude)


class ActionClassifierWProb():
  def __init__(self, queue1, queue2):
    PL.reset()
    load_start = time.time()
    self.all_actions = {"0": "no action", "1": "shield", "2": "bomb", "3": "reload", "4": "basket", "5": "soccer", "6": "volley", "7": "bowl", "8": "logout"}
    self.to_ai_queue = queue1
    self.ai_action_queue = queue2
    self.ol = Overlay('ai/apana3_newthreshold.bit')
    self.dma = self.ol.axi_dma_0
    self.nn = self.ol.predict_0
    self.nn.write(0x00, 0x81) # start and auto restart
    self.dma_send = self.dma.sendchannel
    self.dma_recv = self.dma.recvchannel
    print(self.dma_send.running)
    print(self.dma_recv.running)
    self.input_stream = allocate(shape=(INPUT_SIZE, ), dtype='int32')
    self.output_stream = allocate(shape=(9, ), dtype='int32')
    load_end = time.time()
    print(f"Loading time: {(load_end - load_start):.4f}s")

  def print_dma_channel_status(self, channel, name='dma'):
    print(f'{name}.running =', channel.running)
    print(f'{name}.idle =', channel.idle)
    print(f'{name}.error =', channel.error)
    print(f'status =', hex(channel._mmio.read(channel._offset + 4)))
    
  def print_dma_channels_status(self):
    self.print_dma_channel_status(self.dma_recv, name='dma_rec')
    print()
    self.print_dma_channel_status(self.dma_send, name='dma_send')

  def process_data(self,json_packet):
    imu_data = np.array(json_packet["imu_data"])
    sensor_data = imu_data.T


    features = []
    # Iterate over each sensor's data (each row in imu_data)
    scaling_params = np.load('ai/scaling_params_fresh_try.npy', allow_pickle=True).item()
    sensor_index = 0

    for sensor in sensor_data:
      # Retrieve min and max values for this sensor
      min_val = scaling_params[f'sensor_{sensor_index}']['min']
      max_val = scaling_params[f'sensor_{sensor_index}']['max']
      sensor_index += 1

      # Apply min-max normalization
      scaled_sensor_data = (sensor - min_val) / (max_val - min_val)
      
      # Append the features for this sensor
      # features.append(rms(scaled_sensor_data))
      # features.append(jerk_std(scaled_sensor_data))
      # features.append(jerk_mean(scaled_sensor_data))
      # features.append(iqr(scaled_sensor_data))
      # features.append(mean_first_quarter(scaled_sensor_data))
      # features.append(mean_second_quarter(scaled_sensor_data))
      # features.append(peak_to_peak(scaled_sensor_data))
      # features.append(autocorrelation(scaled_sensor_data))
      # features.append(jerk_std(scaled_sensor_data))
      # features.append(jerk_mean(scaled_sensor_data))
      # features.append(mean_second_quarter(scaled_sensor_data))
      # features.append(peak_to_peak(scaled_sensor_data))
      # features.append(fft_std(scaled_sensor_data))
      # features.append(energy(scaled_sensor_data))
      # features.append(fft_range(scaled_sensor_data))
      features.append(jerk_mean(scaled_sensor_data))
      features.append(iqr(scaled_sensor_data))
      features.append(mean_first_quarter(scaled_sensor_data))
      features.append(mean_second_quarter(scaled_sensor_data))
      features.append(peak_to_peak(scaled_sensor_data))
      features.append(fft_std(scaled_sensor_data))
      features.append(energy(scaled_sensor_data))
      features.append(fft_range(scaled_sensor_data))

    print(len(features))

    return features

  def softmax(self, logits):
    exp_logits = np.exp(logits - np.max(logits))  # Subtracting max for numerical stability
    return exp_logits / np.sum(exp_logits)

  def infer(self, data):
    for i in range(INPUT_SIZE):
      self.input_stream[i] = int(data[i] * 65536.0)
    
    # print("Input Stream: ", self.input_stream)
    self.dma_send.transfer(self.input_stream) 
    self.dma_recv.transfer(self.output_stream)
    # self.print_dma_channels_status()
    self.dma_send.wait()
    self.dma_recv.wait()
    print("Output stream:", self.output_stream)
    probabilities = np.asarray(self.output_stream)
    probabilities = self.softmax(probabilities)
    
    # Print each probability with the class index
    print("Output Probabilities:")
    for i, prob in enumerate(probabilities):
      action = self.all_actions[f"{i}"]
      print(i, f" {action}: Probability = {prob:.4f}")
    
    # Determine the class with the highest probability
    gesture = 0
    max_probability = probabilities[0]
    THRESHOLD_VALUE = OTHERS_THRESHOLD_VALUE
    initial_gesture = probabilities.argmax()
    if (initial_gesture == 1):
      THRESHOLD_VALUE = SHIELD_THRESHOLD_VALUE
    elif (initial_gesture == 2 or initial_gesture == 4):
      THRESHOLD_VALUE = BOMB_THRESHOLD_VALUE
    elif (initial_gesture == 6):
      THRESHOLD_VALUE = VOLLEY_THRESHOLD_VALUE
    else:
      THRESHOLD_VALUE = OTHERS_THRESHOLD_VALUE
    if (probabilities.max() > THRESHOLD_VALUE):
      gesture = probabilities.argmax()
      max_probability = probabilities.max()
    gesture_class = self.all_actions[f"{gesture}"]
    print(f"Predicted Class: {gesture_class} with Probability = {max_probability:.4f}")

    return gesture

  def perform_inference_from_json(self):
    # For Actual
    json_packet = self.to_ai_queue.get()
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
    print("Action: ", self.all_actions[f"{predicted_output}"])
    # if int(predicted_output) != 0:
    json_sendback = {
      "player_id": player_id,
      "action": self.all_actions[f"{predicted_output}"]
    }
    self.ai_action_queue.put(json_sendback)

  def perform_inference_from_json_multiple(self, file):
    start_time = time.time()
    total_predictions = 0
    correct_predictions = 0
    true_labels = []
    predictions = []
    with open(file) as test_data_json:
      json_data = json.load(test_data_json)
        
    for json_packet in json_data:
      player_id = json_packet["player_id"]
      label = json_packet["label"]
      extracted_features = self.process_data(json_packet)
      # print("extracted_features: ", extracted_features)
      predicted_output = self.infer(extracted_features)
      true_labels.append(label)
      predictions.append(predicted_output)
      if predicted_output == label:
        correct_predictions += 1
      total_predictions += 1
      print("Prediction: ", predicted_output)
      print("Label: ", self.all_actions[f"{label}"])
      print("Action: ", self.all_actions[f"{predicted_output}"])

    end_time = time.time()
    execution_time = end_time - start_time
    print("Total execution time for all samples: ", execution_time, "s")
    print(f"Accuracy: {100.0 * (correct_predictions)/total_predictions}%")
    print(f"No. of wrong predictions: {total_predictions - correct_predictions} out of {total_predictions}")

    conf_matrix = confusion_matrix(true_labels, predictions)
    print(conf_matrix)

if __name__ == "__main__":
  clf = ActionClassifierWProb(Queue(), Queue())
  clf.perform_inference_from_json_multiple('ai/train.json')

