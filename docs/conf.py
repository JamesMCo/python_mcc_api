import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import mcc_api

project = "python_mcc_api"
copyright = "2023 James C"
author = "James C"
release = mcc_api.__version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary"
]

exclude_patterns = []

html_theme = "alabaster"
html_theme_options = {
    "page_width": "1200px",
    "sidebar_width": "400px"
}
html_sidebars = {
    "**": [
        "about.html",
        "localtoc.html"
    ]
}
