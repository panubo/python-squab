# Squab - Simple CouchDB Python Bindings

## Install

    pip install git+https://github.com/panubo/squab.git#egg=squab 

## Development

### Testing

    py.test tests -v -s

### Release tagging
    git tag -a v0.3.0 -m 'Release'
    git push --tags

### Upload
    python setup.py sdist upload -r voltgrid
