mkdir -p source/_static source/_templates
sphinx-apidoc -M -f -n -o source ../spoly
make html
