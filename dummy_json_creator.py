import json

consumer_consts = {
    'enriched citations' : {
        'keys' : ['id',
                  'citedDocumentIdentifier',
                  'inventorNameText',
                  'officeActionCategory',
                  'officeActionDate',
                  'patentApplicationNumber',
                  'qualitySummaryText'],
        'descriptions' : {
            'id' : 'unique identifier for the citation; not unique to the cited text',
            'citedDocumentIdentifier' : 'bla bla'
        }
    },
    'office actions text' : {
        'keys' : ['id',
                  'patentApplicationNumber'],
        'descriptions': {
            'id' : 'bla',
            'patentApplicationNumber' : 'bla'
        }
    }
}

json.dump(consumer_consts, open('test.json','w'), indent=2)