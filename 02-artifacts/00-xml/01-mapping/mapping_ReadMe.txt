# ==========================================================
# mapping.txt
# Declarative Mapping Rules for Master XML Merge
#
# This file defines WHICH objects from child models
# are merged into master.xml.
#
# IMPORTANT PRINCIPLES:
# ----------------------------------------------------------
# - If NO rule is defined -> EVERYTHING is merged
# - Rules act ONLY as filters
# - If an object matches a rule -> the COMPLETE object
#   (including all attributes, children and references)
#   is merged into master.xml
# - IDs are NEVER used as filter criteria
# - XML is the source of truth, not intermediate files
# ==========================================================


# ----------------------------------------------------------
# GENERAL SYNTAX
# ----------------------------------------------------------
#
# <source>[<model-filter>]-<entry-point>+<attribute-filters>
#
# Parts:
#   source            : archi | bpmn
#   model-filter      : optional, filename or wildcard pattern
#   entry-point       : XML element name (element, relationship,
#                       bpmn:serviceTask, ...)
#   attribute-filters : optional, AND-combined using "+"
#                       IMPORTANT: always use "+" as separator,
#                       never "-" (which is reserved for the
#                       source-to-entry-point boundary)
#
# Wildcards:
#   *        -> everything
#   *text*   -> contains "text"
#
# If a part is omitted, it is NOT restricted.
# ----------------------------------------------------------


# ==========================================================
# ARCHI / OEF MAPPINGS Achtive Mapping 
# ==========================================================


#Expamples:
# ----------------------------------------------------------
# 1) Merge EVERYTHING from all Archi models
# ----------------------------------------------------------
# - All models
# - All object types
# - All attributes
#
# Result:
#   Complete Archi OEF content is merged into master.xml
# ----------------------------------------------------------
#archi-*


# ----------------------------------------------------------
# 2) Merge ALL Archi elements from ALL models
# ----------------------------------------------------------
# - Entry point: <element>
# - No attribute filters
#
# Result:
#   Every <element> is merged including:
#     - identifier
#     - all <name> entries (all languages)
#     - all <properties>
#     - all referenced relationships, items, views, etc.
# ----------------------------------------------------------
#archi-element


# ----------------------------------------------------------
# 3) Merge ONLY SystemSoftware elements from ALL models
# ----------------------------------------------------------
# Filter:
#   - entry point: <element>
#   - xsi:type must be "SystemSoftware"
#
# NOTE: use "+" to separate entry-point from attribute filters
#
# Result:
#   Complete SystemSoftware elements are merged,
#   NOT only the filtered attributes.
# ----------------------------------------------------------
#archi-element+xsi:type="SystemSoftware"


# ----------------------------------------------------------
# 4) Merge SystemSoftware ONLY from specific models
# ----------------------------------------------------------
# Model filter:
#   - only model files containing "Architecture"
#
# Attribute filter:
#   - xsi:type = SystemSoftware
#
# Result:
#   SystemSoftware elements from matching models only.
# ----------------------------------------------------------
#archi[*Architecture*]-element+xsi:type="SystemSoftware"


# ----------------------------------------------------------
# 5) Merge SystemSoftware with German property "Sprache"
# ----------------------------------------------------------
# Filters (AND logic):
#   - xsi:type = SystemSoftware
#   - property value contains "Sprache"
#   - property value language is "de"
#
# IMPORTANT:
#   The filter decides IF the element is selected.
#   The merge always includes the COMPLETE element.
# ----------------------------------------------------------
archi-element+xsi:type="SystemSoftware"+value-xml:lang="de">Sprache<


# ==========================================================
# BPMN MAPPINGS
# ==========================================================


# ----------------------------------------------------------
# 6) Merge ALL BPMN service tasks
# ----------------------------------------------------------
# Entry point:
#   - bpmn:serviceTask (local name: serviceTask)
#
# Result:
#   Complete serviceTask elements including:
#     - documentation
#     - extensionElements
#     - zeebe mappings
#     - incoming / outgoing flows
# ----------------------------------------------------------
#bpmn-bpmn:serviceTask


# ----------------------------------------------------------
# 7) Merge ONLY BPMN service tasks with Trigger documentation
# ----------------------------------------------------------
# Filters:
#   - entry point: bpmn:serviceTask
#   - <bpmn:documentation> contains "Trigger:Ja"
#
# Result:
#   Full serviceTask subtree is merged.
# ----------------------------------------------------------
# bpmn-bpmn:serviceTask+bpmn:documentation>Trigger:Ja<


# ==========================================================
# NOTES
# ==========================================================
#
# - Filters NEVER limit what is merged, only WHAT is selected
# - Model = XML file, no separate model object required
# - Identifier is used internally to resolve references,
#   but NEVER as a filter
# - This file is intentionally declarative and readable
# - SEPARATOR RULES:
#   "-" separates: source[model-filter] FROM entry-point
#   "+" separates: entry-point FROM attribute-filters
#                  and attribute-filters FROM each other
#
# ==========================================================
