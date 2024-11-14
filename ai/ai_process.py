from multiprocessing import Queue
from ai.overlay import ActionClassifier
from ai.overlay_w_prob import ActionClassifierWProb

def ai_process(to_ai_queue: Queue, ai_action_queue: Queue):
  clf = ActionClassifier(to_ai_queue, ai_action_queue)
  clf_w_prob = ActionClassifierWProb(to_ai_queue, ai_action_queue)
  classifierType = 2
  while True:
    if (classifierType == 1):
      clf.perform_inference_from_json()
    else:
      clf_w_prob.perform_inference_from_json()

        