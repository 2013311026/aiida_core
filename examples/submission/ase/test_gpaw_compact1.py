# -*- coding: utf-8 -*-
__copyright__ = u"Copyright (c), 2014, École Polytechnique Fédérale de Lausanne (EPFL), Switzerland, Laboratory of Theory and Simulation of Materials (THEOS). All rights reserved."
__license__ = "Non-Commercial, End-User Software License Agreement, see LICENSE.txt file"
__version__ = "0.3.0"

import sys
import os
from aiida.common.exceptions import NotExistent

################################################################

ParameterData = DataFactory('parameter')
StructureData = DataFactory('structure')
KpointsData = DataFactory('array.kpoints')

# CUSTOMIZE HERE ############
submit_test = True
codename = 'gpaw-serial'
queue = None
settings = None
#############################

code = Code.get(codename)
    
alat = 4. # angstrom
cell = [[alat, 0., 0.,],
        [0., alat, 0.,],
        [0., 0., alat,],
        ]
    
# BaTiO3 cubic structure
s = StructureData(cell=cell)
s.append_atom(position=(0.,0.,0.),symbols=['Ba'])
s.append_atom(position=(alat/2.,alat/2.,alat/2.),symbols=['Ti'])
s.append_atom(position=(alat/2.,alat/2.,0.),symbols=['O'])
s.append_atom(position=(alat/2.,0.,alat/2.),symbols=['O'])
s.append_atom(position=(0.,alat/2.,alat/2.),symbols=['O'])

kpoints = KpointsData()
kpoints.set_kpoints_mesh([2,2,2])

parameters = ParameterData(
    dict={"calculator": {"name":"gpaw",
                         "args":{"mode":{"@function":"PW",
                                         "args":{"ecut":300}
                         }}},
          })

calc = code.new_calc()
calc.label = "Test Gpaw"
calc.description = "Test calculation with the Gpaw code"
calc.set_max_wallclock_seconds(30*60) # 30 min
calc.set_resources({"num_machines": 1,"num_mpiprocs_per_machine":1})
calc.set_withmpi(False)

calc.use_structure(s)
calc.use_parameters(parameters)
calc.use_kpoints(kpoints)

if queue is not None:
    calc.set_queue_name(queue)

if submit_test:
    subfolder, script_filename = calc.submit_test()
    print "Test_submit for calculation (uuid='{}')".format(
        calc.uuid)
    print "Submit file in {}".format(os.path.join(
            os.path.relpath(subfolder.abspath),
            script_filename
            ))
else:
    calc.store_all()
    print "created calculation; calc=Calculation(uuid='{}') # ID={}".format(
        calc.uuid,calc.dbnode.pk)
    calc.submit()
    print "submitted calculation; calc=Calculation(uuid='{}') # ID={}".format(
        calc.uuid,calc.dbnode.pk)

