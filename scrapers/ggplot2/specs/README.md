Spec files. Each is a JSON object of the form

    {
      layers: [
        {                                   # spec for a single layer 
          geom:
          stat:
          mapping:
        }
      ],

      mapping: { },                         # base aesthetic mapping
      md5: <md5 of datafile>,
      datafile: data/<data file name>.csv,  # use to get csv data
      specfile: specs/<spec file name>.json
    }


The filename is 

    <MD5 of data file>-<MD5 of json structure>.json