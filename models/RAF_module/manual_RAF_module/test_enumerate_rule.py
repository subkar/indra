import sys
sys.path.append('../..')

from indra.trips import trips_api
from indra.pysb_assembler import PysbAssembler
from enumerate_rules import enumerate_rules

tp = trips_api.process_text(
    "BRAF binds BRAF. BRAF binds NRAS. BRAF binds Vemurafenib.")

pa = PysbAssembler()
pa.add_statements(tp.statements)
model = pa.make_model()
print len(model.rules), len(model.parameters)

rule1 = model.rules['BRAF_BRAF_bind']
rule2 = model.rules['BRAF_VEMURAFENIB_bind']

enumerate_rules(model, rule1)
print len(model.rules), len(model.parameters)

enumerate_rules(model, rule2)
print len(model.rules), len(model.parameters)

