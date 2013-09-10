# This file takes a JSON file of {filename: CODESTRING} 
# as input, and extracts specs from every plot it can find
#
# Plots are found by executing each files CODESTRING 
# line by line, and checking if the class is equal to
# a ggplot object

source("plot2json.R")
library(RJSONIO)

# Iteratively runs each line in codeblock
# If a line fails, it's prepended to the next line.  This
# covers the case where a statement is broken across multiple lines:
#
#     ggplot() +
#     geom_point()
#
procCodeblock = function(codeblock, datafolder, specfolder) {
  allspecs = vector()
  lines = strsplit(codeblock, '\n')[[1]]
  buffer = ""
  for (idx in 1:length(lines)) {
    line = lines[idx]
    buffer = sprintf("%s\n%s", buffer, line)
    if (length(line) > 0) {
      resp = try(eval(parse(text=buffer)))
      if (all(class(resp) != "try-error")) {
        if (any(class(resp) == "ggplot")) {
          buffer = ""
          json = plotToJSON(resp)

          # Now write the spec & data out
          json$spec = setFileMD(json$spec, json$data, datafolder, specfolder)

          if (!file.exists(json$spec$datafile)) {
            write.csv(json$data, file=json$spec$datafile)
          }

          write(toJSON(json$spec), file=json$spec$specfile)

        }
      }
    }
  }
}




datafolder = "./datas/"
specfolder = "./specs/"
codes = fromJSON(readLines("code"))
for (codeblock in codes) {
  specs = procCodeblock(codeblock, datafolder, specfolder)
}


