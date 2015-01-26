import sys
import argparse
import encrypt
import decrypt

def writing(name, data):
    outF = open(name, 'w')
    outF.write(''.join(data))
	
def reading(name):
    try:
        with open(name, 'r') as inF:
            text = inF.read()
    except IOError:
        exit('No this file in directory')
    return text	
	
def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('inFile')
    parser.add_argument('key')
    parser.add_argument('out')
    parser.add_argument('mod')
    return parser.parse_args()	
    
def main():
    args = getArgs()
    data = reading(args.inFile)
    key = reading(args.key)

    if args.mod == 'c':
        encrypt_ = encrypt.main(data, key)
        writing(args.out, encrypt_)
    else:
        decrypte_ = decrypt.main(data, key)
        writing(args.out, decrypte_)
if __name__ == "__main__":
 main()
    
