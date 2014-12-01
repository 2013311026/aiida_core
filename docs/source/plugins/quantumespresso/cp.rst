CP
++

Description
-----------
Use the plugin to support inputs of Quantum Espresso pw.x executable.

Supported codes
---------------
* tested from pw.x v5.0 onwards. Back compatibility is not guaranteed (although
  versions 4.3x might work most of the times).

Inputs
------
* **pseudo**, class :py:class:`UpfData <aiida.orm.data.upf.UpfData>`
  One pseudopotential file per atomic species.
  
  Alternatively, pseudo for every atomic species can be set with the **use_pseudos_from_family**
  method, if a family of pseudopotentials has been installed..
  
* **parameters**, class :py:class:`ParameterData <aiida.orm.data.parameter.ParameterData>`
  Input parameters of cp.x, as a nested dictionary, mapping the input of QE.
  Example::
    
      {"ELECTRONS":{"ecutwfc":"30","ecutrho":"100"},
      }
  
  See the QE documentation for the full list of variables and their meaning. 
  Note: some keywords don't have to be specified or Calculation will enter 
  the SUBMISSIONFAILED state, and are already taken care of by AiiDA (are related 
  with the structure or with path to files)::
    
      'CONTROL', 'pseudo_dir': pseudopotential directory
      'CONTROL', 'outdir': scratch directory
      'CONTROL', 'prefix': file prefix
      'SYSTEM', 'ibrav': cell shape
      'SYSTEM', 'celldm': cell dm
      'SYSTEM', 'nat': number of atoms
      'SYSTEM', 'ntyp': number of species
      'SYSTEM', 'a': cell parameters
      'SYSTEM', 'b': cell parameters
      'SYSTEM', 'c': cell parameters
      'SYSTEM', 'cosab': cell parameters
      'SYSTEM', 'cosac': cell parameters
      'SYSTEM', 'cosbc': cell parameters
     
* **structure**, class :py:class:`StructureData <aiida.orm.data.structure.StructureData>`
  The initial ionic configuration of the CP molecular dynamics.
* **settings**, class :py:class:`ParameterData <aiida.orm.data.parameter.ParameterData>` (optional)
  An optional dictionary that activates non-default operations. Possible values are:
    
    *  **'FIXED_COORDS'**: a list Nx3 booleans, with N the number of atoms. If True,
       the atomic position is fixed (in relaxations/md).
    *  **'NAMELISTS'**: list of strings. Specify all the list of Namelists to be 
       printed in the input file.
    *  **'PARENT_FOLDER_SYMLINK'**: boolean # If True, create a symlnk to the scratch 
       of the parent folder, otherwise the folder is copied (default: False)
    *  **'CMDLINE'**: list of strings. parameters to be put after the executable and before the input file. 
       Example: ["-npool","4"] will produce `pw.x -npool 4 < aiida.in`
    *  **'ADDITIONAL_RETRIEVE_LIST'**: list of strings. Specify additional files to be retrieved.
       By default, the output file and the xml file are already retrieved. 
    *  **'ALSO_BANDS'**: boolean. If True, retrieves the band structure (default: False)
    
* **parent_folder**, class :py:class:`RemoteData <aiida.orm.data.parameter.ParameterData>` (optional)
  If specified, the scratch folder coming from a previous QE calculation is 
  copied in the scratch of the new calculation.
  
Outputs
-------
There are several output nodes that can be created by the plugin, according to the calculation details.
All output nodes can be accessed with the ``calculation.out`` method.

* output_parameters :py:class:`ParameterData <aiida.orm.data.parameter.ParameterData>` 
  (accessed by ``calculation.res``)
  Contains the scalar properties. Example: energies (in eV) of the last configuration, 
  wall_time,
  warnings (possible error messages generated in the run).
* output_trajectory_array :py:class:`TrajectoryData <aiida.orm.data.array.trajectory.TrajectoryData>`
  Contains vectorial properties, too big to be put in the dictionary, like
  energies, positions, velocities, cells, at every saved step.  
* output_structure :py:class:`StructureData <aiida.orm.data.structure.StructureData>`
  Structure of the last step.

Errors
------
Errors of the parsing are reported in the log of the calculation (accessible 
with the ``verdi calculation logshow`` command). 
Moreover, they are stored in the ParameterData under the key ``warnings``, and are
accessible with ``Calculation.res.warnings``.
