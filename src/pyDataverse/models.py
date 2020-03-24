# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Dataverse data-types data model."""
from __future__ import absolute_import
from pyDataverse.utils import dict_to_json
from pyDataverse.utils import read_json
from pyDataverse.utils import write_json

"""
Data-structure to work with data and metadata of Dataverses, Datasets and
Datafiles - coming from different sources.
"""


class Dataverse(object):
    """Base class for Dataverse data model."""

    """Attributes to be imported from `dv_up` file."""
    __attr_import_dv_up_values = [
        'affiliation',
        'alias',
        'dataverseContacts',
        'dataverseType',
        'description',
        'name'
    ]

    """Required attributes for valid `dv_up` metadata dict creation."""
    __attr_dict_dv_up_required = [
        'alias',
        'dataverseContacts',
        'name'
    ]

    """Valid attributes for `dv_up` metadata dict creation."""
    __attr_dict_dv_up_valid = __attr_import_dv_up_values

    """Valid attributes for `all` metadata dict creation."""
    __attr_dict_all_valid = [
        'pid'
    ] + __attr_dict_dv_up_valid

    def __init__(self):
        """Init :class:`Dataverse()`.

        Examples
        -------
        Create a Dataverse::

            >>> from pyDataverse.models import Dataverse
            >>> dv = Dataverse()

        """

    def __str__(self):
        """Return name of class :class:`Dataverse()` for users."""
        return 'pyDataverse Dataverse() model class.'

    def set(self, data):
        """Set class attributes with a flat :class:`dict`.

        Parameters
        ----------
        data : dict
            Flat :class:`dict` with data. All keys will be mapped to a similar
            called attribute with it's value.


        Examples
        -------
        Set Dataverse attributes via flat :class:`dict`::

            >>> from pyDataverse.models import Dataverse
            >>> dv = Dataverse()
            >>> data = {
            >>>     'dataverseContacts': [
            >>>         {'contactEmail': 'test@example.com'}
            >>>     ],
            >>>     'name': 'Test pyDataverse',
            >>>     'alias': 'test-pyDataverse'
            >>> }
            >>> dv.set(data)
            >>> dv.contactEmail
            ['test@example.com']

        """
        for key, val in data.items():
            self.__setattr__(key, val)

    def import_data(self, filename, format='dv_up'):
        """Import Dataverse API Upload JSON metadata from JSON file.

        Parses in data stored in the Dataverse API Dataverse JSON standard.

        Parameters
        ----------
        filename : string
            Filename with full path.
        format : string
            Data format for input data formats. Available format so far are:
            ``dv_up``: Dataverse API Upload Dataverse JSON metadata standard.
            ``all``: All attributes.

        Examples
        -------
        Import metadata coming from JSON file::

            >>> from pyDataverse.models import Dataverse
            >>> dv = Dataverse()
            >>> dv.import_data('tests/data/dataverse_full.json')
            >>> dv.name
            'Test pyDataverse'

        """
        data = {}
        if format == 'dv_up':
            metadata = read_json(filename)
            # get first level metadata and parse it automatically
            for key, val in metadata.items():
                if key in self.__attr_import_dv_up_values:
                    data[key] = metadata[key]
                else:
                    print('Attribute {0} not valid for import (dv_up).'.format(key))
            self.set(data)
        else:
            # TODO: Exception
            print('Data-format not right.')

    def is_valid(self):
        """Check if all attributes required for Dataverse metadata are set.

        Check if all attributes are set necessary for the Dataverse API Upload
        JSON metadata standard of a Dataverse.

        Returns
        -------
        bool
            ``True``, if creation of Dataverse API Upload JSON metadata is
            possible. ``False``, if not.

        Examples
        -------
        Check if metadata is valid for Dataverse API Upload JSON metadata creation::

            >>> from pyDataverse.models import Dataverse
            >>> dv = Dataverse()
            >>> data = {
            >>>     'dataverseContacts': [
            >>>         {'contactEmail': 'test@example.com'}
            >>>     ],
            >>>     'name': 'Test pyDataverse',
            >>>     'alias': 'test-pyDataverse'
            >>> }
            >>> dv.set(data)
            >>> dv.is_valid()
            True
            >>> dv.name = None
            >>> dv.is_valid()
            False

        """
        is_valid = True
        for attr in self.__attr_dict_dv_up_required:
            if attr in list(self.__dict__.keys()):
                if not self.__getattribute__(attr):
                    is_valid = False
                    print('Attribute \'{0}\' is `False`.'.format(attr))
            else:
                is_valid = False
                print('Attribute \'{0}\' missing.'.format(attr))
        return is_valid

    def dict(self, format='dv_up'):
        """Create different data outputs as :class:`dict`.

        Creates different data outputs - different in structure and content -
        of the objects data.

        Parameters
        ----------
        format : string
            Data format for :class:`dict` creation. Available format so far are:
            ``dv_up``: Dataverse API Upload Dataverse JSON metadata standard.
            ``all``: All attributes.

        Returns
        -------
        dict
            Data as :class:`dict` with expected structure and content.

        Examples
        -------
        Get dict of Dataverse metadata::

            >>> from pyDataverse.models import Dataverse
            >>> dv = Dataverse()
            >>> data = {
            >>>     'dataverseContacts': [
            >>>         {'contactEmail': 'test@example.com'}
            >>>     ],
            >>>     'name': 'Test pyDataverse',
            >>>     'alias': 'test-pyDataverse'
            >>> }
            >>> dv.set(data)
            >>> data = dv.dict()
            >>> data['name']
            'Test pyDataverse'

        Todo
        -------
        Validate standards.

        """
        data = {}
        if format == 'dv_up':
            if self.is_valid():
                for attr in self.__attr_dict_dv_up_valid:
                    # check if attribute exists
                    if attr in list(self.__dict__.keys()):
                        # check if attribute is not None
                        if self.__getattribute__(attr) is not None:
                            data[attr] = self.__getattribute__(attr)
                return data
            else:
                print('Dict can not be created. Data is not valid for format.')
                return None
        elif format == 'all':
            for attr in self.__attr_dict_all_valid:
                if attr in list(self.__dict__.keys()):
                    if self.__getattribute__(attr) is not None:
                        data[attr] = self.__getattribute__(attr)
            return data
        else:
            # TODO: Exception
            print('Format not right for dict.')
            return None

    def json(self, format='dv_up'):
        r"""Create JSON output of different data formats.

        Parameters
        ----------
        format : string
            Data format for JSON creation. Available format so far are:
            ``dv_up``: Dataverse API Upload Dataverse JSON metadata standard.
            ``all``: All attributes.

        Returns
        -------
        string
            JSON formatted :class:`str` of Dataverse metadata for API upload.

        Examples
        -------
        Get :class:`dict` of Dataverse metadata::

            >>> from pyDataverse.models import Dataverse
            >>> dv = Dataverse()
            >>> data = {
            >>>     'dataverseContacts': [
            >>>         {'contactEmail': 'test@example.com'}
            >>>     ],
            >>>     'name': 'Test pyDataverse',
            >>>     'alias': 'test-pyDataverse'
            >>> }
            >>> dv.set(data)
            >>> data = dv.json()
            >>> data
            '{\n  "name": "Test pyDataverse",\n  "dataverseContacts": [\n    {\n      "contactEmail": "test@example.com"\n    }\n  ],\n  "alias": "test-pyDataverse"\n}'

        Todo
        -------
        Validate standards.

        """
        if format == 'dv_up' or format == 'all':
            data = self.dict(format=format)
            if data:
                return dict_to_json(data)
            else:
                return None
                # TODO Exception
                print('JSON data can not be read in.')
        else:
            # TODO Exception
            print('Data format not valid.')

    def export_data(self, filename, format='dv_up'):
        """Export Dataverse metadata to different formats.

        Parameters
        ----------
        filename : string
            Filename with full path.
        format : string
            Data format for export. Available format so far are:
            ``dv_up``: Dataverse API Upload Dataverse JSON metadata standard.
            ``all``: All attributes.

        Examples
        -------
        Export Dataverse metadata::

            >>> from pyDataverse.models import Dataverse
            >>> dv = Dataverse()
            >>> data = {
            >>>     'dataverseContacts': [
            >>>         {'contactEmail': 'test@example.com'}
            >>>     ],
            >>>     'name': 'Test pyDataverse',
            >>>     'alias': 'test-pyDataverse'
            >>> }
            >>> dv.set(data)
            >>> dv.export_data('dataverse_export.json')

        """
        if format == 'dv_up' or format == 'all':
            return write_json(filename, self.dict(format=format))
        else:
            # TODO: Exception
            print('Data-format not right.')


class Dataset(object):
    """Base class for the Dataset data model."""

    """
    Dataverse API Upload Dataset JSON attributes inside
    ds[\'datasetVersion\'].
    """
    __attr_import_dv_up_datasetVersion_values = [
        'license',
        'termsOfAccess',
        'termsOfUse'
    ]

    """
    Dataverse API Upload Dataset JSON attributes inside
    ds[\'datasetVersion\'][\'metadataBlocks\'][\'citation\'][\'fields\'].
    """
    __attr_import_dv_up_citation_fields_values = [
        'accessToSources',
        'alternativeTitle',
        'alternativeURL',
        'characteristicOfSources',
        'dateOfDeposit',
        'dataSources',
        'depositor',
        'distributionDate',
        'kindOfData',
        'language',
        'notesText',
        'originOfSources',
        'otherReferences',
        'productionDate',
        'productionPlace',
        'relatedDatasets',
        'relatedMaterial',
        'subject',
        'subtitle',
        'title'
    ]

    """
    Dataverse API Upload Dataset JSON attributes inside
    [\'datasetVersion\'][\'metadataBlocks\'][\'citation\'][\'fields\'].
    """
    __attr_import_dv_up_citation_fields_arrays = {
        'author': ['authorName', 'authorAffiliation', 'authorIdentifierScheme',
                   'authorIdentifier'],
        'contributor': ['contributorType', 'contributorName'],
        'dateOfCollection': ['dateOfCollectionStart', 'dateOfCollectionEnd'],
        'datasetContact': ['datasetContactName', 'datasetContactAffiliation',
                           'datasetContactEmail'],
        'distributor': ['distributorName', 'distributorAffiliation',
                        'distributorAbbreviation', 'distributorURL',
                        'distributorLogoURL'],
        'dsDescription': ['dsDescriptionValue', 'dsDescriptionDate'],
        'grantNumber': ['grantNumberAgency', 'grantNumberValue'],
        'keyword': ['keywordValue', 'keywordVocabulary',
                    'keywordVocabularyURI'],
        'producer': ['producerName', 'producerAffiliation',
                     'producerAbbreviation', 'producerURL', 'producerLogoURL'],
        'otherId': ['otherIdAgency', 'otherIdValue'],
        'publication': ['publicationCitation', 'publicationIDType',
                        'publicationIDNumber', 'publicationURL'],
        'software': ['softwareName', 'softwareVersion'],
        'timePeriodCovered': ['timePeriodCoveredStart',
                              'timePeriodCoveredEnd'],
        'topicClassification': ['topicClassValue', 'topicClassVocab']
    }

    """
    Attributes of Dataverse API Upload Dataset JSON metadata standard inside
    [\'datasetVersion\'][\'metadataBlocks\'][\'geospatial\'][\'fields\'].
    """
    __attr_import_dv_up_geospatial_fields_values = [
        'geographicUnit'
    ]

    """
    Attributes of Dataverse API Upload Dataset JSON metadata standard inside
    [\'datasetVersion\'][\'metadataBlocks\'][\'geospatial\'][\'fields\'].
    """
    __attr_import_dv_up_geospatial_fields_arrays = {
        'geographicBoundingBox': ['westLongitude', 'eastLongitude',
                                  'northLongitude', 'southLongitude'],
        'geographicCoverage': ['country', 'state', 'city',
                               'otherGeographicCoverage']
    }

    """
    Attributes of Dataverse API Upload Dataset JSON metadata standard inside
    [\'datasetVersion\'][\'metadataBlocks\'][\'socialscience\'][\'fields\'].
    """
    __attr_import_dv_up_socialscience_fields_values = [
        'actionsToMinimizeLoss',
        'cleaningOperations',
        'collectionMode',
        'collectorTraining',
        'controlOperations',
        'dataCollectionSituation',
        'dataCollector',
        'datasetLevelErrorNotes',
        'deviationsFromSampleDesign',
        'frequencyOfDataCollection',
        'otherDataAppraisal',
        'researchInstrument',
        'responseRate',
        'samplingErrorEstimates',
        'samplingProcedure',
        'unitOfAnalysis',
        'universe',
        'timeMethod',
        'weighting'
    ]

    """
    Attributes of Dataverse API Upload Dataset JSON metadata standard inside
    [\'datasetVersion\'][\'metadataBlocks\'][\'journal\'][\'fields\'].
    """
    __attr_import_dv_up_journal_fields_values = [
        'journalArticleType'
    ]

    """
    Attributes of Dataverse API Upload Dataset JSON metadata standard inside
    [\'datasetVersion\'][\'metadataBlocks\'][\'journal\'][\'fields\'].
    """
    __attr_import_dv_up_journal_fields_arrays = {
        'journalVolumeIssue': ['journalVolume', 'journalIssue',
                               'journalPubDate']
    }

    """Required attributes for valid `dv_up` metadata dict creation."""
    __attr_dict_dv_up_required = [
        'author',
        'datasetContact',
        'dsDescription',
        'subject',
        'title'
    ]

    """typeClass primitive."""
    __attr_dict_dv_up_typeClass_primitive = [
        'accessToSources',
        'alternativeTitle',
        'alternativeURL',
        'authorAffiliation',
        'authorIdentifier',
        'authorName',
        'characteristicOfSources',
        'city',
        'contributorName',
        'dateOfDeposit',
        'dataSources',
        'depositor',
        'distributionDate',
        'kindOfData',
        'notesText',
        'originOfSources',
        'otherGeographicCoverage',
        'otherReferences',
        'productionDate',
        'productionPlace',
        'publicationCitation',
        'publicationIDNumber',
        'publicationURL',
        'relatedDatasets',
        'relatedMaterial',
        'seriesInformation',
        'seriesName',
        'state',
        'subtitle',
        'title'
    ] + __attr_import_dv_up_citation_fields_arrays['dateOfCollection'] \
    + __attr_import_dv_up_citation_fields_arrays['datasetContact'] \
    + __attr_import_dv_up_citation_fields_arrays['distributor'] \
    + __attr_import_dv_up_citation_fields_arrays['dsDescription'] \
    + __attr_import_dv_up_citation_fields_arrays['grantNumber'] \
    + __attr_import_dv_up_citation_fields_arrays['keyword'] \
    + __attr_import_dv_up_citation_fields_arrays['producer'] \
    + __attr_import_dv_up_citation_fields_arrays['otherId'] \
    + __attr_import_dv_up_citation_fields_arrays['software'] \
    + __attr_import_dv_up_citation_fields_arrays['timePeriodCovered'] \
    + __attr_import_dv_up_citation_fields_arrays['topicClassification'] \
    + __attr_import_dv_up_geospatial_fields_values \
    + __attr_import_dv_up_geospatial_fields_arrays['geographicBoundingBox'] \
    + __attr_import_dv_up_socialscience_fields_values \
    + __attr_import_dv_up_journal_fields_arrays['journalVolumeIssue']
    + ['socialScienceNotesType', 'socialScienceNotesSubject', 'socialScienceNotesText'] \
    + ['targetSampleActualSize', 'targetSampleSizeFormula'] \

    """typeClass compound."""
    __attr_dict_dv_up_typeClass_compound = [
    ] + list(__attr_import_dv_up_citation_fields_arrays.keys()) \
    + list(__attr_import_dv_up_geospatial_fields_arrays.keys()) \
    + list(__attr_import_dv_up_journal_fields_arrays.keys()) \
    + ['series', 'socialScienceNotes', 'targetSampleSize']

    """typeClass controlledVocabulary."""
    __attr_dict_dv_up_typeClass_controlledVocabulary = [
        'authorIdentifierScheme',
        'contributorType',
        'country',
        'journalArticleType',
        'language',
        'publicationIDType',
        'subject',
    ]

    __attr_dict_dv_up_multiple = [
    ]

    """
    This attributes are excluded from automatic parsing in ds.dict() creation.
    """
    __attr_dict_dv_up_single_dict = [
        'series',
        'socialScienceNotes',
        'targetSampleSize'
    ]

    """Attributes of displayName."""
    __attr_displayNames = [
        'citation_displayName',
        'geospatial_displayName',
        'socialscience_displayName',
        'journal_displayName'
    ]

    def __init__(self):
        """Init a Dataset() class.

        Examples
        -------
        Create a Dataverse::

            >>> from pyDataverse.models import Dataset
            >>> ds = Dataset()

        """

    def __str__(self):
        """Return name of Dataset() class for users."""
        return 'pyDataverse Dataset() model class.'

    def set(self, data):
        """Set class attributes with a flat :class:`dict`.

        Parameters
        ----------
            Flat :class:`dict` with data. All keys will be mapped to a similar
            called attribute with it's value.

        Examples
        -------
        Set Dataset attributes via flat :class:`dict`::

            >>> from pyDataverse.models import Dataset
            >>> ds = Dataset()
            >>> data = {
            >>>     'title': 'pyDataverse study 2019',
            >>>     'dsDescription': [
            >>>         {'dsDescriptionValue': 'New study about pyDataverse usage in 2019'}
            >>>     ]
            >>> }
            >>> ds.set(data)
            >>> ds.title
            'pyDataverse study 2019'

        """
        for key, val in data.items():
            self.__setattr__(key, val)

    def import_data(self, filename, format='dv_up'):
        """Import Dataset API Upload JSON metadata from JSON file.

        Parses in data stored in the Dataverse API Dataset JSON standard.

        Parameters
        ----------
        filename : string
            Filename with full path.
        format : string
            Data format of input data, coming from file. Available format so
            far are: ``dv_up`` for the Dataverse API Upload Dataset JSON
            metadata standard.

        Examples
        -------
        Set Dataverse attributes via flat :class:`dict`::

            >>> from pyDataverse.models import Dataset
            >>> ds = Dataset()
            >>> ds.import_data('tests/data/dataset_full.json')
            >>> ds.title
            'Replication Data for: Title'

        """
        data = {}
        if format == 'dv_up':
            metadata = read_json(filename)
            """dataset"""
            # get first level metadata and parse it automatically
            for key, val in metadata['datasetVersion'].items():
                if not key == 'metadataBlocks':
                    if key in self.__attr_import_dv_up_datasetVersion_values:
                        data[key] = val
                    else:
                        print('Attribute {0} not valid for import (dv_up).'.format(key))

            if 'metadataBlocks' in metadata['datasetVersion']:

                """citation"""
                if 'citation' in metadata['datasetVersion']['metadataBlocks']:
                    citation = metadata['datasetVersion']['metadataBlocks']['citation']
                    if 'displayName' in citation:
                        data['citation_displayName'] = citation['displayName']

                    for field in citation['fields']:
                        if field['typeName'] in self.__attr_import_dv_up_citation_fields_values:
                            data[field['typeName']] = field['value']
                        elif field['typeName'] in self.__attr_import_dv_up_citation_fields_arrays:
                            data[field['typeName']] = self.__parse_field_array(
                                field['value'],
                                self.__attr_import_dv_up_citation_fields_arrays[field['typeName']])
                        elif field['typeName'] == 'series':
                            data['series'] = {}
                            if 'seriesName' in field['value']:
                                data['series']['seriesName'] = field['value']['seriesName']['value']
                            if 'seriesInformation' in field['value']:
                                data['series']['seriesInformation'] = field['value']['seriesInformation']['value']
                        else:
                            print('Attribute {0} not valid for import (dv_up).'.format(field['typeName']))
                else:
                    # TODO: Exception
                    print('Citation not in JSON')

                """geospatial"""
                if 'geospatial' in metadata['datasetVersion']['metadataBlocks']:
                    geospatial = metadata['datasetVersion']['metadataBlocks']['geospatial']
                    if 'displayName' in geospatial:
                        self.__setattr__('geospatial_displayName',
                                         geospatial['displayName'])

                    for field in geospatial['fields']:
                        if field['typeName'] in self.__attr_import_dv_up_geospatial_fields_values:
                            data[field['typeName']] = field['value']
                        elif field['typeName'] in self.__attr_import_dv_up_geospatial_fields_arrays:
                            data[field['typeName']] = self.__parse_field_array(
                                field['value'],
                                self.__attr_import_dv_up_geospatial_fields_arrays[field['typeName']])
                        else:
                            print('Attribute {0} not valid for import (dv_up).'.format(field['typeName']))
                else:
                    # TODO: Exception
                    print('geospatial not in JSON')

                """socialscience"""
                if 'socialscience' in metadata['datasetVersion']['metadataBlocks']:
                    socialscience = metadata['datasetVersion']['metadataBlocks']['socialscience']

                    if 'displayName' in socialscience:
                        self.__setattr__('socialscience_displayName',
                                         socialscience['displayName'])

                    for field in socialscience['fields']:
                        if field['typeName'] in self.__attr_import_dv_up_socialscience_fields_values:
                            data[field['typeName']] = field['value']
                        elif field['typeName'] == 'targetSampleSize':
                            data['targetSampleSize'] = {}
                            if 'targetSampleActualSize' in field['value']:
                                data['targetSampleSize']['targetSampleActualSize'] = field['value']['targetSampleActualSize']['value']
                            if 'targetSampleSizeFormula' in field['value']:
                                data['targetSampleSize']['targetSampleSizeFormula'] = field['value']['targetSampleSizeFormula']['value']
                        elif field['typeName'] == 'socialScienceNotes':
                            data['socialScienceNotes'] = {}
                            if 'socialScienceNotesType' in field['value']:
                                data['socialScienceNotes']['socialScienceNotesType'] = field['value']['socialScienceNotesType']['value']
                            if 'socialScienceNotesSubject' in field['value']:
                                data['socialScienceNotes']['socialScienceNotesSubject'] = field['value']['socialScienceNotesSubject']['value']
                            if 'socialScienceNotesText' in field['value']:
                                data['socialScienceNotes']['socialScienceNotesText'] = field['value']['socialScienceNotesText']['value']
                        else:
                            print('Attribute {0} not valid for import (dv_up).'.format(field['typeName']))
                else:
                    # TODO: Exception
                    print('socialscience not in JSON')

                """journal"""
                if 'journal' in metadata['datasetVersion']['metadataBlocks']:
                    journal = metadata['datasetVersion']['metadataBlocks']['journal']

                    if 'displayName' in journal:
                        self.__setattr__('journal_displayName',
                                         journal['displayName'])

                    for field in journal['fields']:
                        if field['typeName'] in self.__attr_import_dv_up_journal_fields_values:
                            data[field['typeName']] = field['value']
                        elif field['typeName'] in self.__attr_import_dv_up_journal_fields_arrays:
                            data[field['typeName']] = self.__parse_field_array(
                                field['value'],
                                self.__attr_import_dv_up_journal_fields_arrays[field['typeName']])
                        else:
                            print('Attribute {0} not valid for import (dv_up).'.format(field['typeName']))
                else:
                    # TODO: Exception
                    print('journal not in JSON')
            self.set(data)
        else:
            # TODO: Exception
            print('Data-format not right')

    def __parse_field_array(self, data, attr_list):
        """Parse out Dataverse API Upload Dataset JSON metadata arrays.

        Parameters
        ----------
        data : list
            List of dictionaries of a specific Dataverse API metadata field.
        attr_list : list
            List of attributes to be parsed.

        Returns
        -------
        list
            List of :class:`dict`s with parsed out key-value pairs.

        """
        data_tmp = []

        for d in data:
            tmp_dict = {}
            for key, val in d.items():
                if key in attr_list:
                    tmp_dict[key] = val['value']
                else:
                    print('Key \'{0}\' not in attribute list'.format(key))
            data_tmp.append(tmp_dict)

        return data_tmp

    def is_valid(self):
        """Check if all attributes required for Dataverse metadata are set.

        Check if all attributes are set necessary for the Dataverse API Upload
        JSON metadata standard of a Dataset.

        Returns
        -------
        bool
            ``True``, if creation of metadata JSON is possible. `False`, if
            not.

        Examples
        -------
        Check if metadata is valid for Dataverse API upload::

            >>> from pyDataverse.models import Dataset
            >>> ds = Dataset()
            >>> data = {
            >>>     'title': 'pyDataverse study 2019',
            >>>     'dsDescription': [
            >>>         {'dsDescriptionValue': 'New study about pyDataverse usage in 2019'}
            >>>     ]
            >>> }
            >>> ds.set(data)
            >>> ds.is_valid()
            False
            >>> ds.author = [{'authorName': 'LastAuthor1, FirstAuthor1'}]
            >>> ds.datasetContact = [{'datasetContactName': 'LastContact1, FirstContact1'}]
            >>> ds.subject = ['Engineering']
            >>> ds.is_valid()
            True

        Todo
        -------
        Test out required fields or ask Harvard.

        """
        is_valid = True

        # check if all required attributes are set
        for attr in self.__attr_dict_dv_up_required:
            if attr in list(self.__dict__.keys()):
                if not self.__getattribute__(attr):
                    is_valid = False
                    print('Attribute \'{0}\' is `False`.'.format(attr))
            else:
                is_valid = False
                print('Attribute \'{0}\' missing.'.format(attr))

        # check if attributes set are complete where necessary
        if 'timePeriodCovered' in list(self.__dict__.keys()):
            tp_cov = self.__getattribute__('timePeriodCovered')
            if tp_cov:
                for tp in tp_cov:
                    if 'timePeriodCoveredStart' in tp or 'timePeriodCoveredEnd' in tp:
                        if not ('timePeriodCoveredStart' in tp and 'timePeriodCoveredEnd' in tp):
                            is_valid = False
                            print('timePeriodCovered attribute missing.')

        if 'dateOfCollection' in list(self.__dict__.keys()):
            d_coll = self.__getattribute__('dateOfCollection')
            if d_coll:
                for d in d_coll:
                    if 'dateOfCollectionStart' in d or 'dateOfCollectionEnd' in d:
                        if not ('dateOfCollectionStart' in d and 'dateOfCollectionEnd' in d):
                            is_valid = False
                            print('dateOfCollection attribute missing.')

        if 'author' in list(self.__dict__.keys()):
            authors = self.__getattribute__('author')
            if authors:
                for a in authors:
                    if 'authorAffiliation' in a or 'authorIdentifierScheme' in a or 'authorIdentifier' in a:
                        if 'authorName' not in a:
                            is_valid = False
                            print('author attribute missing.')

        if 'datasetContact' in list(self.__dict__.keys()):
            ds_contac = self.__getattribute__('datasetContact')
            if ds_contac:
                for c in ds_contac:
                    if 'datasetContactAffiliation' in c or 'datasetContactEmail' in c:
                        if 'datasetContactName' not in c:
                            is_valid = False
                            print('datasetContact attribute missing.')

        if 'producer' in list(self.__dict__.keys()):
            producer = self.__getattribute__('producer')
            if producer:
                for p in producer:
                    if 'producerAffiliation' in p or 'producerAbbreviation' in p or 'producerURL' in p or 'producerLogoURL' in p:
                        if not p['producerName']:
                            is_valid = False
                            print('producer attribute missing.')

        if 'contributor' in list(self.__dict__.keys()):
            contributor = self.__getattribute__('contributor')
            if contributor:
                for c in contributor:
                    if 'contributorType' in c:
                        if 'contributorName' not in c:
                            is_valid = False
                            print('contributor attribute missing.')

        if 'distributor' in list(self.__dict__.keys()):
            distributor = self.__getattribute__('distributor')
            if distributor:
                for d in distributor:
                    if 'distributorAffiliation' in d or 'distributorAbbreviation' in d or 'distributorURL' in d or 'distributorLogoURL' in d:
                        if 'distributorName' not in d:
                            is_valid = False
                            print('distributor attribute missing.')

        if 'geographicBoundingBox' in list(self.__dict__.keys()):
            bbox = self.__getattribute__('geographicBoundingBox')
            if bbox:
                for b in bbox:
                    if b:
                        if not ('westLongitude' in b and 'eastLongitude' in b and 'northLongitude' in b and 'southLongitude' in b):
                            is_valid = False
                            print('geographicBoundingBox attribute missing.')

        return is_valid

    def dict(self, format='dv_up'):
        """Create class:`dict` in different data formats.

        Parameters
        ----------
        format : string
            Data format for :class:`dict` creation. Available format so far are:
            ``dv_up``: Dataverse API Upload Dataset JSON metadata standard.
            ``all``: All attributes.

        Returns
        -------
        dict
            Data as dict.

        Examples
        -------
        Get dict of Dataverse metadata::

            >>> from pyDataverse.models import Dataset
            >>> ds = Dataset()
            >>> data = {
            >>>     'title': 'pyDataverse study 2019',
            >>>     'dsDescription': [
            >>>         {'dsDescriptionValue': 'New study about pyDataverse usage in 2019'}
            >>>     ]
            >>> }
            >>> ds.set(data)
            >>> data = dv.dict()
            >>> data['title']
            'pyDataverse study 2019'

        Todo
        -------
        Validate standard

        """
        data = {}
        if format == 'dv_up':
            if self.is_valid():
                data['datasetVersion'] = {}
                data['datasetVersion']['metadataBlocks'] = {}
                citation = {}
                citation['fields'] = []

                """dataset"""
                # Generate first level attributes
                for attr in self.__attr_import_dv_up_datasetVersion_values:
                    if attr in list(self.__dict__.keys()):
                        if self.__getattribute__(attr) is not None:
                            data['datasetVersion'][attr] = self.__getattribute__(attr)

                """citation"""
                if 'citation_displayName' in list(self.__dict__.keys()):
                    citation['displayName'] = self.citation_displayName

                # Generate first level attributes
                for attr in self.__attr_import_dv_up_citation_fields_values:
                    if attr in list(self.__dict__.keys()):
                        if self.__getattribute__(attr) is not None:
                            v = self.__getattribute__(attr)
                            if isinstance(v, list):
                                multiple = True
                            else:
                                multiple = False
                            if attr in self.__attr_dict_dv_up_typeClass_primitive:
                                typeClass = 'primitive'
                            elif attr in self.__attr_dict_dv_up_typeClass_compound:
                                typeClass = 'compound'
                            elif attr in self.__attr_dict_dv_up_typeClass_controlledVocabulary:
                                typeClass = 'controlledVocabulary'
                            citation['fields'].append({
                                'typeName': attr,
                                'multiple': multiple,
                                'typeClass': typeClass,
                                'value': v
                            })

                # Generate fields attributes
                for key, val in self.__attr_import_dv_up_citation_fields_arrays.items():
                    if key in list(self.__dict__.keys()):
                        if self.__getattribute__(key) is not None:
                            v = self.__getattribute__(key)
                            citation['fields'].append({
                                'typeName': key,
                                'multiple': True,
                                'typeClass': 'compound',
                                'value': self.__generate_field_arrays(key, val)
                            })

                # Generate series attributes
                if 'series' in list(self.__dict__.keys()):
                    series = self.__getattribute__('series')
                    if series is not None:
                        tmp_dict = {}
                        if 'seriesName' in series:
                            if series['seriesName'] is not None:
                                tmp_dict['seriesName'] = {}
                                tmp_dict['seriesName']['typeName'] = 'seriesName'
                                tmp_dict['seriesName']['multiple'] = False
                                tmp_dict['seriesName']['typeClass'] = 'primitive'
                                tmp_dict['seriesName']['value'] = series['seriesName']
                        if 'seriesInformation' in series:
                            if series['seriesInformation'] is not None:
                                tmp_dict['seriesInformation'] = {}
                                tmp_dict['seriesInformation']['typeName'] = 'seriesInformation'
                                tmp_dict['seriesInformation']['multiple'] = False
                                tmp_dict['seriesInformation']['typeClass'] = 'primitive'
                                tmp_dict['seriesInformation']['value'] = series['seriesInformation']
                        citation['fields'].append({
                            'typeName': 'series',
                            'multiple': False,
                            'typeClass': 'compound',
                            'value': tmp_dict
                        })

                """geospatial"""
                for attr in self.__attr_import_dv_up_geospatial_fields_values + list(self.__attr_import_dv_up_geospatial_fields_arrays.keys()) + ['geospatial_displayName']:
                    if attr in list(self.__dict__.keys()):
                        geospatial = {}
                        if not attr == 'geospatial_displayName':
                            geospatial['fields'] = []

                if 'geospatial_displayName' in list(self.__dict__.keys()):
                    if 'geospatial' not in locals():
                        geospatial = {}
                    geospatial['displayName'] = self.geospatial_displayName

                # Generate first level attributes
                for attr in self.__attr_import_dv_up_geospatial_fields_values:
                    if attr in list(self.__dict__.keys()):
                        if self.__getattribute__(attr) is not None:
                            v = self.__getattribute__(attr)
                            if isinstance(v, list):
                                multiple = True
                            else:
                                multiple = False
                            if attr in self.__attr_dict_dv_up_typeClass_primitive:
                                typeClass = 'primitive'
                            elif attr in self.__attr_dict_dv_up_typeClass_compound:
                                typeClass = 'compound'
                            elif attr in self.__attr_dict_dv_up_typeClass_controlledVocabulary:
                                typeClass = 'controlledVocabulary'
                            geospatial['fields'].append({
                                'typeName': attr,
                                'multiple': multiple,
                                'typeClass': typeClass,
                                'value': v
                            })

                # Generate fields attributes
                for key, val in self.__attr_import_dv_up_geospatial_fields_arrays.items():
                    if key in list(self.__dict__.keys()):
                        if self.__getattribute__(key) is not None:
                            geospatial['fields'].append({
                                'typeName': key,
                                'multiple': True,
                                'typeClass': 'compound',
                                'value': self.__generate_field_arrays(key, val)
                            })

                """socialscience"""
                for attr in self.__attr_import_dv_up_socialscience_fields_values + ['socialscience_displayName']:
                    if attr in list(self.__dict__.keys()):
                        socialscience = {}
                        if not attr == 'socialscience_displayName':
                            socialscience['fields'] = []

                if 'socialscience_displayName' in list(self.__dict__.keys()):
                    if 'socialscience' not in locals():
                        socialscience = {}
                    socialscience['displayName'] = self.socialscience_displayName

                # Generate first level attributes
                for attr in self.__attr_import_dv_up_socialscience_fields_values:
                    if attr in list(self.__dict__.keys()):
                        if self.__getattribute__(attr) is not None:
                            v = self.__getattribute__(attr)
                            if isinstance(v, list):
                                multiple = True
                            else:
                                multiple = False
                            if attr in self.__attr_dict_dv_up_typeClass_primitive:
                                typeClass = 'primitive'
                            elif attr in self.__attr_dict_dv_up_typeClass_compound:
                                typeClass = 'compound'
                            elif attr in self.__attr_dict_dv_up_typeClass_controlledVocabulary:
                                typeClass = 'controlledVocabulary'
                            socialscience['fields'].append({
                                'typeName': attr,
                                'multiple': multiple,
                                'typeClass': typeClass,
                                'value': v
                            })

                # Generate targetSampleSize attributes
                if 'targetSampleSize' in list(self.__dict__.keys()):
                    if self.__getattribute__('targetSampleSize') is not None:
                        target_sample_size = self.__getattribute__('targetSampleSize')
                        tmp_dict = {}
                        if 'targetSampleActualSize' in target_sample_size:
                            if target_sample_size['targetSampleActualSize'] is not None:
                                tmp_dict['targetSampleActualSize'] = {}
                                tmp_dict['targetSampleActualSize']['typeName'] = 'targetSampleActualSize'
                                tmp_dict['targetSampleActualSize']['multiple'] = False
                                tmp_dict['targetSampleActualSize']['typeClass'] = 'primitive'
                                tmp_dict['targetSampleActualSize']['value'] = target_sample_size['targetSampleActualSize']
                        if 'targetSampleSizeFormula' in target_sample_size:
                            if target_sample_size['targetSampleSizeFormula'] is not None:
                                tmp_dict['targetSampleSizeFormula'] = {}
                                tmp_dict['targetSampleSizeFormula']['typeName'] = 'targetSampleSizeFormula'
                                tmp_dict['targetSampleSizeFormula']['multiple'] = False
                                tmp_dict['targetSampleSizeFormula']['typeClass'] = 'primitive'
                                tmp_dict['targetSampleSizeFormula']['value'] = target_sample_size['targetSampleSizeFormula']
                        socialscience['fields'].append({
                            'typeName': 'targetSampleSize',
                            'multiple': False,
                            'typeClass': 'compound',
                            'value': tmp_dict
                        })

                # Generate socialScienceNotes attributes
                if 'socialScienceNotes' in list(self.__dict__.keys()):
                    if self.__getattribute__('socialScienceNotes') is not None:
                        social_science_notes = self.__getattribute__('socialScienceNotes')
                        tmp_dict = {}
                        if 'socialScienceNotesType' in social_science_notes:
                            if social_science_notes['socialScienceNotesType'] is not None:
                                tmp_dict['socialScienceNotesType'] = {}
                                tmp_dict['socialScienceNotesType']['typeName'] = 'socialScienceNotesType'
                                tmp_dict['socialScienceNotesType']['multiple'] = False
                                tmp_dict['socialScienceNotesType']['typeClass'] = 'primitive'
                                tmp_dict['socialScienceNotesType']['value'] = social_science_notes['socialScienceNotesType']
                        if 'socialScienceNotesSubject' in social_science_notes:
                            if social_science_notes['socialScienceNotesSubject'] is not None:
                                tmp_dict['socialScienceNotesSubject'] = {}
                                tmp_dict['socialScienceNotesSubject']['typeName'] = 'socialScienceNotesSubject'
                                tmp_dict['socialScienceNotesSubject']['multiple'] = False
                                tmp_dict['socialScienceNotesSubject']['typeClass'] = 'primitive'
                                tmp_dict['socialScienceNotesSubject']['value'] = social_science_notes['socialScienceNotesSubject']
                        if 'socialScienceNotesText' in social_science_notes:
                            if social_science_notes['socialScienceNotesText'] is not None:
                                tmp_dict['socialScienceNotesText'] = {}
                                tmp_dict['socialScienceNotesText']['typeName'] = 'socialScienceNotesText'
                                tmp_dict['socialScienceNotesText']['multiple'] = False
                                tmp_dict['socialScienceNotesText']['typeClass'] = 'primitive'
                                tmp_dict['socialScienceNotesText']['value'] = social_science_notes['socialScienceNotesText']
                        socialscience['fields'].append({
                            'typeName': 'socialScienceNotes',
                            'multiple': False,
                            'typeClass': 'compound',
                            'value': tmp_dict
                        })

                """journal"""
                for attr in self.__attr_import_dv_up_journal_fields_values + list(self.__attr_import_dv_up_journal_fields_arrays.keys()) + ['journal_displayName']:
                    if attr in list(self.__dict__.keys()):
                        journal = {}
                        if not attr == 'journal_displayName':
                            journal['fields'] = []

                if 'journal_displayName' in list(self.__dict__.keys()):
                    journal['displayName'] = self.journal_displayName

                # Generate first level attributes
                for attr in self.__attr_import_dv_up_journal_fields_values:
                    if attr in list(self.__dict__.keys()):
                        if self.__getattribute__(attr) is not None:
                            v = self.__getattribute__(attr)
                            if isinstance(v, list):
                                multiple = True
                            else:
                                multiple = False
                            if attr in self.__attr_dict_dv_up_typeClass_primitive:
                                typeClass = 'primitive'
                            elif attr in self.__attr_dict_dv_up_typeClass_compound:
                                typeClass = 'compound'
                            elif attr in self.__attr_dict_dv_up_typeClass_controlledVocabulary:
                                typeClass = 'controlledVocabulary'
                            journal['fields'].append({
                                'typeName': attr,
                                'multiple': multiple,
                                'typeClass': typeClass,
                                'value': v
                            })

                # Generate fields attributes
                for key, val in self.__attr_import_dv_up_journal_fields_arrays.items():
                    if key in list(self.__dict__.keys()):
                        if self.__getattribute__(key) is not None:
                            journal['fields'].append({
                                'typeName': key,
                                'multiple': True,
                                'typeClass': 'compound',
                                'value': self.__generate_field_arrays(key, val)
                            })

                # TODO: prüfen, ob required attributes gesetzt sind. wenn nicht = Exception!
                data['datasetVersion']['metadataBlocks']['citation'] = citation
                if 'socialscience' in locals():
                    data['datasetVersion']['metadataBlocks']['socialscience'] = socialscience
                if 'geospatial' in locals():
                    data['datasetVersion']['metadataBlocks']['geospatial'] = geospatial
                if 'journal' in locals():
                    data['datasetVersion']['metadataBlocks']['journal'] = journal

                return data
            else:
                print('dict can not be created. Data is not valid for format')
                return None
        elif format == 'all':
            for attr in list(self.__dict__.keys()):
                if self.__getattribute__(attr) is not None:
                    data[attr] = self.__getattribute__(attr)
            return data
        else:
            print('dict can not be created. Format is not valid')
            return None

    def __generate_field_arrays(self, key, sub_keys):
        """Generate dicts for array attributes of Dataverse API metadata upload.

        Parameters
        ----------
        key : string
            Name of attribute.
        sub_keys : string
            List of keys to be created.

        Returns
        -------
        list
            List of filled :class:`dict`s of metadata for Dataverse API upload.

        """
        # check if attribute exists
        tmp_list = []
        if self.__getattribute__(key):
            attr = self.__getattribute__(key)
            # loop over list of attribute dict
            for d in attr:
                tmp_dict = {}
                # iterate over key-value pairs
                for k, v in d.items():
                    # check if key is in attribute list
                    if k in sub_keys:
                        multiple = None
                        typeClass = None
                        if isinstance(v, list):
                            multiple = True
                        else:
                            multiple = False
                        if k in self.__attr_dict_dv_up_typeClass_primitive:
                            typeClass = 'primitive'
                        elif k in self.__attr_dict_dv_up_typeClass_compound:
                            typeClass = 'compound'
                        elif k in self.__attr_dict_dv_up_typeClass_controlledVocabulary:
                            typeClass = 'controlledVocabulary'
                        tmp_dict[k] = {}
                        tmp_dict[k]['typeName'] = k
                        tmp_dict[k]['typeClass'] = typeClass
                        tmp_dict[k]['multiple'] = multiple
                        tmp_dict[k]['value'] = v
                tmp_list.append(tmp_dict)

        return tmp_list

    def json(self, format='dv_up'):
        """Create JSON output of different data formats.

        Parameters
        ----------
        format : string
            Data format for :class:`dict` creation. Available format so far are:
            ``dv_up``: Dataverse API Upload Dataset JSON metadata standard.
            ``all``: All attributes.

        Returns
        -------
        string
            JSON formatted string of Dataverse metadata for API upload.

        Examples
        -------
        Get JSON of Dataverse API upload::

            >>> from pyDataverse.models import Dataset
            >>> ds = Dataset()
            >>> data = {
            >>>     'title': 'pyDataverse study 2019',
            >>>     'dsDescription': [
            >>>         {'dsDescriptionValue': 'New study about pyDataverse usage in 2019'}
            >>>     ]
            >>>     'author': [{'authorName': 'LastAuthor1, FirstAuthor1'}],
            >>>     'datasetContact': [{'datasetContactName': 'LastContact1, FirstContact1'}],
            >>>     'subject': ['Engineering']
            >>> }
            >>> ds.set(data)
            >>> data = ds.json()

        Todo
        -------
        TODO: Validate standard
        TODO: Link to default JSON file

        """
        if format == 'dv_up' or format == 'all':
            return dict_to_json(self.dict(format=format))
        else:
            # TODO Exception
            print('data format not valid.')

    def export_data(self, filename, format='dv_up'):
        """Export Dataset metadata to different formats.

        Parameters
        ----------
        filename : string
            Filename with full path.
        format : string
            Data format for :class:`dict` creation. Available format so far are:
            ``dv_up``: Dataverse API Upload Dataset JSON metadata standard.
            ``all``: All attributes.

        Examples
        -------
        Export metadata to JSON file::

            >>> from pyDataverse.models import Dataset
            >>> ds = Dataset()
            >>> data = {
            >>>     'title': 'pyDataverse study 2019',
            >>>     'dsDescription': [
            >>>         {'dsDescriptionValue': 'New study about pyDataverse usage in 2019'}
            >>>     ]
            >>>     'author': [{'authorName': 'LastAuthor1, FirstAuthor1'}],
            >>>     'datasetContact': [{'datasetContactName': 'LastContact1, FirstContact1'}],
            >>>     'subject': ['Engineering'],
            >>> }
            >>> ds.set(data)
            >>> ds.export_data('export_dataset.json')

        """
        return write_json(filename, self.dict(format=format))


class Datafile(object):
    """Base class for the Datafile model.

    Parameters
    ----------
    filename : string
        Filename with full path.
    pid : type
        Description of parameter `pid` (the default is None).

    Attributes
    ----------
    description : string
        Description of datafile
    restrict : bool
        Unknown
    __attr_required_metadata : list
        List with required metadata.
    __attr_valid_metadata : list
        List with valid metadata for Dataverse API upload.
    __attr_valid_class : list
        List of all attributes.
    pid
    filename

    """

    """Attributes to be imported from `dv_up` file."""
    __attr_import_dv_up_values = [
        'description',
        'categories',
        'restrict',
        'title',
        'directoryLabel'
    ]

    """Required attributes for valid `dv_up` metadata dict creation."""
    __attr_dict_dv_up_required = [
        'pid',
        'filename'
    ]

    """Valid attributes for `dv_up` metadata dict creation."""
    __attr_dict_dv_up_valid = __attr_import_dv_up_values + __attr_dict_dv_up_required

    """Valid attributes for `all` metadata dict creation."""
    __attr_dict_all_valid = __attr_dict_dv_up_valid


    def __init__(self, filename=None, pid=None):
        """Init a Datafile() class.

        Parameters
        ----------
        filename : string
            Filename with full path.
        pid : string
            Persistend identifier, e.g. DOI.

        Examples
        -------
        Create a Datafile::

            >>> from pyDataverse.models import Datafile
            >>> df = Datafile()
            >>> df
            <pyDataverse.models.Datafile at 0x7f4dfc0466a0>

        """
        """Misc"""
        self.pid = pid
        self.filename = filename

        """Metadata"""
        self.description = None
        self.restrict = None

    def __str__(self):
        """Return name of Datafile() class for users."""
        return 'pyDataverse Datafile() model class.'

    def set(self, data):
        """Set class attributes with a flat dict.

        Parameters
        ----------
        data : dict
            Flat dict with data. Key's must be name the same as the class
            attribute, the data should be mapped to.

        Examples
        -------
        Set Datafile attributes via flat dict::

            >>> from pyDataverse.models import Datafile
            >>> df = Datafile()
            >>> data = {
            >>>     'pid': 'doi:10.11587/EVMUHP',
            >>>     'description': 'Test file',
            >>>     'categories': ['Data', 'Code'],
            >>>     'filename': 'tests/data/datafile.txt'
            >>> }
            >>> df.set(data)
            >>> df.pid
            'doi:10.11587/EVMUHP',

        """
        for key, val in data.items():
            self.__setattr__(key, val)

    def is_valid(self):
        """Check if set attributes are valid for Dataverse API metadata creation.

        Returns
        -------
        bool
            True, if creation of metadata JSON is possible. False, if not.

        Examples
        -------
        Check if metadata is valid for Dataverse API upload::

            >>> from pyDataverse.models import Datafile
            >>> df = Datafile()
            >>> data = {
            >>>     'pid': 'doi:10.11587/EVMUHP',
            >>>     'description': 'Test file',
            >>>     'categories': ['Data', 'Code'],
            >>>     'filename': 'tests/data/datafile.txt'
            >>> }
            >>> df.set(data)
            >>> df.is_valid
            True
            >>> df.filename = None
            >>> df.is_valid
            False

        """
        is_valid = True
        for attr in self.__attr_dict_dv_up_required:
            if attr in list(self.__dict__.keys()):
                if not self.__getattribute__(attr):
                    is_valid = False
                    print('Attribute \'{0}\' is `False`.'.format(attr))
            else:
                is_valid = False
                print('Attribute \'{0}\' missing.'.format(attr))
        return is_valid

    def dict(self, format='dv_up'):
        """Create dict in different data formats.

        Parameters
        ----------
        format : string
            Data format for dict creation. Available formats are: `dv_up` with
            all metadata for Dataverse API upload, and `all` with all attributes
            set.

        Returns
        -------
        dict
            Data as dict.

        Examples
        -------
        Check if metadata is valid for Dataverse API upload::

            >>> from pyDataverse.models import Datafile
            >>> df = Datafile()
            >>> data = {
            >>>     'pid': 'doi:10.11587/EVMUHP',
            >>>     'description': 'Test file',
            >>>     'categories': ['Data', 'Code']
            >>> }
            >>> df.set(data)
            >>> data = df.dict()
            >>> data['description']
            'Test file'

        Todo
        -------
        Validate standards.

        """
        data = {}
        if format == 'dv_up':
            if self.is_valid():
                for attr in self.__attr_dict_dv_up_valid:
                    # check if attribute exists
                    if attr in list(self.__dict__.keys()):
                        # check if attribute is not None
                        if self.__getattribute__(attr) is not None:
                            data[attr] = self.__getattribute__(attr)
                return data
            else:
                print('Dict can not be created. Data is not valid for format.')
                return None
        elif format == 'all':
            for attr in self.__attr_dict_all_valid:
                if attr in list(self.__dict__.keys()):
                    if self.__getattribute__(attr) is not None:
                        data[attr] = self.__getattribute__(attr)
            return data
        else:
            # TODO: Exception
            print('Format not right for dict.')
            return None

    def json(self, format='dv_up'):
        r"""Create JSON from attributes.

        Parameters
        ----------
        format : string
            Data format of input. Available formats are: `dv_up` for Dataverse
            API upload compatible format (default) and `all` with all attributes
            named in `__attr_valid_class`.

        Returns
        -------
        string
            JSON formatted string of Dataverse metadata for API upload.

        Examples
        -------
        Get dict of Dataverse metadata::

            >>> from pyDataverse.models import Datafile
            >>> df = Datafile()
            >>> data = {
            >>>     'pid': 'doi:10.11587/EVMUHP',
            >>>     'description': 'Test file',
            >>>     'categories': ['Data', 'Code']
            >>> }
            >>> df.set(data)
            >>> df.dict()
            {'description': 'Test file',
             'directoryLabel': None,
             'restrict': None}

        Todo
        -------
        Validate standards.
        Link to default JSON file

        """
        if format == 'dv_up' or format == 'all':
            data = self.dict(format=format)
            if data:
                return dict_to_json(data)
            else:
                return None
        else:
            # TODO Exception
            print('Data format not valid.')
            return None

    def export_data(self, filename, format='dv_up'):
        """Export Datafile metadata to different formats.

        Parameters
        ----------
        filename : string
            Filename with full path.
        format : string
            Data format for export. Available format so far are:
            ``dv_up``: Dataverse API Upload Dataverse JSON metadata standard.
            ``all``: All attributes.

        Examples
        -------
        Export Datafile metadata::

            >>> from pyDataverse.models import Datafile
            >>> df = Datafile()
            >>> data = {
            >>>     'pid': 'doi:10.11587/EVMUHP',
            >>>     'description': 'Test file',
            >>>     'categories': ['Data', 'Code']
            >>> }
            >>> df.set(data)
            >>> dv.export_data('dataverse_export.json')

        """
        if format == 'dv_up' or format == 'all':
            return write_json(filename, self.dict(format=format))
        else:
            # TODO: Exception
            print('Data-format not right.')
