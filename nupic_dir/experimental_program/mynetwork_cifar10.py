#!/usr/bin/env python
# encoding: utf-8
import copy
import json
import numpy
from collections import defaultdict, Counter

from nupic.algorithms.anomaly import computeAnomalyScore
from nupic.engine import Network
from nupic.encoders import MultiEncoder

from netowrk import Network as myNetwork

from nupic_dir.lib.load_data import load_dataset, get_patch


def stochastic_encoder(inputArray, minVal=0, maxVal=255, sample_number=20):
    """
    inputArray : (32,32)
    return : (32,32)
    """
    result = []
    numInput = reduce(lambda x,y: x*y, inputArray.shape)
    prob   = inputArray.reshape(numInput).astype("float32") / maxVal

    sample = numpy.ones(numInput)
    for i in range(sample_number):
        for j, p in enumerate(prob):
            sample[j] = numpy.random.binomial(n=1, p=p)
        result.append(sample.reshape(inputArray.shape) )
    return result

def temporal_scalor_encoder(inputArray, minVal=0, maxVal=255):
    """
    inputArray : (32,32)
    return : (n, 32,32)
    """

    encoder = MultiEncoder()
    encoder.addMultipleEncoders({
            "x": {
                    "type": "ScalarEncoder",
                    "fieldname": u"x",
                    "name": u"x",
                    "maxval": 255.0,
                    "minval": 0.0,
                    "n": 20,
                    "w": 3,
                    "clipInput": True,
                    "forced": True
            },
    })
    numInput   = reduce(lambda x,y: x*y, inputArray.shape)

    result = numpy.ones([numInput, encoder.getWidth()])

    for i, value in enumerate(inputArray.reshape(numInput)):
        encoder.encodeIntoArray({'x': value}, result[i])

    result = numpy.transpose(result, (1,0))  # [numInput, encoder.getWidth()] -> [encoder.getWidth(), numInput]
    result = result.reshape( (encoder.getWidth(), inputArray.shape[0], inputArray.shape[1]))
    return result


PARAMS = {
    'SP': {
        "spVerbosity": 0,
        "spatialImp": "cpp",
        "globalInhibition": 1,
        "columnCount": 2048,
        #"columnCount": 2048, SP(32, 32) -> TP(1024)
        # This must be set before creating the SPRegion
        #"potentialRadius": 3,                 # default 16
        "inputWidth": 0,
        "numActiveColumnsPerInhArea": 40,
        "seed": 1956,
        "potentialPct": 0.8,
        "synPermConnected": 0.1,
        "synPermActiveInc": 0.01,   # default: 0.0001
        "synPermInactiveDec": 0.05, # default: 0.0005
        "maxBoost": 1.0,
    },
    'TP':{
        "verbosity": 0,
        "columnCount": 2048,
        "cellsPerColumn": 32,
        "inputWidth": 2048,
        "seed": 1960,
        "collectStats": True,
        "temporalImp": "cpp",
        "newSynapseCount": 20,
        "maxSynapsesPerSegment": 32,
        "maxSegmentsPerCell": 128,
        "initialPerm": 0.21,
        "permanenceInc": 0.1,
        "permanenceDec": 0.1,
        "globalDecay": 0.0,
        "maxAge": 0,
        "minThreshold": 9,
        "activationThreshold": 12,
        "outputType": "normal",
        "pamLength": 3,
    },
    'CL':{
        "clVerbosity": 0,
        "alpha": 0.005,
        "steps": "0"
    },
}

def createSensorEncoder():
    """Create the encoder instance for our test and return it."""
    encoder = MultiEncoder()
    encoder.addMultipleEncoders({
            "x": {
                    #"type": "ScalarEncoder",
                    "type": "VectorEncoderOPF",
                    "length": 64,
                    "fieldname": u"x",
                    "name": u"x",
                    "maxval": 255.0,
                    "minval": 0.0,
                    "n": 100,
                    "w": 21,
                    "clipInput": True,
            },
    })

    return encoder

def createClassifierEncoder():
    """Create the encoder instance for our test and return it."""
    encoder = MultiEncoder()
    encoder.addMultipleEncoders({
            "y": {
                    "type": "SDRCategoryEncoder",
                    "categoryList": ["label-" + str(x) for x in range(10)],
                    #"categoryList": ["white", "gray1", "gray2", "black"],
                    "fieldname": u"y",
                    "name": u"y",
                    "n": 102400,
                    "w": 121,
            },
    })

    return encoder

"""
--------------------------------------------
Nupic Network
--------------------------------------------
"""

"""
実験内容
1. 2次元SPをした場合としない場合で結果に違いが出るか?
   2次元SPの法が良い結果になることはあるか?

  + 縦線と横線の判別.
  + 縦線と横線の動きの判別.

2. 確率的エンコーダーを利用して, 色の違いを判別できるか?
  + 9x9, １色の判別.
"""

def deleteParam():
    # sp
    del PARAMS['SP']["columnCount"]
    del PARAMS['SP']["inputWidth"]
    del PARAMS['SP']["spatialImp"]

    # tp
    del PARAMS['TP']['columnCount']
    del PARAMS['TP']["inputWidth"]
    del PARAMS['TP']["temporalImp"]

    # cl
    del PARAMS['CL']["clVerbosity"]


def createMyNetworkSimple():

    network = myNetwork()

    # set SP
    PARAMS['SP']["inputDimensions"]             = (20, 32, 32)
    PARAMS['SP']["columnDimensions"]            = (10, 8, 8)
    PARAMS['SP']["numActiveColumnsPerInhArea"]  = int(10. * 8. * 8. * 0.02)
    network.addRegion("simplePoolerRegion", "SP", PARAMS['SP'])
    network.calc_sort.append("simplePoolerRegion")

    # # set TP
    # PARAMS['TP']['numberOfCols']   = 20 * 20
    # PARAMS['TP']['cellsPerColumn'] = 10
    # network.addRegion("stpPoolerRegion", "TP", PARAMS['TP'])
    # network.link("simplePoolerRegion", "stpPoolerRegion")

    network.initialize()

    return network


def createMyNetworkComplex():

    network = myNetwork()

    # set SP
    PARAMS['SP']["inputDimensions"]             = (40960,) # 32 *32 * 100
    PARAMS['SP']["columnDimensions"]            = (64 * 64, )  # default 64 * 64
    PARAMS['SP']["numActiveColumnsPerInhArea"]  = 80      # default: 80
    network.addRegion("spatialPoolerRegion", "SP", PARAMS['SP'])

    # set TP
    PARAMS['TP']['numberOfCols']   = 64 * 64            # default: 64 * 64
    PARAMS['TP']['cellsPerColumn'] = 6
    network.addRegion("temporalPoolerRegion", "TP", PARAMS['TP'])
    network.link("spatialPoolerRegion", "temporalPoolerRegion")

    # set Classifier
    PARAMS['CL']["steps"] = [0,1]
    network.addRegion( "classifierRegion", "CL", PARAMS['CL'])
    network.link("temporalPoolerRegion", "classifierRegion")

    network.initialize()

    return network

def initialize_myNetwork(simpleNetwork, myNetwork):
    SimpleRegion = simpleNetwork.regions["simplePoolerRegion"]
    SimpleRegion.setLearnmode(True)

    # Make sure learning is enabled
    SPRegion = myNetwork.regions["spatialPoolerRegion"]
    SPRegion.setLearnmode(True)


    TPRegion = myNetwork.regions["temporalPoolerRegion"]
    TPRegion.setLearnmode(True)

    return

def set_learn_myNetwork(simpleNetwork, myNetwork, enable):
    SimpleRegion = simpleNetwork.regions["simplePoolerRegion"]
    SimpleRegion.setLearnmode(enable)

    # Make sure learning is enabled
    SPRegion = myNetwork.regions["spatialPoolerRegion"]
    SPRegion.setLearnmode(enable)

    TPRegion = myNetwork.regions["temporalPoolerRegion"]
    TPRegion.setLearnmode(enable)
    return


#@profile
def runCifar10Network(train_data, train_label, simpleNetwork, complexNetwork, datanum=0, length=1000, learnMode=True):

    def toOneArray(Array):
        input_len = reduce(lambda x,y: x * y, Array.shape)
        return Array.reshape((input_len))

    global tnum

    set_learn_myNetwork(simpleNetwork, complexNetwork, learnMode)
    result = []

    patch_heigh = 32
    patch_width = 32
    patch_step  = 32

    simplePoolerRegion   = simpleNetwork.regions["simplePoolerRegion"]
    #stpPoolerRegion      = simpleNetwork.regions["stpPoolerRegion"]

    spatialPoolerRegion  = complexNetwork.regions["spatialPoolerRegion"]
    temporalPoolerRegion = complexNetwork.regions["temporalPoolerRegion"]
    classifierRegion     = complexNetwork.regions["classifierRegion"]

    prevPredictedColumns = []

    # encoder
    vector_encoder = createSensorEncoder()
    label_encoder  = createClassifierEncoder()


    #
    sdr_data = defaultdict(list)
    label_patch_data = []
    base_sdr = None

    datanum_i = datanum
    for i, data in enumerate(train_data[datanum:datanum+length]):
        # print
        # print "============================ ", i

        patch_data, movement = get_patch(data, height=patch_heigh, width=patch_width, step=patch_step)
        label = train_label[datanum_i][0]
        label_name = "label-" + str(label)

        dataset  = []

        for pnum, patch in enumerate(patch_data):

            """
            temporal_scalor_encoder
            3次元SP利用
                return activeColumns
                => 色の濃さは共通している.
                => 形状も多少共通しているように見える.
                => そしてTPないから速い.
            """
            dataset = temporal_scalor_encoder(patch)
            simpleNetwork.run(toOneArray(dataset))
            activeColumns = simplePoolerRegion.getOutput()

            sdr_data[str(label)].append(activeColumns.nonzero()[0])

            """
            """
            # if 4 in activeColumns.nonzero()[0]:
            #     label_patch_data.append(patch)
            #     print datanum_i, pnum, activeColumns.nonzero()[0]
            if pnum >= 0:
                if base_sdr == None:
                    base_patch = patch
                    base_sdr = activeColumns.nonzero()[0]
                    print 'base : ', base_sdr
                else:
                    if len(set(base_sdr) & set(activeColumns.nonzero()[0]))  >= len(base_sdr)/2:
                        print datanum_i, pnum, activeColumns.nonzero()[0]
                        label_patch_data.append(patch)

            # Classifier
            activeCells = activeColumns.nonzero()[0]
            res = classifierRegion.getObj().compute(
                            recordNum=tnum,
                            patternNZ=activeCells,
                            classification={
                                'bucketIdx': createClassifierEncoder().getBucketIndices({'y': label_name})[0] if learnMode else 0,
                                'actValue': label_name if learnMode else 'no'},
                            learn=learnMode,
                            infer=True
                            )
            predict_0 = res['actualValues'][res[0].tolist().index(max(res[0]))]
            pri = "\033[32mOK\033[0m" if label_name ==  predict_0 else "\033[31mNG\033[0m"
            if learnMode:
                print '%s  y:%s  p0:%s rate:%5.2f  %s' % (datanum_i, label_name, predict_0, max(res[0]), pri)
            else:
                result.append(label_name ==  predict_0)

            tnum += 1

        datanum_i += 1
        continue

    # """
    # """
    # from PIL import Image
    # img = Image.new('L', (80, 80))
    # numpy.random.shuffle(label_patch_data)   # 同じ画像内ばかりでないようにshuffle.
    # #label_patch_data.insert(0, base_patch)   # 左上がbase_patchになるように.
    # for i, patch in enumerate(label_patch_data[:100]):
    #     image_patch = patch.reshape((8,8))
    #     for a in range(8):
    #         for b in range(8):
    #             aidx = (i * 8 + a)  % 80
    #             bidx = (i / 10) * 8 + b
    #             img.putpixel((bidx,aidx), image_patch[a][b])
    # img.show()


    # Task1. 得られるSDRは, 同じlabelの集合の方が共通するカラムが多いか確認.
    #        => そんなことない. label集合からとっても, 全集合からとっても変わりなし.

    # def sample_and_cell(data):
    #     numpy.random.shuffle(data)
    #     return len(set(data[0]) & set(data[1]))

    # print '============ same cell in SDR =============='
    # sample_num = 10000
    # for label, data in sorted(sdr_data.items(), key=lambda x: x[0]):
    #     cell_num = []
    #     for x in range(sample_num):
    #         cell_num.append(sample_and_cell(data))
    #     print  label, round(numpy.mean(cell_num), 3), round(numpy.std(cell_num),3)
    #     continue
    #
    # cell_num = []
    # data =  reduce(lambda x,y: x+y, sdr_data.values())
    # for x in range(sample_num):
    #     cell_num.append(sample_and_cell(data))
    # print  "all", round(numpy.mean(cell_num), 3), round(numpy.std(cell_num), 3)





    if not learnMode:
        print "collect count : ", result.count(True) , "/", len(result)


    return simpleNetwork, complexNetwork


if __name__ == "__main__":
    print "load data "
    train_data, train_label = load_dataset('./data/pylearn2_test/train.pkl')
    #test_data, test_label = load_dataset('./data/pylearn2_test/test.pkl')

    deleteParam()

    print "make createMyNetworkSimple"
    simpleNetwork  = createMyNetworkSimple()
    complexNetwork = createMyNetworkComplex()

    print "initialize createMyNetworkSimple"
    initialize_myNetwork(simpleNetwork, complexNetwork)


    print "run network"
    tnum    = 0
    datanum = 0
    for i in range(40):
        print
        print 'train: ' +  str(datanum)
        simpleNetwork, complexNetwork = runCifar10Network(train_data, train_label, simpleNetwork, complexNetwork, datanum, length=500, learnMode=True)
        #datanum += 500
        datanum = 0

        print
        print 'valid: ' +  str(datanum)
        simpleNetwork, complexNetwork = runCifar10Network(train_data, train_label, simpleNetwork, complexNetwork, 49000, length=100, learnMode=False)


    # datanum = 0
    # for i in range(1):
    #     print
    #     print 'train: ' +  str(datanum)
    #     network = runCifar10Network(train_data, train_label, network, datanum, length=1000,learnMode=True)

    # datanum = 0
    # for i in range(1):
    #     print
    #     print 'train: ' +  str(datanum)
    #     network = runCifar10Network(train_data, train_label, network, datanum, length=1000,learnMode=True)
