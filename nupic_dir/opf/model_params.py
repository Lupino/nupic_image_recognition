config = \
{ 'aggregationInfo': { 'days': 0,
                       'fields': [],
                       'hours': 0,
                       'microseconds': 0,
                       'milliseconds': 0,
                       'minutes': 0,
                       'months': 0,
                       'seconds': 0,
                       'weeks': 0,
                       'years': 0},
  'model': 'CLA',
  'modelParams': { 'anomalyParams': { u'anomalyCacheRecords': None,
                                      u'autoDetectThreshold': None,
                                      u'autoDetectWaitRecords': None},
                   'clParams': { 'alpha': 0.050050000000000004,
                                 'clVerbosity': 0,
                                 'regionName': 'CLAClassifierRegion',
                                 'steps': '0'},
                   'inferenceType': 'TemporalMultiStep',
                   'sensorParams': { 'encoders': { 'label': { 'classifierOnly': True,
                                                                         'fieldname': 'label',
                                                                         "type": "CategoryEncoder",
                                                                         "categoryList": [i for i in range(10)],
                                                                         'name': 'label',
                                                                         'w': 21},
                                                   u"pixel": {
                                                       "clipInput": True,
                                                       "type": "VectorEncoderOPF",
                                                       "dataType": "float",
                                                       "n": 200,
                                                       "w": 21,
                                                       "length": 27,
                                                       "fieldname": u"pixel",
                                                       "name": u"pixel",
                                                       "maxval":  15.0,
                                                       "minval": -15.0},
                                                   },
                                     'sensorAutoReset': None,
                                     'verbosity': 0},
                   'spEnable': True,
                   'spParams': { 'columnCount': 2048,
                                 'globalInhibition': 1,
                                 'inputWidth': 0,
                                 'maxBoost': 2.0,
                                 'numActiveColumnsPerInhArea': 40,
                                 'potentialPct': 0.8,
                                 'seed': 1956,
                                 'spVerbosity': 0,
                                 'spatialImp': 'cpp',
                                 'synPermActiveInc': 0.05,
                                 'synPermConnected': 0.1,
                                 'synPermInactiveDec': 0.05015},
                   'tpEnable': True,
                   'tpParams': { 'activationThreshold': 14,
                                 'cellsPerColumn': 32,
                                 'columnCount': 2048,
                                 'globalDecay': 0.0,
                                 'initialPerm': 0.21,
                                 'inputWidth': 2048,
                                 'maxAge': 0,
                                 'maxSegmentsPerCell': 128,
                                 'maxSynapsesPerSegment': 32,
                                 'minThreshold': 11,
                                 'newSynapseCount': 20,
                                 'outputType': 'normal',
                                 'pamLength': 3,
                                 'permanenceDec': 0.1,
                                 'permanenceInc': 0.1,
                                 'seed': 1960,
                                 'temporalImp': 'cpp',
                                 'verbosity': 0},
                   'trainSPNetOnlyIfRequested': False},
  'predictAheadTime': None,
  'version': 1}
