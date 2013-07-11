import loader
import features
import argparse

parser = argparse.ArgumentParser(description='Process csv/tsv file and compute features.')
parser.add_argument('filename', metavar = 'filename',type=str,help='a file to parse')
parser.add_argument('--delim', metavar = 'delimiter',type=str,help='delimiter of the data file',default='\t')
parser.add_argument('--skip',metavar = 'skip',type=int,help='number of lines to skip before reading the data',default=0)

args = parser.parse_args()
#print args
vismap = loader.loadMapper('/home/leibatt/projects/vldb_demo_04-1-2013/mapping.txt',skip=0)
raw_data = loader.loadFile(args.filename,delim=args.delim,skip=args.skip)
#print raw_data
results = features.get_features(raw_data)
print results
