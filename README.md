# Simple CouchDB Python Bindings

Squab is a simple and minimal library that provides [CouchDB](http://couchdb.apache.org/) bindings for your Python
application. The HTTP heavy lifting is provided by [Requests](http://www.python-requests.org/).

## Status

There are still some some rough edges in the API implementation to be ironed out. (eg implicit create vs update)
But it's otherwise usable for your project, and a lot simpler to grock than other implementations.

## Usage

Define your document model:

```
# documents.py

from squab.base import BaseDocument


class Zone(BaseDocument):
    """ Zone Object """
    type = 'zone'

    def update(self, name, data, serial):
        super(Zone, self).update(
            serial=serial,
            data=data,
            _id=name)

    def parse(self):
        super(Zone, self).update(
            name=self['_id'],
            serial=self['serial'],
            data=self['data'],
            _id=self['_id'],
            _rev=self['_rev'])

```

Create the document

```
from squab.connection import CouchConnection
from .documents import Zone

# CouchDB connection
connection = CouchConnection(host='localhost', db='mydb', user='me', password='mypass', ignore_missing=False)

# Create a document
_id = 'example.com'
doc = Zone(connection=connection, _id=_id)
doc.update(name=obj.domain_name,
           serial=obj.serial,
           data=obj.render())
doc.save()

```

## Installation

    pip install git+https://github.com/panubo/python-squab.git#egg=squab

## Development

### Testing

    py.test tests -v -s

### Release tagging

    git tag -a v0.3.0 -m 'Release'
    git push --tags

### Upload

    python setup.py sdist upload -r voltgrid
