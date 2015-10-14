TCOD database exporter
----------------------

TCOD database exporter is used to export computation results of
:py:class:`StructureData <aiida.orm.data.structure.StructureData>`,
:py:class:`CifData <aiida.orm.data.cif.CifData>` and
:py:class:`TrajectoryData <aiida.orm.data.array.trajectory.TrajectoryData>`
(or any other data type, which can be converted to them) to the
`Theoretical Crystallography Open Database`_ (TCOD).

Setup
+++++

To be able to export data to TCOD, one has to
:ref:`install dependencies for CIF manipulation <CIF_manipulation_dependencies>`
as well as :ref:`cod-tools package <codtools_installation>`, and set up an
AiiDA :py:class:`Code <aiida.orm.code.Code>` for *cif_cod_deposit* script
from **cod-tools**.

How to deposit a structure
++++++++++++++++++++++++++

Best way to deposit data is to use the command line interface::

    verdi DATATYPE structure deposit tcod [--type {published,prepublication,personal}]
                                          [--username USERNAME] [--password]
                                          [--user-email USER_EMAIL] [--title TITLE]
                                          [--author-name AUTHOR_NAME]
                                          [--author-email AUTHOR_EMAIL] [--url URL]
                                          [--code CODE_LABEL]
                                          [--computer COMPUTER_NAME]
                                          [--replace REPLACE] [-m MESSAGE]
                                          [--reduce-symmetry] [--no-reduce-symmetry]
                                          [--parameter-data PARAMETER_DATA]
                                          [--dump-aiida-database]
                                          [--no-dump-aiida-database]
                                          [--exclude-external-contents]
                                          [--no-exclude-external-contents] [--gzip]
                                          [--no-gzip]
                                          [--gzip-threshold GZIP_THRESHOLD]
                                          PK

Where:

* ``DATATYPE`` -- one of AiiDA structural data types (at the moment of
  writing, they were
  :py:class:`StructureData <aiida.orm.data.structure.StructureData>`,
  :py:class:`CifData <aiida.orm.data.cif.CifData>` and
  :py:class:`TrajectoryData <aiida.orm.data.array.trajectory.TrajectoryData>`);
* ``TITLE`` -- the title of the publication, where the exported data
  is/will be published; in case of personal communication, the title
  should be chosen so as to reflect the exported dataset the best;
* ``CODE_LABEL`` -- label of AiiDA :py:class:`Code <aiida.orm.code.Code>`,
  associated with *cif_cod_deposit*;
* ``COMPUTER_NAME`` -- name of AiiDA
  :py:class:`Computer <aiida.orm.computer.Computer>`, where
  *cif_cod_deposit* script is to be launched;
* ``REPLACE`` -- `TCOD ID`_ of the replaced entry in the event of
  redeposition;
* ``MESSAGE`` -- string to describe changes for redeposited structures;
* ``--reduce-symmetry``, ``--no-reduce-symmetry`` -- turn on/off symmetry
  reduction of the exported structure (on by default);
* ``--parameter-data`` -- specify the PK of
  :py:class:`ParameterData <aiida.orm.data.parameter.ParameterData>`
  object, describing the result of the final (or single) calculation step
  of the workflow;
* ``--dump-aiida-database``, ``--no-dump-aiida-database`` -- turn on/off
  addition of relevant AiiDA database dump (on by default).

  .. warning:: be aware that TCOD is an **open** database, thus **no
    copyright-protected data should be deposited** unless permission is
    given by the owner of the rights.

  .. note:: data, which is deposited as pre-publication material, **will
    be kept private on TCOD server** and will not be disclosed to anyone
    without depositor's permission.

* ``--exclude-external-contents``, ``--no-exclude-external-contents`` --
  exclude contents of initial input files, that contain
  :py:class:`source <aiida.orm.data.Data.source>` property with
  definitions on how to obtain the contents from external resources (on
  by default);
* ``--gzip``, `--no-gzip`` -- turn on/off gzip compression for large
  files (off by default); ``--gzip-threshold`` sets the minimum file size
  to be compressed.

.. _Theoretical Crystallography Open Database: http://www.crystallography.net/tcod/
.. _TCOD deposition type: http://wiki.crystallography.net/deposition_type/
.. _TCOD ID: http://wiki.crystallography.net/tcod_id/
