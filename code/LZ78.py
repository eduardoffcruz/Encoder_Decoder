# -*- coding: utf-8 -*-
"""
LZ78
Obtained from : https://github.com/war-and-peace/LZ78 {Rakhimov Abdurasul}
"""

class Node:
    '''Represents a node of a tree for building LZ78 compression
    Each node stores a value which is a symbol from input file
    Also it stores an index of itself and a dictionary of childrens
    '''

    def __init__(self, value=None, index=None):
        self.value = value
        self.index = index
        self.children = {}

    def getIndex(self):
        return self.index
    
    def addChild(self, value, index=None):
        node = Node(value, index)
        self.children[value] = node
        return node

    def findValue(self, value):
        if value in self.children.keys():
            return self.children[value]
        else:
            return None
    

class LZ78Compressor:
    '''LZ78 compressor class.
    It constructs a tree for compression as it was in the algorithm
    '''

    def __init__(self):
        '''Constructor function'''
        self.root = Node(index=0)
        self.mapping = []
        self.next_index = 1
    
    def clear(self):
        '''Clears all the variables in the class. Prepares it for the next file'''

        self.root = Node(index=0)
        self.mapping = []
        self.next_index = 1

    def findLastOne(self, node, inputs):
        '''Finds the index of the last byte of the file if not previously found'''

        for i in inputs:
            node = node.findValue(i)
        return self.mapping[node.getIndex() - 1]

    def addToTree(self, node, input):
        '''Adds a new entitiy to the tree'''

        childNode = node.findValue(input)
        if childNode is None:
            node.addChild(input, self.next_index)
            self.mapping.append((node.getIndex(), input))
            self.next_index = self.next_index + 1
            return self.root
        else:
            return childNode 

    def compress(self, inputPath, outputPath):
        '''Implements LZ78 compression algorithm.
        Compresses the file located in path inputPath,
        Writes the output to the file in path outputPath
        Uses the compression method described in the description of the assignmnet
        '''
        
        self.clear()
        next_node = self.root
        inp = []
        
        f=open(inputPath, 'rb')
        inp = list(f.read())
        f.close()    
        for binary_input in inp:
            next_node = self.addToTree(next_node, binary_input)

        f=open(outputPath, "wb")
        for index, value in self.mapping:                
            self.writeIndex(f, index)
            f.write(value.to_bytes(1, 'big'))
                
        if next_node is not self.root:
            index, value = self.mapping[next_node.getIndex() - 1]
            self.writeIndex(f, index)
            f.write(value.to_bytes(1, 'big'))
        f.close()
        
        
        
    def writeIndex(self, file, index):
        '''Writes an index to the file in a special form that was described in the assignment description'''
        
        last = True
        ans = ""
        if index == 0:
            file.write(int(128).to_bytes(1, 'big'))
            return
        while index > 0:
            offset = index % 128
            index = index // 128
            if last:
                last = False
                ans = (bin(offset + 128)[2:]) + ans
            else:
                ans = (bin(offset)[2:]).zfill(8) + ans
        
        number = int(ans, 2)
        bstring = number.to_bytes((len(ans) + 7) // 8, 'big')
        file.write(bstring)
    
class LZ78Decompressor:
    '''LZ78 Decompressor class
    Constructor receives path to a directory where the compressed files are located
    '''

    def __init__(self, directoryPath):
        '''Constructor function'''

        self.directoryPath = directoryPath
        self.root = Node(index=0)
        self.mapping = []
        self.next_index = 1
    
    def clear(self):
        '''Clears the class variables in order to prepare them for next file'''

        self.root = Node(index=0)
        self.mapping = []
        self.next_index = 1

    def checkLast(self, byte):
        '''Checks if the byte is the last byte in the sequence
        In particular it checks whether the binary representation of the byte starts with 1
        '''

        return (int.from_bytes(byte, 'big') > 127)

    def byteToInt(self, byte):
        '''Converts bytes object into int'''

        return int.from_bytes(byte, 'big')
    
    def bytesToInt(self, bytes):
        '''converts list of bytes objects into list of ints'''

        if(len(bytes) == 0):
            print("Something went wrong")
        stringForm = ""
        for i in bytes:
            stringForm += (((bin(int.from_bytes(i, "big"))[2:]).zfill(8))[1:])
        return int(stringForm, 2)

    def readOneItem(self, file):
        '''Helper function to distinguish between separate entities in compressed file'''

        bytesList = []
        while True:
            nextByte = file.read(1)
            if not nextByte:
                return None, None
            bytesList.append(nextByte)
            if self.checkLast(nextByte):
                index = self.bytesToInt(bytesList)
                symbol = file.read(1)
                return index, symbol

    def decompress(self, inputPath, outputPath):
        '''Implementation of the LZ78 decompression algorithm.
        Receives an input file location and output file location and decompresses the input file
        '''

        self.clear()
        self.mapping.append(None)
        mlen = 1
        outputFile = open(outputPath, "wb")
        with open(inputPath, "rb") as f:
            while True:
                index, symbol = self.readOneItem(f)
                if index is None:
                    break
                if index >= mlen:
                    raise Exception("Wrong input file. Input file might not be compressed with LZ78")
                prefix = self.mapping[index]
                result = None
                if prefix is None:
                    result = symbol
                else:
                    result = prefix + symbol
                self.mapping.append(result)
                mlen += 1
                outputFile.write(result)
        outputFile.close()


