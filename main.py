'''Main

'''
from api_uspto import retrieve_metadata_for_, retrieve_records_for_
from api_uspto_reader import USPTOAPIReader
from consumers import ConsumerUSPTOReturnData
from patent_seed_data import patent_seed_data_clothing

consumer_citation = ConsumerUSPTOReturnData(
    keys2read=[
        'id',
        'citedDocumentIdentifier',
        'inventorNameText',
        'officeActionCategory',
        'officeActionDate',
        'patentApplicationNumber',
        'qualitySummaryText'
    ]
)
consumer_oa = ConsumerUSPTOReturnData(
    keys2read=[
        'id',
        'patentApplicationNumber',
        'applicationDeemedWithdrawnDate',
        'inventionSubjectMatterCategory',
        'inventionTitle',
        'sections.section103RejectionText',
        'sections.section112RejectionText',
        'sections.section102RejectionText',
        'bodyText'
    ]
)

r = retrieve_metadata_for_('enriched citation', verify=False)
print (r)

rc = retrieve_records_for_('enriched citation',
                          data={
                              'criteria' : 'patentApplicationNumber:{}'.format(patent_seed_data_clothing[0].application_id),
                              'start' : '0',
                              'rows': '100'
                          },
                          verify=False)
consumer_citation.append(rc)
consumer_citation._remove_lists()
consumer_citation.dump_to_('test.csv')
print (rc)

roa = retrieve_records_for_('office actions text',
                          data={
                              'criteria' : 'patentApplicationNumber:{}'.format(patent_seed_data_clothing[0].application_id),
                              'start' : '0',
                              'rows' : '100'
                          },
                          verify=False)
consumer_oa.append(roa)
consumer_oa._remove_lists()
print (roa)
print (consumer_oa.container)

uu = USPTOAPIReader(
    api_name='enriched citation',
    consumer_keys=[
        'id',
        'citedDocumentIdentifier',
        'inventorNameText',
        'officeActionCategory',
        'officeActionDate',
        'patentApplicationNumber',
        'qualitySummaryText'
    ]
)
uu.read_by_patent_application_number_(patent_seed_data_clothing[0].application_id)
print (uu.container)