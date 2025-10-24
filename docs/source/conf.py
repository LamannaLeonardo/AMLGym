# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

# Add the repo root to sys.path so autodoc can import your package
sys.path.insert(0, os.path.abspath('../..'))

project = 'AMLGym: benchmarking action model learning.'
copyright = '2025, Roni Stern, Leonardo Lamanna, Argaman Mordoch, Yarin Benyamin, Pascal Lauer, Brendan Juba, Gregor Behnke, Christian Muise, Pascal Bercher, Mauro Vallati, Kai Xi, Omar Wattad, Omer Eliyahu'
author = 'Roni Stern, Leonardo Lamanna, Argaman Mordoch, Yarin Benyamin, Pascal Lauer, Brendan Juba, Gregor Behnke, Christian Muise, Pascal Bercher, Mauro Vallati, Kai Xi, Omar Wattad, Omer Eliyahu'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',            # core autodoc
    'sphinx.ext.napoleon',           # Google / NumPy style parsing
    'sphinx.ext.autosummary',        # generate summary stubs
    'sphinx.ext.viewcode',           # add links to source
    'sphinx_autodoc_typehints',      # show type hints in signature
    'sphinx.ext.todo',
    'sphinx.ext.mathjax',
    "nbsphinx",
]

# Add a button for opening the notebook in google colab
nbsphinx_prolog = r"""
.. raw:: html

    <a href="https://colab.research.google.com/github/LamannaLeonardo/AMLGym/blob/main/docs/source/{{ env.doc2path(env.docname, base=None) }}" target="_blank">
    <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
    </a>
"""
# nbsphinx_allow_errors = True  # compile despite notebook errors


templates_path = ['_templates']
exclude_patterns = []

# napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True

# include module docstrings (modules.rst generation)
autodoc_default_options = {
    'members': True,
    'undoc-members': False,
    'show-inheritance': True,
    'inherited-members': True,
}

autosummary_generate = True
autoclass_content = "both"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_css_files = ['custom.css']   # for small style tweaks
html_theme_options = {
    'collapse_navigation': False,
    'navigation_depth': 4,
    'titles_only': False,
}
