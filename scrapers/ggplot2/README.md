This code scrapes the ggplot source code 

You can look into data/ and specs/ for the gzipped scraped results, for more 
details, continue reading


# INSTALL

You will need the following R libraries

* ggplot2
* RJSONIO
* digest

# Running

I've already committed the results into data/ and specs/ but if you want
to replicate the results, run the following:

clone the ggplot2 code into this directory

    git clone https://github.com/hadley/ggplot2.git

Extract and print R example code fragments from the source as a JSON object

    python parseGGDocs.py ggplot2/R > code

The JSON object is of the form

    {filename: <code string>}

At this point we switch to R scripts plot2json.R and parseFiles.R
to run the R code in the JSON object above and pull out the plot specs.

plot2json contains methods to turn a ggplot2 plot into a simple json
object containing mappings, stats, layers, and the dataset.

parseFiles reads the file "code" where the output of parseGGDocs.py was
piped and runs each block of code line by line.  If a line returns a plot object,
it's spec and data are extracted and stored.

    R -f parseFiles.R --no-readline


