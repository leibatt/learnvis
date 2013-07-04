import inspect
import imp
import os

def run_klass(klass, table):
  o = klass()
  val = o.process(table)
  return (o.name, val)

def list_klasses(ROOT, filter_func):
  for dirpath, dirnames, fnames in os.walk(ROOT):
    for fname in fnames:
      try:
        (f, path, desc) = imp.find_module(fname, dirpath)
        with f:
          module = imp.load_module("feature", file, path, desc)
          members = inspect.getmembers(module)
          classtuples = filter(lambda tup: inspect.isclass(tup[1]), members)

          for (klassname, klass) in classtuples:
            if filter_func(klass):
              yield klass
      except:
        print "oi"




def extract_features(ROOT, filter_func, table):
  """
  Args
    ROOT: root directory containing feature definitions
    filter_func: function to filter feature objects
    table is in some (currently unspecified format)
  """
  features = {}

  for klass in list_klasses(ROOT, filter_func):
    (name, val) = run_klass(klass, table)
    features[name] = val

  return features



