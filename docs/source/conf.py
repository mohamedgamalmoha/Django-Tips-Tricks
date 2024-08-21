# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project configuration ---------------------------------------------------
import os
import sys
from unittest.mock import MagicMock

import django

sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('../../src'))

# Specify the settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'


# Mock any modules not needed
class Mock(MagicMock):

    @classmethod
    def __getattr__(cls, name):
        return MagicMock()


MOCK_MODULES = ['factory']
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

# Initialize Django
django.setup()

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Django-Tips-&-Tricks'
copyright = '2024, M.Gamal'
author = 'M.Gamal'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',      # Automatically document from docstrings
    'sphinx.ext.napoleon',     # Support for Google and NumPy style docstrings
    'sphinx.ext.viewcode',     # Add links to highlighted source code
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']
exclude_patterns = [
    '*/__init__.py'
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
html_favicon = '_static/images/logo.png'
