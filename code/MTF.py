# -*- coding: utf-8 -*-
"""
Addapted from:
https://github.com/ArezooAbdollahi/Lossless-image-compression-with-Hilbert-Curve-and-Move-to-Front

"""
import numpy as np

def compress(arr,alphabet):
    #import ipdb; ipdb.set_trace()
    st=list(alphabet) 
    print('Alphabet Data Type: '+str(alphabet.dtype))
    n=len(arr)
    cw=np.zeros(n,dtype=alphabet.dtype)
    for i in range(n):
        item=arr[i]
        index=st.index(item)
        cw[i]=index
        st.pop(index)
        st=[item]+st
    return cw

def decompress(arr,alphabet):
    st=list(alphabet)  
    n=len(arr)
    data=np.zeros(n,dtype=alphabet.dtype)
    #import ipdb; ipdb.set_trace()
    for i in range(n):
        code=arr[i]
        symbol=st[code]
        data[i]=symbol
        st.pop(code)
        st=[symbol]+ st
    return data
