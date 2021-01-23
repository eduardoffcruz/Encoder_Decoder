# -*- coding: utf-8 -*-
"""
Run-Length Encoding
Compress function - Adapted from: https://stackoverflow.com/questions/46572023/run-length-encoding-python
Decompress function - Developed by Eduardo F. F. Cruz
"""
import numpy as np        
from itertools import chain, groupby

def compress(iterable):
    compList=list(chain.from_iterable(
        (val, len([*thing]))
        for val, thing in groupby(iterable)
    ))
    ma=max(compList)
    mi=min(compList)
    if(ma<2**8 and mi>=0):
        return np.array(compList,dtype=np.uint8)
    elif(ma<2**8/2 and mi>=-2**8/2):
        return np.array(compList,dtype=np.int8)
    elif(ma<2**16 and mi>=0):
        return np.array(compList,dtype=np.uint16)
    elif(ma<2**16/2 and mi>=-2**16/2):
        return np.array(compList,dtype=np.int16)
    elif(ma<2**32 and mi>=0):
        return np.array(compList,dtype=np.uint32)
    elif(ma<2**32/2 and mi>=-2**32/2):
        return np.array(compList,dtype=np.int32)
    else:
        return np.array(compList)


def decompress(data):
    d=np.frombuffer(data, dtype=np.uint16)
    vals=d[::2]
    reps=d[1::2]
    decompressed=np.array([])
    for i in range(len(vals)-1):
        aux=np.empty(reps[i])
        aux[:] = vals[i] 
        decompressed=np.append(decompressed,aux) 
    return decompressed.astype(np.uint8)


 
def main():
    data=np.array([[1,2,3,3,3,4,3,3,5,5],[1,2,3,1,1,1,3,5,5,5],[1,2,3,3,3,4,3,5,5,2],[1,2,3,3,3,4,3,5,5,2],[1,1,1,1,1,1,1,1,1,1]])
    compressedData=compress(data.flatten()) #data.T.flatten()
    print('data:')
    print(data)
    print('compressed data:')
    print(compressedData)
    print(compressedData.dtype)
    print(bytearray(compressedData))
    print(decompress(bytearray(compressedData)))
    print(len(compressedData))

if __name__ == '__main__':
    main()

    
