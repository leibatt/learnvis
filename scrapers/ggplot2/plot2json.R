# This file extracts a simple plot spec and data file from a ggplot2 plot object.
# We currently extract:
#   Layers:
#     geom name
#     stat name
#     layer mapping (if any)
#   Global aesthetic mapping
#   Data (ignores layer specific data)
#
library(RJSONIO)
library(ggplot2)
library(digest)

plotToJSON = function(p, datafolder, specfolder) {

  # base aesthetic mappings
  base_mapping = p$mapping
  base_names = names(base_mapping)
  print(p$mapping)

  # layers
  f = function(layer) {
    geom_name = layer$geom$objname
    stat_name = layer$stat$objname
    mapping = layer$mapping
    list(geom=geom_name, stat=stat_name, mapping=mapping)
  }
  plot = list()
  plot$layers = lapply(p$layers, f)
  plot$mapping = p$mapping

  md5 = digest(p$data)
  datafilename = sprintf("%s/%s.csv", datafolder, md5)
  specfilename = sprintf("%s/%s.json", specfolder, md5)

  # write if './FILEROOT/md5.csv' doesn't exist
  if (!file.exists(datafilename)) {
    write.csv(p$data, file=datafilename)
  }

  write(toJSON(plot), specfilename)
}


p = ggplot(data=head(diamonds,n=100), aes(carat, price)) 
p = p + geom_line() + geom_point(aes(color=cut)) 
p = p + facet_grid(.~color)

plotToJSON(p, "/tmp", "/tmp")