import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import mcc_api

project = "python_mcc_api"
copyright = "2023-2024 James C"
author = "James C"
release = mcc_api.__version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx"
]

intersphinx_mapping = {
    "gql": ("https://gql.readthedocs.io/en/stable", None),
    "graphql": ("https://graphql-core-3.readthedocs.io/en/latest", None),
    "python": ("https://docs.python.org/3", None)
}

exclude_patterns = []

html_theme = "bizstyle"
html_theme_options = {
    "sidebarwidth": "400px"
}
html_sidebars = {
    "**": [
        "globaltoc.html"
    ]
}
