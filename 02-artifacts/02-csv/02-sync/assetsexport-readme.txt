assetsexport.txt – README
=========================
Config file for CSV10-masterCsv2Assets.py

Location:  <BLUEPRINT_ROOT>/02-artifacts/02-csv/02-sync/assetsexport.txt
Optional:  If missing, all defaults apply (see below)

Format:
  KEY=VALUE   active directive
  # comment   inactive / documentation

-----------------------------------------------------------------------
DIRECTIVES
-----------------------------------------------------------------------

ID_STRATEGY=<value>
  How to handle elements with the same identifier across sourceModels.
  merge      First occurrence wins. SourceModel column lists all models
             comma-separated. Safe default, no data loss.
  last_wins  Last occurrence overwrites the first.
  prefix     objectKey becomes "<sourceModel>::<id>". Always unique,
             but creates separate Assets objects per model.
  Default:   merge

INCLUDE_RELATIONS=true
  Exports relations to assets_relations.csv.
  Default:   false (file not created)

INCLUDE_SOURCE_MODEL=true
  Adds a SourceModel column to all output CSVs.
  Default:   true

INCLUDE_SOURCEMODEL=<filename>
  Restricts export to one specific sourceModel.
  Repeatable - add one line per model to include multiple.
  Empty (directive absent) = all sourceModels are exported.
  Example:   INCLUDE_SOURCEMODEL=Architecture.xml

EXCLUDE_TYPE=<ArchiMateType>
  Excludes an ArchiMate type from all output CSVs.
  Repeatable - add one line per type.
  Example:   EXCLUDE_TYPE=Artifact

-----------------------------------------------------------------------
DEFAULTS (when assetsexport.txt is absent or directive is commented)
-----------------------------------------------------------------------
  ID_STRATEGY          merge
  INCLUDE_RELATIONS    false
  INCLUDE_SOURCE_MODEL true
  INCLUDE_SOURCEMODEL  (all)
  EXCLUDE_TYPE         (none)
