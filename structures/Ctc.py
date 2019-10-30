# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 02:08:51 2019

@author: AsteriskAmpersand
"""

from collections import OrderedDict
try:
    import mathutils as np
    Matrix = np.Matrix
    Vector = np.Vector
    from ..common.Cstruct import PyCStruct, FileClass
except:
    import sys
    sys.path.insert(0, r'..\common')
    from Cstruct import PyCStruct, FileClass
    import numpy as np
    Matrix = np.matrix
    Vector = lambda x: np.matrix(x).transpose()

class Header(PyCStruct):
	fields = OrderedDict([
	("filetype","char[4]"),
	("unknownsConstantIntSet","int[3]"),
	("numARecords","int"),
	("numBRecords","int"),
	("unknownConstantInt","int"),
	("updateTicks","float"),
	("poseSnapping","float"),
	("chainDamping","float"),
	("reactionSpeed","float"),
	("gravityMult","float"),
	("windMultMid","float"),
	("windMultLow","float"),
	("windMultHigh","float"),
	("unknownFloatSet","float[3]"),
	("fixedBytes","byte[8]"),])#1 1 1 1 1 1 0 0
#} header 

class ARecord(PyCStruct):
	fields = OrderedDict([
	("chainLength","int"),
	("collision","byte"),
	("weightiness","byte"),
	("unknownByteSet","byte[2]"),
   ("fixedNegativeOne","byte[4]"),
   ("oneZeroZeroZero1","byte[4]"),
   ("oneZeroZeroZero2","byte[4]"),
   ("unknownByteSetCont","byte[12]"),
	("xGravity","float"),
	("yGravity","float"),
	("zGravity","float"),
	("zeroFloat","float"),
	("xInertia","float"),
	("yInertia","float"),
	("zInertia","float"),
	("unknownFloatTwo","float"),#100
	("unknownFloatThree","float"),#0
	("unknownFloatFour","float"),#0.1
	("windMultiplier","float"),
	("lod","int"),])
#} arecord [ header.numARecords ] 
class BRecord(PyCStruct):
    fields = OrderedDict([
	("m00","float"),
	("m10","float"),
	("m20","float"),
	("m30","float"),
	("m01","float"),
	("m11","float"),
	("m21","float"),
	("m31","float"),
	("m02","float"),
	("m12","float"),
	("m22","float"),
	("m32","float"),
	("m03","float"),
	("m13","float"),
	("m23","float"),
	("m33","float"),
	("zeroSet1","byte[2]"),
	("isChainParent","byte"),
	("unknownByteSetTwo","byte[5]"),
	("boneFunctionID","int"),
	("zeroSet3","byte[4]"),
	("unknownFloatSet","float[4]"),])
    
    def marshall(self, data):
        super().marshall(data)
        self.Matrix = Matrix(        
        [[self.m00, self.m01, self.m02, self.m03],
         [self.m10, self.m11, self.m12, self.m13],
         [self.m20, self.m21, self.m22, self.m23],
         [self.m30, self.m31, self.m23, self.m33],
         ])
        self.Vector = Vector(self.unknownFloatSet)
        return self
        
#} brecord [ header.numBRecords ] }}
    
class CtcChain():
    def __init__(self,arecord,brecords):
        self.chain = arecord
        self.nodes = [next(brecords) for _ in range(arecord.chainLength)]
        
    def __len__(self):
        return len(self.nodes)
    
    def __iter__(self):
        return iter(self.nodes)
    
class Ctc():
    def marshall(self,data):
        self.Header = Header().marshall(data)
        arecords = [ARecord().marshall(data) for _ in range(self.Header.numARecords)]
        brecords = [BRecord().marshall(data) for _ in range(self.Header.numBRecords)]
        biter = iter(brecords)
        self.Chains = [CtcChain(chain,biter) for chain in arecords]
        return self
    def __iter__(self):
        return iter(self.Chains)
CtcFile = FileClass(Ctc)

def norm(v):
    return np.sqrt(v[0]**2+v[1]**2+v[2]**2)

def ifAdd(dictionary, key, data):
    if key in dictionary:
        dictionary[key].append(data)
    else:
        dictionary[key]=[data]
    return dictionary

if __name__ == "__main__":
    from pathlib import Path
    for ctcf in Path(r"E:\MHW\Merged").rglob("*.ctc"):
        ctc = CtcFile(ctcf).data
        for chain in ctc:
            c = chain.chain


    """
    uci = set()
    ui = set()
    ufs = [set() for _ in range(3)]
    ubs = [set() for _ in range(8)]
    
    ws = [set() for i in range(2)]
    ws2 = [set() for i in range(12)]
    centi = {}
    zero = {}
    uno = {}
    
        uci.add(tuple(ctc.Header.unknownsConstantIntSet))
        ui.add(ctc.Header.unknownConstantInt)
        for v,s in zip(ctc.Header.unknownFloatSet,ufs):
            s.add(v)
        for v,s in zip(ctc.Header.unknownByteSet,ubs):
            s.add(v)
            ifAdd(centi, chain.chain.unknownFloatTwo, ctcf.relative_to("E:\MHW\Merged").as_posix())
            ifAdd(zero, chain.chain.unknownFloatThree, ctcf.relative_to("E:\MHW\Merged").as_posix())
            ifAdd(uno, chain.chain.unknownFloatFour, ctcf.relative_to("E:\MHW\Merged").as_posix())
            for byte, container in zip(chain.chain.unknownByteSet,ws):
                container.add(byte)
            for byte, container in zip(chain.chain.unknownByteSetCont,ws2):
                container.add(byte)   
    outputroot = Path(r"G:\Wisdom\DataOutputs")
    with outputroot.joinpath("centi.csv").open("w") as fil:
        json.dump(centi,fil)
    with outputroot.joinpath("zero.csv").open("w") as fil:
        json.dump(zero,fil)
    with outputroot.joinpath("uno.csv").open("w") as fil:
        json.dump(uno,fil)
    for entry in ws:
        print(entry)
    for entry in ws2:
        print(entry)
    print(uci)
    print(ui)
    print(ufs)
    print(ubs)
    """