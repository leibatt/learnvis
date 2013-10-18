all: paper

paper: main.tex
	pdflatex main && bibtex main && bibtex main && pdflatex main


clean: 
	rm -f *.dvi *.aux *.log *.blg *.toc *.bbl *~ *.lof *.lot
