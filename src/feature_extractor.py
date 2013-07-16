import inspect
import imp
import os

def run_klass(klass, table):
  o = klass()
  features = o.process(table)
  return (o.name, features)

def list_klasses(filter_func):
  import features.column as features
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
    filter_func: function to filter feature objects
    table:       a structured numpy array containing the data
  """
  ret = {}

  for klass in list_klasses(filter_func):
    (name, features) = run_klass(klass, table)
    if not features: continue
    for key, val in features.iteritems():
      ret["%s__%s" % (name, key)] = val

  print ret 
  return ret


if __name__ == "__main__":

  print extract_features(None, [0,1,2,3])
