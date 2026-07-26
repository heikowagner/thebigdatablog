# Makefile for arXiv submission
# Requires: pdflatex, bibtex (or biber)

MAIN = main
BIB  = references

PDFLATEX = pdflatex -interaction=nonstopmode

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex $(BIB).bib
	-$(PDFLATEX) $(MAIN).tex
	bibtex    $(MAIN)
	-$(PDFLATEX) $(MAIN).tex
	-$(PDFLATEX) $(MAIN).tex

clean:
	rm -f $(MAIN).aux $(MAIN).bbl $(MAIN).blg $(MAIN).log $(MAIN).out $(MAIN).pdf

# arXiv-compatible: create a flat tarball with all LaTeX sources
arxiv: $(MAIN).pdf
	rm -f arxiv.tar.gz
	tar czf arxiv.tar.gz \
		$(MAIN).tex $(MAIN).bbl references.bib \
		figures/*.png
	@echo "Created arxiv.tar.gz"

.PHONY: all clean arxiv
