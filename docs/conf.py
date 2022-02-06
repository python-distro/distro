# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import datetime
import os
import sys

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath(".."))

import distro  # noqa: E402

# -- Project information -----------------------------------------------------

project = "distro"
copyright = f"{datetime.date.today().year}, Nir Cohen, Andreas Maier"
author = "Nir Cohen, Andreas Maier"

# The short X.Y version.
# Note: We use the full version in both cases.
version = distro.__version__  # type: ignore

# The full version, including alpha/beta/rc tags
release = version


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages. See
# https://www.sphinx-doc.org/en/master/usage/theming.html or a list of builtin
# themes.
html_theme = "classic"


# -- Options for intersphinx extension ------------------------------------
# For documentation, see
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html

# Defines the prefixes for intersphinx links and the targets they resolve to.
# Use Python 3.7 as that is the last version to include
# platform.linux_distribution() and platform.dist(). Example RST source for
# 'py' prefix:
#     :py:func:`platform.dist`
intersphinx_mapping = {"py": ("https://docs.python.org/3.7", None)}
