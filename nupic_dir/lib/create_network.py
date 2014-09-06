#!/usr/bin/python
# coding: utf-8

net_structure = {
        'sensor1': ['region1'],
        #'region1': ['region2']
        }

"""
you need delete [:] at l.298
repos/nupic/build/release/lib/python2.7/site-packages/nupic/regions/RecordSensor.py

https://github.com/numenta/nupic/issues/727
"""
sensor_params = {
    'sensor1': {
        "xy_value": {
            "clipInput": True,
            "type": "VectorEncoderOPF",
            "dataType": "float",
            "n": 200,
            "w": 21,
            "length": 2,
            "fieldname": u"xy_value",
            "name": u"xy_value",
            "maxval": 100.0,
            "minval": 0.0,
        },
        'x_value': None,
        'y_value': None,
    },
}

dest_resgion_data = {
    'region1': {
        'SP_PARAMS':{
            "columnCount": 2024,
            "numActiveColumnsPerInhArea": 40,
            },
        'TP_PARAMS':{
            "cellsPerColumn": 32,
            },
        },
    # 'region2': {
    #     'SP_PARAMS':{
    #         "inputWidth": 2024 * 32,
    #         "columnCount": 2024,
    #         "numActiveColumnsPerInhArea": 40,
    #         },
    #     'TP_PARAMS':{
    #         "cellsPerColumn": 32,
    #         },
    #     },
 }

class_encoder_params = {
    "ftype": {
        "type": "CategoryEncoder",
        "fieldname": u"ftype",
        "name": u"ftype",
        "categoryList": ['plus', 'minus', 'flat', 'sin', 'quad', 'step'],
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