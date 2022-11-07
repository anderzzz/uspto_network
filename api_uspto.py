'''Request creation and handling to USPTO API

'''
import requests
from dataclasses import dataclass

@dataclass
class RESTApiAccessData:
    base_url : str
    apis : dict[str]
    metadata_api_label :str
    record_api_label : str
    headers : dict[str]

    def url_records(self, key):
        url_ = self.base_url + '/' + self.apis[key] + '/' + self.record_api_label
        url_ = url_[:8] + url_[8:].replace('//','/')
        return url_

    def url_metadata(self, key):
        url_ = self.base_url + '/' + self.apis[key] + '/' + self.metadata_api_label
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