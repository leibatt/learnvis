import random
from model import Model
from fscore import Fscore
from datasets.base import BaseDataset

def run():
  visDataObjects = load_data()
  features = compute_features(visDataObjects)
  labels = compute_labels(visDataObjects)
  modelData = ModelData(features, labels)
  harness = ModelTrainer(models)
  for modelKlass, score in harness.train_and_test(modelData):
    pass
  return models


if __name__ == '__main__':
  dataset = BaseDataset()
  train_and_test(dataset, 2, False)

