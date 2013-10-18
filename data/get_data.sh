#!/bin/bash

scp -r learnvis@hammer.csail.mit.edu:~/data_sets .

scp -r learnvis@hammer.csail.mit.edu:~/*.zip .
unzip manyeyes_crawler.zip


mkdir -p ./data_sets/ggplot2
cd ./data_sets/ggplot2
tar -xf ../../../scrapers/ggplot2/ggplotdata.tar.gz
cd -
