import random
from models import *
from datasets import *
from feature_extractor import extract_features


def load_data(fname):
  #exops = {"filename": fname}
  #vd = VisDataset(ManyEyesExtractor, exops)
  exops = {"filename": fname}
  vd = VisDataset(MappingExtractor, exops)
  return vd.getVisualizations()


def compute_vis_features(vis):
  data = vis.data
  md = vis.metadata

  def axis_features(idx):
    axisname = data.dtype.names[idx]
    col = data[axisname]
    return extract_features(None, col)

  features = {}
  if len(md.axes) >= 2:
    # add x axis features
    features.update(axis_features(md.axes[0]))

    # add y axis features
    features.update(axis_features(md.axes[1]))
  return features

def compute_features(vds):
  return map(compute_vis_features, vds)

def compute_labels(vds):
  return [vis.metadata.vistype for vis in vds]
  


def run(fname):
  visDataObjects = load_data(fname)
  features = compute_features(visDataObjects)
  labels = compute_labels(visDataObjects)
  modelData = ModelData(features, labels)
  trainer = ModelTrainer(Model)
  for modelKlass, score in trainer.train_and_test(modelData):
    print "\n"
    print modelKlass
    print score
    print "\n"





# get the path to the datasets package
if __name__ == '__main__':
  import os, sys
  # get an absolute path to the directory that contains mypackage
  datasets_dir = os.path.dirname(os.path.join(os.getcwd(), __file__))
  sys.path.append(os.path.normpath(os.path.join(datasets_dir, '..', '..')))
  from datasets import ManyEyesExtractor,VisDataset,Vis,VisMetadata

  run("../data/data_sets/many_eyes/mapping.txt")
  #run("../data/manyeyes_test")


else:
  from .. import ManyEyesExtractor,VisDataset,Vis,VisMetadata


