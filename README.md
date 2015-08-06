# Simple CouchDB Python Bindings

Squab is a simple and minimal library that provides [CouchDB](http://couchdb.apache.org/) bindings for your application. The HTTP heavy lifting is provided by [Requests](http://www.python-requests.org/).

## Status

There are still some some rough edges in the API implementation to be ironed out. But it's otherwise usable for your project.

## Install

    pip install git+https://github.com/panubo/python-squab.git#egg=squab

## Development

### Testing

    py.test tests -v -s

### Release tagging
    git tag -a v0.3.0 -m 'Release'
    git push --tags

### Upload
    python setup.py sdist upload -r voltgrid
