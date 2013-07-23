from datasets.extractors.exhibit_extractor import *

e = ExhibitExtractor()

for i in e.extract("../data/data_sets/exhibit/VIZ_*"):
  print i

