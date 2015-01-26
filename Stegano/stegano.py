#!/usr/bin/python

import sys
import re
import os
import operator
import Image, ImageDraw

'''
Output should be (.bmp)
'''

def parseArgs():    
    ''' 
        -c --code
        -d --decode
    '''
    cmd = 'inputFIleName {dat if -c} outputFileName {-c, -d}'
    lenARG = len (sys.argv)
    
    if lenARG<4 or lenARG>5:
        print "Error, wrong number of arguments"
        print cmd
        return None
    
      
    if not isThisFile(sys.argv[1]):
        print "The original image does not exist"
        print cmd
        return None
    
    if  lenARG == 5:
        if  not isThisFile(sys.argv[2]):
            print "Message file does not exist"
            print cmd
            return None
        
    if lenARG == 5:
        return sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    if lenARG == 4:
        return sys.argv[1], "ttt", sys.argv[2], sys.argv[3]


def isThisFile(fName):
    if os.path.exists(fName):
        if os.path.isfile(fName):
            return True
        else:
            return False
    else:
        return False

def changeEndBits(byte, bits):
    byte = ((byte >> 2) << 2) + int(bits, 2)
    return byte

def getEndBits(byte):
    byte = bin(byte)[2:].rjust(8, '0')
    return byte[6:8]

 
def code(imag, dat):                       
    imagSize = imag.size
    datSize = len(dat)
   
    if datSize > (imagSize[0]*imagSize[1])/2:
        print "Too much text size for this image"
        return None
    
    w = 0
    h = 0
    for byte in dat:
        block = bin(ord(byte))[2:].rjust(8, '0')        
       
        if w == imagSize[0]:
            w = 0
            h += 1
        
        for i in range(2):
            w += i
            if w == imagSize[0]:
                w = 0
                h += 1
                
            pixel = imag.getpixel((w, h))
       
            f_pix = changeEndBits(int(pixel[0]), block[4*i:4*i+2])
            s_pix = changeEndBits(int(pixel[1]), block[4*i+2:4*i+4])
        
            
            t_pix  = (int(pixel[2]) >> 2) << 2
 
            imag.putpixel((w, h), (f_pix, s_pix, t_pix))
        w += 1
    
    
    f_pixel = imag.getpixel((w, h))
    f_t  = ((int(f_pixel[2]) >> 2) << 2) + 3
    imag.putpixel((w, h), (int(f_pixel[0]), int(f_pixel[1]), f_t))
    
    return imag
 
 

def decode(imag):
    imagSize = imag.size
    dat = bytearray()
    byte = ''
    
    w = 0
    h = 0
    
    f_t = ''
    while 1:       
        if w == imagSize[0]:
            w = 0
            h += 1
        
        for i in range(2):
            w += i
            if w == imagSize[0]:
                w = 0
                h += 1
                
            pixel = imag.getpixel((w, h))
            
            f_bits = getEndBits(int(pixel[0]))
            s_bits = getEndBits(int(pixel[1]))
            t_bits = getEndBits(int(pixel[2]))          
            
            if t_bits != '11':
                byte += f_bits + s_bits
            else:
                return dat
           
        dat.append(int(byte,2))  
        byte = ''  
        w += 1

    
    return imag   
    
def main():
   
    try:
        inputFileName, datName, outputFileName, mode = parseArgs()
    except Exception as err:
        return
        

    imag = Image.open(inputFileName)


    if (mode == '-c'):
        inFile = open(datName, "r")
        dat = inFile.read()
        inFile.close()
        try:
            imag = code(imag, dat)
            imag.save(outputFileName)
        except Exception as err:
            return
    if (mode == '-d'):
        dat = decode(imag)
        outFile = open(outputFileName, "w")
        outFile.write(dat)
        outFile.close()
   
    

if __name__ == "__main__": 
    main()
