# -*- coding: utf-8 -*-
"""
--------------------------------------
[TInf_PL2] 
Trabalho_Prático 2
--------------------------------------
Eduardo F. F. Cruz         2018285164
--------------------------------------
"""
import sys
import os
import numpy as np
import matplotlib.image as mplimg
import matplotlib.pyplot as plt
import PIL.Image as im
#-------------
import gzip
import bz2
import lzma
import huffmancodec as huff
import LZ77 as lz77
import LZ78 as lz78
import LZW as lzw
import RLE as rle
import MTF as mtf
import arithmeticcoding as ac
import BurrowsWheeler as bw
import pngFilters

compressedPath='../data/compressed/' 
decompressedPath='../data/decompressed/'


def decompress(compressedFilename):
    decompressionOps=['rle','rleT','up','sub','lzma','bzip2','gzip','huff','lzw','mtf','bwt']
    splitted=compressedFilename.split('.')
    if(len(splitted)<=1): #invalid
        print('<!> '+compressedFilename+' file is not compressed!\n')
        return
    outName=''
    for compOp in splitted[1:]:
        if(compOp not in decompressionOps):
            print('<!> This decompressor does not support '+compOp.upper() +' compression!\n')
            return
        outName+='_'+compOp
    fi=open(compressedPath+compressedFilename,"rb")
    data=fi.read()
    fi.close()
    print('[@'+compressedFilename+'] Decompressing...')
    for i in range(len(splitted)-1,0,-1):
        if(splitted[i]=='rle'):
            data=rle.decompress(data)
        elif(splitted[i]=='rleT'):
            data=rle.decompress(data) #transpose
        elif(splitted[i]=='up'):
            data=pngFilters.up_dec(data)
        elif(splitted[i]=='sub'):
            data=pngFilters.sub_dec(data)
        elif(splitted[i]=='mtf'):
            data=mtf.decompress(data,np.arange(0,2**8,dtype=np.uint8))
        elif(splitted[i]=='bwt'):
            data=bw.ibwt(data[:-1],data[-1])
        elif(splitted[i]=='lzma'):
            data=lzma.decompress(data)
        elif(splitted[i]=='lzw'):
            data=lzw.decompress(data)
        elif(splitted[i]=='bzip2'):
            data=bz2.decompress(data)
        elif(splitted[i]=='gzip'):
            data=gzip.decompress(data)
        elif(splitted[i]=='huff'):
            data=huff.decode(data)

    if(splitted[i]=='rle' or splitted[i]=='sub'):
        data=data[:-2].reshape(data[-2],data[-1])
        im.fromarray(data.astype(np.uint8)).save(decompressedPath+splitted[0]+outName+".bmp") 
    elif(splitted[i]=='rleT' or splitted[i]=='up' ):
        data=data[:-2].reshape(data[-1],data[-2]).T
        im.fromarray(data.astype(np.uint8)).save(decompressedPath+splitted[0]+outName+".bmp") 
    elif(splitted[i]=='bzip2' or splitted[i]=='lzma' or splitted[i]=='gzip' or splitted[i]=='lzw' or splitted[i]=='bwt' or splitted[i]=='mtf' or splitted[i]=='huff'):
        fo = open(decompressedPath+splitted[0]+outName+".bmp", "wb") # open for [w]riting as [b]inary
        fo.write(data)
        fo.close()
    print('[@'+compressedFilename+'] Decompression Finished!\n')


def main():
    totalFileNum=len(os.listdir(compressedPath))

    if(len(sys.argv)>1):
        if sys.argv[1][:2]=='-f':
            if(len(sys.argv[1])>2):                
                fileQnt=int(sys.argv[1][2:]) #number of input files                
                if(fileQnt<=0 or fileQnt>totalFileNum):
                    print('[error]@ flag -f{num} with invalid {num} input')
                    exit()
            else:
                fileQnt=1    
            #load img data from input files 
            filenames=sys.argv[2:2+fileQnt]
    else: #no -f flag
        fileQnt=totalFileNum            
        filenames= os.listdir(compressedPath)

    for fname in filenames:
        decompress(fname)
        

if __name__=="__main__":
    main()