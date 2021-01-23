# -*- coding: utf-8 -*-
"""
PNG - SUB and UP filters (linear predictors)
---------------------------------------------
Developed by: 
    Eduardo F. F. Cruz         2018285164
"""
import numpy as np
def up(data):
    #expects image data matrix from img file (numpy array or list)
    data = np.asarray(data)
    data=np.append(data.flatten('F'),[data.shape]) #collums
    compList=np.concatenate(([data[0]],data[1:]-data[0:-1])) 
    ma=np.amax(compList)
    mi=np.amin(compList)
    if(ma<2**8 and mi>=0):
        return compList.astype(np.uint8)
    elif(ma<2**8/2 and mi>=-2**8/2):
        return compList.astype(np.int8)
    elif(ma<2**16 and mi>=0):
        return compList.astype(np.uint16)
    elif(ma<2**16/2 and mi>=-2**16/2):
        return compList.astype(np.int16)
    elif(ma<2**32 and mi>=0):
        return compList.astype(np.uint32)
    elif(ma<2**32/2 and mi>=-2**32/2):
        return compList.astype(np.int32)
    else:
        return compList
    
def sub(data):
    #expects image data matrix from img file (numpy array or list)
    data = np.asarray(data)
    data=np.append(data.flatten(),[data.shape]) #lines
    compList=np.concatenate(([data[0]],data[1:]-data[0:-1]))
    ma=np.amax(compList)
    mi=np.amin(compList)
    if(ma<2**8 and mi>=0):
        return compList.astype(np.uint8)
    elif(ma<2**8/2 and mi>=-2**8/2):
        return compList.astype(np.int8)
    elif(ma<2**16 and mi>=0):
        return compList.astype(np.uint16)
    elif(ma<2**16/2 and mi>=-2**16/2):
        return compList.astype(np.int16)
    elif(ma<2**32 and mi>=0):
        return compList.astype(np.uint32)
    elif(ma<2**32/2 and mi>=-2**32/2):
        return compList.astype(np.int32)
    else:
        return compList

def sub_dec(data):
    #expects flattened data
    d=np.frombuffer(data, dtype=np.int16)
    dec=np.copy(d)
    for i in range(1,len(dec)):
        dec[i]=dec[i-1]+d[i]
    #dec=dec[:-2].reshape(dec[-2],dec[-1])
    return dec

def up_dec(data):
    #expects flattened data
    d=np.frombuffer(data, dtype=np.int16)
    dec=np.copy(d)
    for i in range(1,len(dec)):
        dec[i]=dec[i-1]+d[i]
    #dec=dec[:-2].reshape(dec[-1],dec[-2])
    return dec.T

def main():
    print(up([[100,120,110,115],[100,120,110,115]]).dtype)
    print(up_dec(up([[100,120,110,115],[100,120,110,115]])))
    print(sub([[100,120,110,115],[100,120,110,115]]))
    print(sub_dec(sub([[100,120,110,115],[100,120,110,115]])))
    
if __name__=="__main__":
    main()