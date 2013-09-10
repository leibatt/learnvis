Spec files. Each is a JSON object of the form

    {
      layers: [
        {   # spec for a single layer 
          geom:
          stat:
          mapping:
        }
      ],

      mapping: { }  # base aesthetic mapping
    }


The filename is 

    <MD5 of data file>-<MD5 of json structure>.json