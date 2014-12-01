#!/usr/bin/python
# coding: utf-8

net_structure = {
        'sensor1': ['region1'],
        'region1': ['region2']
        }

"""
you need delete [:] at l.298
repos/nupic/build/release/lib/python2.7/site-packages/nupic/regions/RecordSensor.py

https://github.com/numenta/nupic/issues/727
"""
sensor_params = {
    'sensor1': {
        "pixel": {
            "type": "SparsePassThroughEncoder",
            "n": 1000,
            "fieldname": u"pixel",
            "verbosity": 1,
        },
    },
}

dest_resgion_data = {
    'region1': {
        'SP_PARAMS':{
            "columnCount": 2024,
            "numActiveColumnsPerInhArea": 40,
            "potentialRadius": 100,   # default value: 16
            },
        'TP_PARAMS':{
            "cellsPerColumn": 32,
            },
        },
    'region2': {
        'SP_PARAMS':{
            "inputWidth": 2024 * 32,
            "columnCount": 2024,
            "potentialRadius": 100,   # default value: 16
            "numActiveColumnsPerInhArea": 40,
            },
        'TP_PARAMS':{
            "cellsPerColumn": 32,
            },
        },
 }

class_encoder_params = {
    "label": {
        "type": "CategoryEncoder",
        "fieldname": u"label",
        "name": u"label",
        "categoryList": [i for i in range(10)],
        "w": 21,
        },
    }


# TODO: こんな形で予測するところだけにclassifierを設置.
#       stepもここで指定したい.
# predict_data = {
#     'predict1': {
#         'region': 'region1',
#         'step': 0,
#         'predict_value': 'ftype',
#         'encoder': {
#             "type": "CategoryEncoder",
#             "fieldname": u"ftype",
#             "name": u"ftype",
#             "categoryList": ['plus', 'minus', 'flat', 'sin', 'quad', 'step'],
#             "w": 21,
#         }
#     }
# }
