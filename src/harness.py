import random
from models import *
from models.model0 import Model0
from models.model1 import Model1
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
    visualizations = self.load_data()
    experiment_type = self.config.get(self.section, 'experiment')
    if experiment_type == 'model0':
      self.model = Model0
    elif experiment_type == 'model1':
      self.model = Model1
    else:
      self.log.fatal("Unknown experiment type: '%s'", experiment_type)
      return

    log.info("Running Model \"%s\"", experiment_type)
    self.trainer = ModelTrainer(self.config, self.section, self.model)
    for modelKlass, score in self.trainer.train_and_test(visualizations):
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
    from sklearn.multiclass import OutputCodeClassifier
    from sklearn.svm import LinearSVC
    clf = OutputCodeClassifier(LinearSVC(random_state=0),
      code_size=2, random_state=0)
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
