This code scrapes the ggplot source code 

# Running

clone the ggplot2 code into this directory

    git clone https://github.com/hadley/ggplot2.git

Extract and print R example code fragments from the source as a JSON object

    python parseGGDocs.py ggplot2/R > code

The JSON object is of the form

    filename: <code string>

There needs to be a step to run the code, but once it is run, then construct each ggplot2 object and run
in R:

    plotToJSON(plot, datas, specs)

