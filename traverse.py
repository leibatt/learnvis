import os
import argparse
import traceback
import features
import loader

parser = argparse.ArgumentParser(description='Process csv/tsv files and compute features.')
parser.add_argument('dirname', metavar = 'dirname',type=str,help='directory to look for files')
parser.add_argument('filename', metavar = 'filename',type=str,help='a file to write the results to')

args = parser.parse_args()
dirname = args.dirname
outfilename = args.filename
total_files = 0
total_parsed = 0
with open(outfilename,"a") as of:
    for root,dirs,filenames in os.walk(dirname):
        for f in filenames:
           full_path = os.path.join(root,f)
           l = len(f)
           if l > 4 and f[l-4:l] == '.csv':
               total_files = total_files + 1
               print "analyzing",os.path.join(root,f)
               try:
                   raw_data = loader.loadFile(full_path,delim=',',skip=1)
                   results = features.get_features(raw_data)
                   of.write('\t'.join([str(full_path),str(results['density']),str(results['density_minus_one']),str(results['density_all_nums']),str(results['density_strict']),str(results['fnumcols']),str(results['hasdate']),str(results['sum_covariance']),str(results['sum_abs_covariance']),str(results['max_abs_covariance']),str(results['total_unique_labels']),str(results['first_unique_labels'])])+'\n')
                   #print results
                   total_parsed = total_parsed + 1
               except Exception as e:
                   print "error occured while trying to parse",f,":"
                   print traceback.format_exc()
           elif (l > 4 and f[l-4:l] == '.tsv') or f == 'data.txt':
               total_files = total_files + 1
               print "analyzing",os.path.join(root,f)
               try:
                   raw_data = loader.loadFile(full_path,delim='\t',skip=1)
                   results = features.get_features(raw_data)
                   of.write('\t'.join([str(full_path),str(results['density']),str(results['density_minus_one']),str(results['density_all_nums']),str(results['density_strict']),str(results['fnumcols']),str(results['hasdate']),str(results['sum_covariance']),str(results['sum_abs_covariance']),str(results['max_abs_covariance']),str(results['total_unique_labels']),str(results['first_unique_labels'])])+'\n')
                   #print results
                   total_parsed = total_parsed + 1
               except Exception as e:
                   print "error occured while trying to parse",f,":"
                   print traceback.format_exc()

print "successfully parsed %r out of %r files found" % (total_parsed,total_files)
