'''Main

'''
from api_uspto import retrieve_metadata_for_, retrieve_records_for_

r = retrieve_metadata_for_('enriched_citation', verify=False)
print (r)
r = retrieve_records_for_('enriched_citation',
                          data={'criteria' : 'patentApplicationNumber:15758327',
                                'start' : '0',
                                'rows': '100'},
                          verify=False)
print (r)
