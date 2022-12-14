'''Bla bla

'''
import pandas as pd
from dataclasses import dataclass

@dataclass
class USPTOReturnDataBasic:
    root : list[str]
    call_meta : list[str]

uspto_return_data_basic = USPTOReturnDataBasic(
    root = ['response', 'docs'],
    call_meta = ['responseHeader']
)

class ConsumerFormatError(Exception):
    pass

class ConsumerUSPTOReturnData(object):
    '''Bla bla

    '''
    def __init__(self, keys2read=None):
        self.keys2read = keys2read
        if self.keys2read is None:
            self.to_read_ = lambda x: True
        else:
            self.to_read_ = lambda x: x in self.keys2read

        self.container = pd.DataFrame()

    def _remove_lists(self):
        '''In the event that the return data from the Web API is one-element lists, then take only the
        first element value. This unfortunately is needed because the office action API has different convention
        than the enriched citation API.

        Raises:
            ConsumerFormatError: if a list was returned with more than one value; this should not happen with
                standard return values from the Web API

        '''
        def _pop_first(x):
            if isinstance(x, list):
                if len(x) == 1:
                    return x[0]
                else:
                    raise ConsumerFormatError('Multi-valued list obtained. Should not happen! Inspect raw data from Web API')
            else:
                return x
        self.container = self.container.applymap(_pop_first)

    def _process(self, payload, read_header=False):
        '''Bla bla

        '''
        def nested_retrieve(payload_dict, navigator):
            d = payload_dict[navigator[0]]
            if len(navigator) == 1:
                return d
            else:
                return nested_retrieve(d, navigator[1:])

        if read_header:
            payload_data = nested_retrieve(payload, uspto_return_data_basic.call_meta)
        else:
            payload_data = nested_retrieve(payload, uspto_return_data_basic.root)

        return [
            dict((key, value) for key, value in payload_data_slice.items()
                if self.to_read_(key))
            for payload_data_slice in payload_data
        ]

    def process(self, payload, read_header=False):
        return pd.DataFrame(self._process(payload, read_header=read_header))

    def append(self, payload, read_header=False):
        self.container = pd.concat([self.container, self.process(payload, read_header=read_header)])

    def dump_to_(self, fp, mode='a'):
        self.container.to_csv(path_or_buf=fp, mode=mode)
        self.reset()

    def reset(self):
        self.container = pd.DataFrame()
