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
    if isinstance(patent_metas, PatentMeta):
        pdata = [patent_metas]
    else:
        pdata = patent_metas
    return json.dumps([asdict(p) for p in pdata], indent=indent)

def get_patentmeta_from_(fp):
    raise NotImplementedError('Have not checked how to get data from json properly')
    data = json.load(fp)
    patent_metas = []
    for x in data:
        patent_metas.append(PatentMeta(**x))

    return patent_metas



