'''Request creation and handling to USPTO API

'''
import requests
from dataclasses import dataclass

from consumers import ConsumerUSPTOReturnData

class RESTApiAccessDataException(Exception):
    pass

@dataclass
class RESTApiAccessData:
    base_url : str
    apis : dict[str]
    metadata_api_label :str
    record_api_label : str
    headers : dict[str]

    def url_records(self, key):
        try:
            url_ = self.base_url + '/' + self.apis[key] + '/' + self.record_api_label
        except KeyError as e:
            raise RESTApiAccessDataException('Incorrect API key: {}. Available options: {}'.format(e, list(self.apis.keys())))
        url_ = url_[:8] + url_[8:].replace('//','/')
        return url_

    def url_metadata(self, key):
        try:
            url_ = self.base_url + '/' + self.apis[key] + '/' + self.metadata_api_label
        except KeyError as e:
            raise RESTApiAccessDataException('Incorrect API key: {}. Available options: {}'.format(e, list(self.apis.keys())))
        url_ = url_[:8] + url_[8:].replace('//','/')
        return url_

uspto_api_access = RESTApiAccessData(
    base_url='https://developer.uspto.gov/ds-api/',
    apis={
        'rejections' : 'oa_rejections/v2',
        'enriched citation' : 'enriched_cited_reference_metadata/v2',
        'office actions text' : 'oa_actions/v1'
    },
    metadata_api_label='fields',
    record_api_label='records',
    headers={'Accept' : 'application/json'}
)

def do_func(method, url, data=None, **kwargs):
    if method == 'get':
        r = requests.get(url=url, **kwargs)
    elif method == 'post':
        r = requests.post(url=url, data=data, **kwargs)
    else:
        raise ValueError('Only methods allowed are `get` and `post`, not `{}`'.format(method))

    if r.status_code == 200:
        return r.json()
    else:
        return r

def retrieve_metadata_for_(api_key, **kwargs):
    return do_func(method='get', url=uspto_api_access.url_metadata(api_key), **kwargs)

def retrieve_records_for_(api_key, data, **kwargs):
    return do_func(method='post', url=uspto_api_access.url_records(api_key), data=data, **kwargs)


class USPTOAPIReader(object):
    '''Bla bla

    '''
    def __init__(self,
                 api_name,
                 consumer_keys=None,
                 verify_api=False
                 ):
        self.api_name = api_name
        self.consumer_keys = consumer_keys
        self.verify_api = verify_api

        self.consumer = ConsumerUSPTOReturnData(
            keys2read=self.consumer_keys
        )

    @property
    def container(self):
        return self.consumer.container

    def __repr__(self):
        return self.container.__repr__()

    def retrieve_api_metadata(self):
        return retrieve_metadata_for_(self.api_name, verify=self.verify_api)

    def retrieve_by_patent_application_number_(self, patent_application_number):
        '''Bla bla

        '''
        rc = retrieve_records_for_(
            self.api_name,
            data={
                'criteria' : 'patentApplicationNumber:{}'.format(patent_application_number),
                'start' : '0',
                'rows': '100'
            },
            verify=self.verify_api
        )
        return rc

    def read_by_patent_application_number_(self, patent_application_number):
        '''Bla bla

        '''
        self.consumer.append(
            self.retrieve_by_patent_application_number_(patent_application_number)
        )
        self.consumer._remove_lists()

    def save_to_(self, fp, mode='a'):
        '''Bla bla

        '''
        self.consumer.dump_to_(fp=fp, mode=mode)
