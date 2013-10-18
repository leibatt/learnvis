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

plotToJSON = function(p) {
  # base aesthetic mappings
  base_mapping = p$mapping
  base_names = names(base_mapping)
  print(p$mapping)

  # Layers
  # extracts geom, stat, and aes mapping for each layer
  f = function(layer) {
    geom_name = layer$geom$objname
    stat_name = layer$stat$objname
    mapping = layer$mapping
    list(geom=geom_name, stat=stat_name, mapping=mapping)
  }
  plot = list()
  plot$layers = lapply(p$layers, f)
  plot$mapping = p$mapping

  return(list(spec=plot, data=p$data))
}

setFileMD = function(spec, data, datafolder, specfolder) {
  # compute IDs for the data and spec files
  md5 = digest(data)
  specid = sprintf("%s-%s", md5, digest(spec))
  datafilename = sprintf("%s/%s.csv", datafolder, md5)
  specfilename = sprintf("%s/%s.json", specfolder, specid)

  spec$datamd5 = md5
  spec$datafile = datafilename
  spec$specfile = specfilename
  return(spec)
}


writeSpec = function(spec, data) {
  if (!file.exists(spec$datafile)) {
    write.csv(data, file=spec$datafile)
  }
  write(toJSON(spec), file=spec$specfile)
  return(spec)
}



p = ggplot(data=head(diamonds,n=100), aes(carat, price)) 
p = p + geom_line() + geom_point(aes(color=cut)) 
p = p + facet_grid(.~color)

ret = plotToJSON(p)
ret$spec = setFileMD(ret$spec, ret$data, "/tmp", "/tmp")
writeSpec(ret$spec, ret$data)