from multiprocessing import Queue
from ai.overlay import ActionClassifier

def ai_process(to_ai_queue: Queue, ai_action_queue: Queue):
  clf = ActionClassifier(to_ai_queue, ai_action_queue)
  while True:
    clf.perform_inference_from_json()

        