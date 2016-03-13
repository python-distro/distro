
# Name of this package
PACKAGENAME = ld

# Additional options for Sphinx
SPHINXOPTS = -v

# Paper format for the Sphinx LaTex/PDF builder.
# Valid values: a4, letter
SPHINXPAPER = a4

# Sphinx build subtree.
SPHINXBUILDDIR = build_docs

# Directory where conf.py is located
SPHINXCONFDIR = docs

# Directory where input files for Sphinx are located
SPHINXSOURCEDIR = .

# Sphinx build command (Use 'pip install sphinx' to get it)
SPHINXBUILD = sphinx-build

# Internal variables for Sphinx
SPHINXPAPEROPT_a4     = -D latex_paper_size=a4
SPHINXPAPEROPT_letter = -D latex_paper_size=letter
ALLSPHINXOPTS = -d $(SPHINXBUILDDIR)/doctrees -c $(SPHINXCONFDIR) \
                $(SPHINXPAPEROPT_$(SPHINXPAPER)) $(SPHINXOPTS) \
                $(SPHINXSOURCEDIR)

.PHONY: help
help:
	@echo 'Please use "make <target>" where <target> is one of'
	@echo "  release   - build a release and publish it"
	@echo "  dev       - prepare a development environment (includes tests)"
	@echo "  instdev   - prepare a development environment (no tests)"
	@echo "  install   - install into current Python environment"
	@echo "  test      - test from this directory using tox, including test coverage"
	@echo "  publish   - upload to PyPI"
	@echo "  html      - generate docs as standalone HTML files in: $(SPHINXBUILDDIR)/html"
	@echo "  pdf       - generate docs as PDF (via LaTeX) for paper format: $(SPHINXPAPER) in: $(SPHINXBUILDDIR)/pdf"
	@echo "  man       - generate docs as manual pages in: $(SPHINXBUILDDIR)/man"
	@echo "  docchanges   - generate an overview of all changed/added/deprecated items in docs"
	@echo "  doclinkcheck - check all external links in docs for integrity"
	@echo "  doccoverage  - run coverage check of the documentation"
	@echo "  clean     - remove any temporary build products"
	@echo "  clobber   - remove any build products"

.PHONY: release
release: publish
	@echo "$@ done."

.PHONY: dev
dev: instdev test
	@echo "$@ done."

.PHONY: instdev
instdev:
	pip install -r dev-requirements.txt
	python setup.py develop
	@echo "$@ done."

.PHONY: install
install:
	python setup.py install
	@echo "$@ done."

.PHONY: test
test:
	sudo pip install 'tox>=1.7.2'
	tox
	@echo "$@ done."

.PHONY: publish
publish:
	python setup.py sdist upload
	@echo "$@ done; uploaded the ld package to PyPI."

.PHONY: html
html:
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) $(SPHINXBUILDDIR)/html
	@echo "$@ done; the HTML pages are in $(SPHINXBUILDDIR)/html."

.PHONY: pdf
pdf:
	$(SPHINXBUILD) -b latex $(ALLSPHINXOPTS) $(SPHINXBUILDDIR)/pdf
	@echo "Running LaTeX files through pdflatex..."
	$(MAKE) -C $(SPHINXBUILDDIR)/pdf all-pdf
	@echo "$@ done; the PDF files are in $(SPHINXBUILDDIR)/pdf."

.PHONY: man
man:
	$(SPHINXBUILD) -b man $(ALLSPHINXOPTS) $(SPHINXBUILDDIR)/man
	@echo "$@ done; the manual pages are in $(SPHINXBUILDDIR)/man."

.PHONY: docchanges
docchanges:
	$(SPHINXBUILD) -b changes $(ALLSPHINXOPTS) $(SPHINXBUILDDIR)/changes
	@echo
	@echo "$@ done; the doc changes overview file is in $(SPHINXBUILDDIR)/changes."

.PHONY: doclinkcheck
doclinkcheck:
	$(SPHINXBUILD) -b linkcheck $(ALLSPHINXOPTS) $(SPHINXBUILDDIR)/linkcheck
	@echo
	@echo "$@ done; look for any errors in the above output " \
	      "or in $(SPHINXBUILDDIR)/linkcheck/output.txt."

.PHONY: doccoverage
doccoverage:
	$(SPHINXBUILD) -b coverage $(ALLSPHINXOPTS) $(SPHINXBUILDDIR)/coverage
	@echo "$@ done; the doc coverage results are in $(SPHINXBUILDDIR)/coverage/python.txt."

.PHONY: clean
clean:
	rm -rf build $(PACKAGENAME).egg-info
	@echo "$@ done."

.PHONY: clobber
clobber: clean
	rm -rf $(SPHINXBUILDDIR)
	@echo "$@ done."
