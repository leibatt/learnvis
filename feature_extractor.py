import inspect
import imp
import os

def run_klass(klass, table):
  o = klass()
  val = o.process(table)
  return (o.name, val)

def list_klasses(filter_func):
  import features
  from features import BaseFeature
  members = inspect.getmembers(features)
  classtuples = filter(lambda tup: inspect.isclass(tup[1]), members)

  for (klassname, klass) in classtuples:
    if klass == BaseFeature: continue
    if filter_func is None or filter_func(klass):
      yield klass


def extract_features(filter_func, table):
  """
  Args
    ROOT: root directory containing feature definitions
    filter_func: function to filter feature objects
    table is in some (currently unspecified format)
  """
  features = {}

  for klass in list_klasses(filter_func):
    (name, val) = run_klass(klass, table)
    features[name] = val

  return features


if __name__ == "__main__":

  print extract_features(None, [0,1,2,3])
