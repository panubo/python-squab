from uuid import uuid4 as uuid

import requests
import json

from squab.exceptions import NotPersistedException, CouchRequestException, CouchConnectionException


class DocumentInterface(dict):
    """ This is the interface that the Document objects will implement """

    def update(self, *args, **kwargs):
        super(DocumentInterface, self).__init__(*args, **kwargs)

    def json(self, *args, **kwargs):
        return json.dumps(self, *args, **kwargs)

    def parse(self, *args, **kwargs):
        raise NotImplementedError()

    def save(self, *args, **kwargs):
        raise NotImplementedError()

    def delete(self, *args, **kwargs):
        raise NotImplementedError()


class BaseDocument(DocumentInterface):
    type = None
    _rev = None
    _id = None
    _deleted = False

    def __init__(self, connection, type=None, _id=None):
        self.connection = connection
        if type is not None:
            self.type = type
        # try load type from document
        if _id is not None:
            self._id = _id
            j = self._get_json(_id=_id)
            if j.get('type', None) is not None:
                self.type = j.get('type')
            self._rev = j.get('_rev')
            super(BaseDocument, self).update(j)
        else:
            # objects must have an _id
            self._id = str(uuid())
            super(BaseDocument, self).update(_id=_id)
        super(BaseDocument, self).__init__(type=self.type, _id=self._id)

    def update(self, *args, **kwargs):
        """ Update arbitrary k/v pairs in the document  """
        if '_rev' in kwargs and kwargs['_rev'] is None:
            kwargs.pop('_rev')
        if kwargs.get('type', None) is None:
            kwargs['type'] = self.type
        if kwargs['_id'] is None:
            kwargs['_id'] = self._id
        super(BaseDocument, self).__init__(*args, **kwargs)  # Update base dictionary object

    def save(self):
        headers = {'Content-type': 'application/json'}
        try:
            url = '%s/%s/%s' % (self.connection.host, self.connection.db, self['_id'])
            r = requests.put(url, data=json.dumps(self), headers=headers, auth=(self.connection.user, self.connection.password))
            if r.status_code != 201:
                if not self.connection.ignore_missing:
                    raise CouchRequestException('Error: %s. %s' % (r.status_code, r.text))
                else:
                    return True
            else:
                result = json.loads(r.text)
                self.__setitem__('_rev', result['rev'])
                self.__setitem__('_id', result['id'])
                self._rev = result['rev']
                self._id = result['id']
        except requests.ConnectionError, e:
            raise CouchConnectionException("Error: %s" % str(e))

    def delete(self):
        if self._rev:
            try:
                url = '%s/%s/%s?rev=%s' % (self.connection.host, self.connection.db, self['_id'], self['_rev'])
                r = requests.delete(url, auth=(self.connection.user, self.connection.password))
                if r.status_code == 404 and self.connection.ignore_missing:
                    pass
                elif r.status_code != 200:
                    raise CouchRequestException('Error: %s. %s' % (r.status_code, r.text))
                self._deleted = True
            except requests.ConnectionError, e:
                raise CouchRequestException("Error: %s" % str(e))
        else:
            raise NotPersistedException('Tried to delete non existent document')

    def _get_json(self, _id):
        headers = {}
        try:
            url = '%s/%s/%s' % (self.connection.host, self.connection.db, _id)
            r = requests.get(url, data=json.dumps(self), headers=headers, auth=(self.connection.user, self.connection.password))
            if r.status_code == 404 and self.connection.ignore_missing:
                return json.loads('{}')
            elif r.status_code != 200:
                raise CouchRequestException('Error: %s. %s' % (r.status_code, r.text))
            return json.loads(r.text)
        except requests.ConnectionError, e:
            raise CouchConnectionException("Error: %s" % str(e))
