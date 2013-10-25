import random
from models import *
from datasets import *
from operator import itemgetter
from feature_extractor import extract_features
import time
import logging
import datetime
import os, sys
import ConfigParser
import itertools
import time

class Harness:
  def __init__(self, configSection):
    self.section = configSection # The config section we're running.
    self.config = self.loadConfig(configSection)
    self.setupLog()
    self.log = logging.getLogger(__name__)
    self.log.propagate = True

  def run(self):
    self.log.info("3..2..1...VRRRRROOMMMM")
    visDataObjects = self.load_data()
    print visDataObjects
    features, labels = self.compute_features_and_labels(visDataObjects)
    # If these aren't the same, there is no point in continuing.
    assert(len(labels) == len(features))
    self.dump_points(features, labels)
    self.log.info("- %d data points loaded.", len(features))

    experiment_type = self.config.get(self.section, 'experiment')
    log.info("Running Model \"%s\"", experiment_type)
    if experiment_type == 'model0':
      self._model0(visDataObjects, features, labels)
    if experiment_type == 'model1':
      self._model1(visDataObjects, features, labels)
    else:
      log.fatal("Unknown experiment type: %s", experiment_type)

  def _model0(self, visDataObjects, features, labels):
    log.info("Model 0 Called")
    log.info(visDataObjects)
    log.info(features)
    log.info(labels)
    modelData = ModelData(features, labels)
    trainer = ModelTrainer(Model)
  
    for modelKlass, score in trainer.train_and_test(modelData):
      self.log.info("\n")
      self.log.info(modelKlass)
      self.log.info(score)
      self.log.info("\n")

  def _model1(self, visDataObjects, features, labels):
    """Ted's round one.

    Find max margin in:
      for t in vis_types:
        for x in columns:
          yield margin(x_axis | t, x)

    Repeat for y.

    Then we basis so (independently) pick the best axis assignment for a chart
    type.
    """
    pass

  def dump_points(self, features, labels):
    self.log.info("Read Data")
    self.log.info("===========================")
    labelCount = {}
    for label in labels:
      if label not in labelCount:
        labelCount[label] = 1
      else:
        labelCount[label] += 1
    thelist = sorted([(k,v) for k,v in labelCount.iteritems()], key=itemgetter(1))

    for tup in thelist:
      self.log.info("%d %s", tup[1], tup[0])

  def load_data(self):
    dataset_name = self.config.get(self.section, 'dataset')
    thisPath = os.path.abspath(os.path.dirname(__file__))
    if dataset_name == 'OldManyEyes':
      dataset = 'many_eyes/mapping.txt'
      mappingPath = os.path.join(thisPath, '..', 'data', 'data_sets', dataset)
      self.log.info("Using mapping: %s", mappingPath)
  
      exops = {"filename": mappingPath}
      vd = VisDataset(MappingExtractor, exops)
      return vd.getVisualizations()
    elif dataset_name == "ManyEyes":
      from datasets.extractors import ManyEyesExtractor
      ex = ManyEyesExtractor()
      mappingPath = os.path.join(thisPath, '..', 'data', 'manyeyes_crawler')
      opts = {'filename': mappingPath}
      vd = ex.extract(opts)
      return vd
    elif dataset_name == 'ggplot2':
      from datasets.extractors import GGPlotExtractor
      ex = GGPlotExtractor()
      mappingPath = os.path.join(thisPath, '..', 'data', 'data_sets', 'ggplot2/specs/*')
      opts = {'filepattern': mappingPath}
      vd = ex.extract(opts)
    else:
      raise Exception("Unknown dataset")
    return vd
  
  def compute_features_and_labels(self, vds):
    """Compute features and label for a vis data set.

    We do both at the same time to avoid reading in the set twice.

    """
    i = 0
    start = time.time()
    features = []
    labels = []
    cum_duration = 0
    dataset_name = self.config.get(self.section, 'dataset')
    max_points = int(self.config.get(self.section, 'maxpoints', 0))

    for vis in vds:
      if (i % 100 == 0) or (i >=  max_points):
        stop = time.time()
        duration = stop - start
        start = time.time()
        cum_duration += duration
        self.log.info("Loaded %d visualizations from Dataset \"%s\" in %ds (total: %ds)", i, dataset_name, duration, cum_duration)
      if i >= max_points:
        self.log.info("Stopping mode because reached configured maximum %d points", max_points)
        break
      features.append(self.features_for(vis))
      labels.append(self.label_for(vis))
      i += 1
    return features,labels

  def features_for(self, vis):
    # TODO: Depend on config for features computed.
    data = vis.data
    md = vis.metadata
  
    def axis_features(idx):
      axisname = data.dtype.names[idx]
      print data
      col = data[axisname]
      return extract_features(None, col, self.config, self.section)
  
    features = {}
    if len(md.axes) >= 2:
      # add x axis features
      features.update(axis_features(md.axes[0]))
  
      # add y axis features
      features.update(axis_features(md.axes[1]))
    return features
 
  def label_for(self, vis):
    # TODO: Depend on config for label computed.
    return vis.metadata.vistype

  def setupLog(self):

    formatter = logging.Formatter('%(asctime)s %(name)-10s %(levelname)-8s %(message)s')
    rootLogger = logging.getLogger('')

    # Add a handler for the screen
    if not rootLogger.handlers:
      console = logging.StreamHandler()
      rootLogger.addHandler(console)
    else:
      console = rootLogger.handlers[0]
    rootLogger.setLevel(logging.INFO)
    console.setFormatter(formatter)

    # Add a hdnaler for the filesystem
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S.txt')
    thisPath = os.path.abspath(os.path.dirname(__file__))
    logdir = os.path.join(thisPath, '..', 'log')
    if not os.path.exists(logdir):
      os.makedirs(logdir)
    self.logfile = os.path.abspath(os.path.join(logdir, st))
    fileHandler = logging.FileHandler(self.logfile, 'w')
    fileHandler.setFormatter(formatter)
    rootLogger.addHandler(fileHandler)

    rootLogger.info("Logging to %s", self.logfile)
  
  def loadConfig(self, name):
    thisPath = os.path.abspath(os.path.dirname(__file__))
    configFile = os.path.join(thisPath, '..', 'config.ini')
    config = ConfigParser.ConfigParser()
    config.read(configFile)
    if name not in config.sections():
      logging.error("Error: config %s not found." % name)
      return None
    else:
      logging.info("Using config: %s" % name)
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
