# get the path to the datasets package
if __name__ == '__main__':
  import os, sys
  # get an absolute path to the directory that contains mypackage
  datasets_dir = os.path.dirname(os.path.join(os.getcwd(), __file__))
  sys.path.append(os.path.normpath(os.path.join(datasets_dir, '..', '..')))
  from datasets import ManyEyesExtractor, MappingExtractor, ExhibitExtractor, GGPlotExtractor
else:
  from .. import ManyEyesExtractor, MappingExtractor, ExhibitExtractor, GGPlotExtractor

#initialize extractor class
x = ManyEyesExtractor()

#setup extraction inputs and options
#assumes you downloaded new many eyes dataset
ex_ops = {'filename':'../../../data/manyeyes_crawler'} 

#call extractor's extract function to get 
vds1 = x.extract(ex_ops)

#try this for another extractor
y = MappingExtractor()

#assumes you downloaded old many eyes data set
ex_ops = {'filename':'../../../data/data_sets/many_eyes/mapping.txt'}

vds2 = y.extract(ex_ops)

#try for exhibit extractor
z = ExhibitExtractor()

ex_ops = {'filepattern':'../data/data_sets/exhibit/VIZ_*'}
vds3 = z.extract(ex_ops)

#try for exhibit extractor
ge = GGPlotExtractor()

ex_ops = {'filepattern':'../../data/data_sets/ggplot2/specs/*'}
vds4 = ge.extract(ex_ops)


for i in vds4:
  print i

