import random
from models import *
from datasets import *
from feature_extractor import extract_features
import time
import logging
import datetime
import os, sys
import ConfigParser

class Harness:
  def __init__(self, configSection):
    self.section = configSection # The config section we're running.
    self.config = self.loadConfig(configSection)
    self.setupLog()

  def run(self):
    visDataObjects = self.load_data()
    features = self.compute_features(visDataObjects)
    labels = self.compute_labels(visDataObjects)
    modelData = ModelData(features, labels)
    trainer = ModelTrainer(Model)
  
    for modelKlass, score in trainer.train_and_test(modelData):
      print "\n"
      print modelKlass
      print score
      print "\n"

  def load_data(self):
    dataset = self.config.get(self.section, 'mapping')
    thisPath = os.path.abspath(os.path.dirname(__file__))
    mappingPath = os.path.join(thisPath, '..', 'data', 'data_sets', dataset)
    print "Using mapping: %s" % mappingPath
    exops = {"filename": mappingPath}
    vd = VisDataset(MappingExtractor, exops)
    return vd.getVisualizations()
  
  def compute_vis_features(self, vis):
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
  
  def compute_features(self, vds):
    return map(self.compute_vis_features, vds)
  
  def compute_labels(self, vds):
    return [vis.metadata.vistype for vis in vds]
    
  def setupLog(self):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S.txt')
    logdir = 'log'
    if not os.path.exists(logdir):
      os.makedirs(logdir)
    logging.basicConfig(filename=os.path.join(logdir, st), level=logging.INFO)
    logging.info("3..2..1...VRRRRROOMMMM")
  
  def loadConfig(self, name):
    thisPath = os.path.abspath(os.path.dirname(__file__))
    configFile = os.path.join(thisPath, '..', 'config.ini')
    config = ConfigParser.ConfigParser()
    config.read(configFile)
    if name not in config.sections():
      print "Error: config %s not found." % name
      return None
    else:
      print "Using config: %s" % name
      return config
  

# get the path to the datasets package
if __name__ == '__main__':
  # get an absolute path to the directory that contains mypackage
  #datasets_dir = os.path.dirname(os.path.join(os.getcwd(), __file__))
  #sys.path.append(os.path.normpath(os.path.join(datasets_dir, '..', '..')))
  #from datasets import ManyEyesExtractor,VisDataset,Vis,VisMetadata

  if len(sys.argv) == 1:
    print "Please run with the config name as argument"
  else:
    name = sys.argv[1]
    harness = Harness(name)
    harness.run()

  #run("../data/data_sets/many_eyes/mapping.txt")
  #run("../data/manyeyes_test")

#else:
#  from .. import ManyEyesExtractor,VisDataset,Vis,VisMetadata

