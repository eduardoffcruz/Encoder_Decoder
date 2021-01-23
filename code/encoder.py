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


#global
originalPath='../data/original/' #relative path to original data
compressedPath='../data/compressed/' 
totalFileNum=4 #total number of files in dataPath

def loadImgData(filename):
    return mplimg.imread(originalPath+filename)

def flattenData(data):
    #convert multidimensional data array to unidimensional array 
    if(data.ndim>1):
        return data.flatten()     
    else: #if data array is already unidimensional
        return data
        
def getOccurrenceArray(data,alphabet): #return occurrences array 
    #Note: alphabet is always unidimensional 
    occurrences=np.zeros(len(alphabet))#create zeros array with len==len(alphabet)
    for sample in data:
        occurrences[sample]+=1
    return occurrences
    
def viewHistogram(alphabet,occurrences,title):
    plt.figure()
    plt.bar(alphabet,occurrences)
    plt.xlabel("Alphabet Symbols")
    plt.ylabel("Symbol Occurrence")
    plt.title(title)
    plt.tight_layout()

def getEntropy(nSamples,occurrences): #return entropy value and probability's array
    probability=occurrences[occurrences>0]/nSamples #calculate probability only for nonzero occurrence values
    
    return (-np.sum(probability*np.log2(probability))),probability #consider only nonzero probabilities
  
def pairData(data,alphabet): #grouping source's data in pairs (integers only)
    dataLen=len(data)
    alphabetLen=len(alphabet)
    if(dataLen%2==1): #in case dataLen is odd..ignore last element from data
        data=data[:dataLen-1]
        
    ##group source samples as pairs
    #NOTE:if we used a more complex/inefficient way of pairing data we would be able to decompress that paired data back to unpaired data..but, for the purpose of this experiment we don't need to unpair data after it has been paired (compressed)
    pairedData=data[::2]*alphabetLen+data[1::2] #efficiency purposes
    ##generate alphabet with paired symbols     
    pairedAlphabet=np.arange(0,alphabetLen**2,dtype=np.uint16) #bottom 0 because source datatype is always unsigned int8 
            
    return pairedData,pairedAlphabet 

#######################-------MAIN------##########################################
def main(): 
    filenames=['pattern.bmp','egg.bmp','zebra.bmp','landscape.bmp'] #default
    originalFiles=[] #structure: [data,alphabet,occurrencesArray]
    commandi=1
    flags=[False]*len(filenames) #if True, compression has already been applied to the original data
        
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
            for i in range(fileQnt):
                originalFiles.append([loadImgData(filenames[i]),np.array([]),np.array([])])  #all files are monocromatic images with one channel only         
            commandi+=fileQnt+1
        else: #no -f flag
            fileQnt=totalFileNum            
            #load img data from Files         
            for i in range(fileQnt):
                originalFiles.append([loadImgData(filenames[i]),np.array([]),np.array([])])                    
           
        if('-info' in sys.argv):            
            #print info about original data (e.g. entropy's value, save histogram image,..)
            for i in range(fileQnt):
                filename=filenames[i]
                nBits=int(str(originalFiles[i][0].dtype)[4:])
                nSamples=flattenData(originalFiles[i][0]).shape[0]
                originalFiles[i][1]=np.arange(0,2**nBits,dtype=originalFiles[i][0].dtype) #img alphabet from 0 to (2**nBits)-1
                originalFiles[i][2]=getOccurrenceArray(flattenData(originalFiles[i][0]),originalFiles[i][1])
                viewHistogram(originalFiles[i][1],originalFiles[i][2],filename+' @ Symbol\'s Occurrence Histogram')
                plt.savefig('../histograms/'+filename[:-4]+'.svg') #save histogram image as svg in histograms folder
                entropy,probabilities=getEntropy(nSamples,originalFiles[i][2])  
                print(filename+' @ File Size {} MBytes (without compression)'.format(os.path.getsize(originalPath+filename)/(1024*1024)))
                print(filename+' @ {} bits/symbol (without compression)'.format(nBits))
                print(filename+' @ Entropy = {} bits/symbol'.format(entropy))
        
        posfix=['']*fileQnt #to store the format of the compressed file
        #COMPRESSION OPTIONS:
        for compressionOp in sys.argv[commandi:]:
            for i in range(fileQnt):               
                if(compressionOp=='-huff'):
                    #Huffman Coding
                    if(flags[i]):
                        fi=open(compressedPath+filenames[i][:-4]+posfix[i],"rb")
                    else:
                        fi=open(originalPath+filenames[i],"rb")
                    data=fi.read() 
                    fi.close()
                    posfix[i]+='.huff'
                    fo=open(compressedPath+filenames[i][:-4]+posfix[i],"wb")
                    print(filenames[i]+' @ Huffman Compression STARTED..') 
                    codec=huff.HuffmanCodec.from_data(data) 
                    fo.write(codec.encode(data))
                    print(filenames[i]+' @ Huffman Compression FINISHED!')                 
                    fo.close()                    
                    flags[i]=True
                elif(compressionOp=='-gzip'):                    
                    #GZIP
                    if(flags[i]):
                        fi=open(compressedPath+filenames[i][:-4]+posfix[i],"rb")
                    else:
                        fi=open(originalPath+filenames[i],"rb")
                    data=fi.read() 
                    fi.close()
                    posfix[i]+='.gzip'
                    fo=open(compressedPath+filenames[i][:-4]+posfix[i],"wb")
                    print(filenames[i]+' @ GZip Compression STARTED..') 
                    fo.write(gzip.compress(data))    
                    print(filenames[i]+' @ GZip Compression FINISHED!')                   
                    fo.close()                    
                    flags[i]=True
                elif(compressionOp=='-bzip2'):
                    #BZIP2
                    if(flags[i]):
                        fi=open(compressedPath+filenames[i][:-4]+posfix[i],"rb")
                    else:
                        fi=open(originalPath+filenames[i],"rb")
                    data=fi.read() 
                    fi.close()
                    posfix[i]+='.bzip2'
                    fo=open(compressedPath+filenames[i][:-4]+posfix[i],"wb")
                    print(filenames[i]+' @ BZip2 Compression STARTED..') 
                    fo.write(bz2.compress(data))    
                    print(filenames[i]+' @ BZip2 Compression FINISHED!')                  
                    fo.close()                    
                    flags[i]=True
                elif(compressionOp=='-lzma'):
                    #LZMA
                    if(flags[i]):
                        fi=open(compressedPath+filenames[i][:-4]+posfix[i],"rb")
                    else:
                        fi=open(originalPath+filenames[i],"rb")
                    data=fi.read() 
                    fi.close()
                    posfix[i]+='.lzma'
                    fo=open(compressedPath+filenames[i][:-4]+posfix[i],"wb")
                    print(filenames[i]+' @ LZMA Compression STARTED..') 
                    fo.write(lzma.compress(data))    
                    print(filenames[i]+' @ LZMA Compression FINISHED!')                  
                    fo.close()                    
                    flags[i]=True                    
                elif(compressionOp=='-lz77'):    
                    #LZ77
                    if(flags[i]):
                        fi=compressedPath+filenames[i][:-4]+posfix[i]
                    else:
                        fi=originalPath+filenames[i]
              
                    posfix[i]+='.lz77'
                    fo=compressedPath+filenames[i][:-4]+posfix[i]
                    print(filenames[i]+' @ LZ77 Compression STARTED..') 
                    codec=lz77.LZ77Compressor(window_size=20)
                    codec.compress(fi,fo)   
                    print(filenames[i]+' @ LZ77 Compression FINISHED!')                                   
                    flags[i]=True                
                elif(compressionOp=='-lz78'): 
                    #LZ78
                    if(flags[i]):
                        fi=compressedPath+filenames[i][:-4]+posfix[i]
                    else:
                        fi=originalPath+filenames[i]
                    posfix[i]+='.lz78'
                    fo=compressedPath+filenames[i][:-4]+posfix[i]
                    print(filenames[i]+' @ LZ78 Compression STARTED..')
                    codec=lz78.LZ78Compressor()
                    codec.compress(fi,fo)   
                    print(filenames[i]+' @ LZ78 Compression FINISHED!')                                   
                    flags[i]=True 
                elif(compressionOp=='-lzw'):
                    #LZW
                    if(flags[i]):
                        fi=compressedPath+filenames[i][:-4]+posfix[i]
                    else:
                        fi=originalPath+filenames[i]
                    data=lzw.readbytes(fi)
                    posfix[i]+='.lzw'                    
                    fo=compressedPath+filenames[i][:-4]+posfix[i]
                    print(filenames[i]+' @ LZW Compression STARTED..')                    
                    lzw.writebytes(fo,lzw.compress(data))   
                    print(filenames[i]+' @ LZW Compression FINISHED!')                    
                    flags[i]=True
                elif(compressionOp=='-rle'):
                    if(flags[i]):
                        fi=open(compressedPath+filenames[i][:-4]+posfix[i],"rb")
                        data=fi.read()
                        posfix[i]+='.rle'
                        print(filenames[i]+' @ Run-Length Encoding Transform STARTED..') 
                        data=rle.compress(data)
                        fi.close()                    
                    #determine wether it's better to transpose matrix or not to get the best result!
                    else:
                        print(filenames[i]+' @ Run-Length Encoding Transform STARTED..') 
                        data=np.append(flattenData(originalFiles[i][0]),originalFiles[i][0].shape)
                        dataT=np.append(flattenData(originalFiles[i][0].T),originalFiles[i][0].shape) #transpose
                        comp=rle.compress(data)
                        compT=rle.compress(dataT)#transpose
                        if(len(comp)<=len(compT)):
                            data=comp                             
                            posfix[i]+='.rle'
                        else:
                            data=compT
                            posfix[i]+='.rleT'
                    fo=open(compressedPath+filenames[i][:-4]+posfix[i],"wb")
                    fo.write(data.tobytes())
                    #print(rle.compress(data))
                    print(filenames[i]+' @ Run-Length Encoding Transform FINISHED!')                  
                    fo.close()                    
                    flags[i]=True
                elif(compressionOp=='-group'):
                    #samples will have 16bits instead of 8 after grouping
                    #group symbols
                    #apply to raw data only (uint8)..only to reduce redudancy!! Bom..grouping+huffman coding!
                    if(len(originalFiles[i][1])==0): 
                        #get alphabet
                        nBits=8 #uint8
                        originalFiles[i][1]=np.arange(0,2**nBits,dtype=np.uint8) #img alphabet from 0 to (2**nBits)-1                        
                    ######################################
                    if(flags[i]):
                        fi=open(compressedPath+filenames[i][:-4]+posfix[i],"rb")
                        data=np.fromfile(fi,dtype=np.uint8)
                        fi.close()
                        data,_=pairData(data,originalFiles[i][1]) #alphabet grows to len(data)**2 symbols (not a memory issue..)
                    else: 
                        data,_=pairData(flattenData(originalFiles[i][0],originalFiles[i][1])) #alphabet grows to len(data)**2 symbols (not a memory issue..)
                    data=np.append(data,originalFiles[i][0].shape)
                    posfix[i]+='.group'
                    fo=open(compressedPath+filenames[i][:-4]+posfix[i],"wb")
                    print(filenames[i]+' @ Symbol\'s Grouping Transform STARTED..') 
                    fo.write(data)
                    print(filenames[i]+' @ Symbol\'s Grouping Transform FINISHED!')                  
                    fo.close()                    
                    flags[i]=True                    
                elif(compressionOp=='-mtf'): 
                    #Move-To-Front Transform
                    if(len(originalFiles[i][1])==0): 
                        #get alphabet
                        nBits=8 #uint8
                        originalFiles[i][1]=np.arange(0,2**nBits,dtype=np.uint8) #img alphabet from 0 to (2**nBits)-1  
                    if(flags[i]):
                        fi=open(compressedPath+filenames[i][:-4]+posfix[i],"rb")
                        data=np.fromfile(fi,dtype=np.uint8)
                        fi.close()                        
                    else: 
                        data=flattenData(originalFiles[i][0])
                    posfix[i]+='.mtf'
                    fo=open(compressedPath+filenames[i][:-4]+posfix[i],"wb")
                    print(filenames[i]+' @ Move-to-Front Transform STARTED..') 
                    fo.write((mtf.compress(data,originalFiles[i][1])).tobytes())
                    print(filenames[i]+' @ Move-to-Front Transform FINISHED!')                   
                    fo.close()                    
                    flags[i]=True
                elif(compressionOp=='-bwt'):
                    ##################
                    winSize=1048576*2
                    ##################
                    compData=np.array([],dtype=np.uint8)
                    if(flags[i]):
                        fi=open(compressedPath+filenames[i][:-4]+posfix[i],"rb")
                        data=np.fromfile(fi,dtype=np.uint8)
                        fi.close()                        
                    else: 
                        data=flattenData(originalFiles[i][0])
                    posfix[i]+='.bwt'
                    fo=open(compressedPath+filenames[i][:-4]+posfix[i],"wb")
                    print(filenames[i]+' @ Burrows-Wheeler Transform STARTED..') 
                    print(int(np.floor(len(data)/winSize)))
                    for k in range(int(np.floor(len(data)/winSize))-1):
                        bwt_ref, idx = bw.bwt(data[k*winSize:k*winSize+winSize])
                        encoded = [data[x] for x in bwt_ref]
                        if(idx<2**8 or idx>=0):
                            tp=(np.uint8)
                        elif(idx<2**8/2 or idx>=-2**8/2):
                            tp=(np.int8)
                        elif(idx<2**16 or idx>=0):
                            tp=(np.uint16)
                        elif(idx<2**16/2 or idx>=-2**16/2):
                            tp=(np.int16)
                        elif(idx<2**32 or idx>=0):
                            tp=(np.uint32)
                        elif(idx<2**32/2 or idx>=-2**32/2):
                            tp=(np.int32)
                        compData=np.append(compData,np.append(np.array(encoded),[idx])).astype(tp)
                        print(k)
                    k+=1
                    bwt_ref, idx = bw.bwt(data[k*winSize:])
                    encoded = [data[x] for x in bwt_ref]
                    if(idx<2**8 or idx>=0):
                        tp=(np.uint8)
                    elif(idx<2**8/2 or idx>=-2**8/2):
                        tp=(np.int8)
                    elif(idx<2**16 or idx>=0):
                        tp=(np.uint16)
                    elif(idx<2**16/2 or idx>=-2**16/2):
                        tp=(np.int16)
                    elif(idx<2**32 or idx>=0):
                        tp=(np.uint32)
                    elif(idx<2**32/2 or idx>=-2**32/2):
                        tp=(np.int32)
                    compData=np.append(compData,np.append(np.array(encoded),[idx])).astype(tp)
                    fo.write(compData.tobytes())                    
                    print(filenames[i]+' @ Burrows-Wheeler Transform FINISHED!')                   
                    fo.close()                    
                    flags[i]=True                
                elif(compressionOp=='-sub'):
                    posfix[i]+='.sub'
                    #PNG Sub filter
                    if(flags[i]):
                        print('[error]@ Sub filter should be applied only to IMG raw data (not flattened)')
                        exit()
                    fo=open(compressedPath+filenames[i][:-4]+posfix[i],"wb")
                    print(filenames[i]+' @ Sub Filtering STARTED..') 
                    originalFiles[i][0]=pngFilters.sub(originalFiles[i][0])
                    fo.write(originalFiles[i][0].tobytes())
                    print(filenames[i]+' @ Sub Filtering FINISHED!')  
                    fo.close()
                    flags[i]=True
                    
                    #update alphabet
                    originalFiles[i][1]=np.arange(-2**8+1,2**8,dtype=np.int16) #update dictionary
                    if(originalFiles[i][0][-2] not in originalFiles[i][1]):
                        originalFiles[i][1]=np.append(originalFiles[i][1],originalFiles[i][0][-2]).astype(np.int16)
                    if(originalFiles[i][0][-1] not in originalFiles[i][1]):
                        originalFiles[i][1]=np.append(originalFiles[i][1],originalFiles[i][0][-1]).astype(np.int16)                      
                elif(compressionOp=='-up'):
                    posfix[i]+='.up'
                    #PNG Sub filter
                    if(flags[i]):
                        print('[error]@ Up filter should be applied only to IMG raw data (not flattened)')
                        exit()
                    fo=open(compressedPath+filenames[i][:-4]+posfix[i],"wb")
                    print(filenames[i]+' @ Up Filtering STARTED..') 
                    originalFiles[i][0]=pngFilters.up(originalFiles[i][0])  
                    fo.write(originalFiles[i][0].tobytes())
                    print(filenames[i]+' @ Up Filtering FINISHED!')
                    fo.close()
                    flags[i]=True
                    
                    #update alphabet
                    originalFiles[i][1]=np.arange(-2**8+1,2**8,dtype=np.int16) #update dictionary
                    if(originalFiles[i][0][-2] not in originalFiles[i][1]):
                        originalFiles[i][1]=np.append(originalFiles[i][1],originalFiles[i][0][-2]).astype(np.int16)
                    if(originalFiles[i][0][-1] not in originalFiles[i][1]):
                        originalFiles[i][1]=np.append(originalFiles[i][1],originalFiles[i][0][-1]).astype(np.int16)                       
        
                elif(compressionOp=='-info'):
                    break #next compressionOp
                else:
                    print('[error]@ invalid compression -flag!\n\toptions > -huff -gzip -bz2 -lzma -lz77 -lz78 -lzw -rle -up -sub -bwt -mtf -group')
                    return
                
                if(flags[i]):
                    print(filenames[i]+" @ File was sucessfully compressed with {} MBytes".format(os.path.getsize(compressedPath+filenames[i][:-4]+posfix[i])/(1024*1024)))
            
            
    else: #no input parameters
        fileQnt=totalFileNum                
        #load all files and print histograms + entropy values        
        for i in range(fileQnt):
            filename=filenames[i]
            originalFiles.append(flattenData(loadImgData(filename)))
            nBits=int(str(originalFiles[i].dtype)[4:])
            nSamples=originalFiles[i].shape[0]
            alphabet=np.arange(0,2**nBits,dtype=originalFiles[i].dtype) #img alphabet from 0 to (2**nBits)-1
            oc=getOccurrenceArray(originalFiles[i],alphabet)
            viewHistogram(alphabet,oc,filename+' @ Symbol\'s Occurrence Histogram')
            plt.savefig('../histograms/'+filename[:-4]+'.svg') #save histogram image as svg in histograms folder
            entropy,probabilities=getEntropy(nSamples,oc)
            originalSize=(nSamples*nBits)/(8*1024*1024)   #in MBytes             
            print(filename+' @ File Size {} MBytes (without compression)'.format(originalSize))
            print(filename+' @ {} bits/symbol (without compression)'.format(nBits))
            print(filename+' @ Entropy = {} bits/symbol'.format(entropy))
                
        


if __name__=="__main__":
    main()
    
    '''
    elif(compressionOp=='-arith'):
                    if(flag):
                        fi=open(compressedPath+"compressed_"+filenames[i][:-4]+posfix[i],"rb")
                        data=np.fromfile(fi,dtype=np.uint8)
                        fi.close()
                    else:
                        data=originalFiles[i][0]  
                    print(filenames[i]+' @ Arithmetic Compression STARTED..') 
                    #get alphabet and occurrences data
                    nBits=8 #uint8
                    alph=np.arange(0,2**nBits,dtype=np.uint8) #img alphabet from 0 to (2**nBits)-1  
                    oc=getOccurrenceArray(data,alph)
                    freq={alph[j]:oc[j] for j in range(2**nBits)}
                    codec=ac.ArithmeticEncoding(frequency_table=freq, save_stages=False)
                    compdata,_=codec.encode(msg=data,probability_table=codec.probability_table)
                    posfix[i]+='arith'
                    fo=open(compressedPath+"compressed_"+filenames[i][:-4]+posfix[i],"wb")                    
                    print(compdata)
                    print(codec.decode(encoded_msg=compdata, msg_length=len(data),probability_table=codec.probability_table))
                    #fo.write(struct.pack('>d',data))
                    #print(rle.compress(data))
                    print(filenames[i]+' @ Arithmetic Compression FINISHED!')                  
                    fo.close()                    
                    flag=True
    '''