import loader
import features
import argparse
from visdata import VisData

parser = argparse.ArgumentParser(description='Process csv/tsv files listed in mapper file and compute features.')
parser.add_argument('filename', metavar = 'filename',type=str,help='mapper file to parse')
parser.add_argument('--delim', metavar = 'delimiter',type=str,help='delimiter of the mapper file',default='\t')
parser.add_argument('--outfile', metavar = 'outfile',type=str,help='file to write results to',default='out.txt')
parser.add_argument('--skip',metavar = 'skip',type=int,help='number of lines to skip before reading the mapper data',default=0)

args = parser.parse_args()
#print args
with open(args.outfile,'w') as outfile:
    counter = 0
    vismap = loader.loadMapper(args.filename,delim=args.delim,skip=args.skip)
    for i,visobj in enumerate(vismap):
        print "source:",visobj.source,", url:",visobj.url,",location:",visobj.location,",label:",visobj.label,"column_names:",",".join(visobj.column_names)
        results = features.get_features_new(visobj,include=['a','g','p','s','c'])
        #print results
        outfile.write(args.delim.join([str(counter),str(visobj.label)]))
        outfile.write(args.delim+args.delim.join(map(str,results)))
        outfile.write('\n')
        counter = counter + 1
        #break
