'''Bla bla

'''
import json
from dataclasses import dataclass, field, asdict

@dataclass
class PatentMeta:
    application_id : str
    document_id : str = ''
    cpci_classifications : list = field(default_factory=lambda : [])
    title : str = ''

def get_json_str_for_(patent_metas, indent=2):
    return json.dumps([asdict(p) for p in patent_metas], indent=indent)

patent_seed_data_clothing = [
    PatentMeta(
        application_id="15942658",
        cpci_classifications=['C12Q1/002', 'A61B5/1477'],
        title='WEARABLE TECHNOLOGY WITH SENSORS INTEGRATED INTO CLOTHING FIBERS',
        document_id='US20180279930A1'
    ),
    PatentMeta(
        application_id="16737055",
        cpci_classifications=['H04W4/029'],
        title="Fabric, Connections And Functional Structures For Wearable Electronic Garments And Applications For The Same",
        document_id="US20200237031A1"
    )
]

