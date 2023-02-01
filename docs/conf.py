import pagseguro

extensions = [
    "sphinx.ext.autodoc",
]

templates_path = ["_templates"]

source_suffix = ".rst"

master_doc = "index"

project = "django-pagseguro2"
copyright = "2020, Allisson Azevedo"

version = pagseguro.__version__.rsplit(".", 1)[0]
release = pagseguro.__version__

exclude_patterns = ["_build"]

pygments_style = "sphinx"

html_theme = "default"

html_static_path = ["_static"]

htmlhelp_basename = "django-pagseguro2doc"
