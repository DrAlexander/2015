import sys
import argparse


def WriteFile(filename, code):
    try:
        with open(filename, 'wb') as f:
            f.write(''.join(code))
    except IOError:
        exit('No such file or directory ' + filename)


def ReadFile(filename):
    try:
        with open(filename, 'rb') as f:
            text = f.read()
    except IOError:
        exit('No such file or directory ' + filename)
    return text	


def VigenereCrypt(data, key):
    key_len = len(key)
    output = []
    for i in range(len(data)):
        tmp = chr(ord(data[i]) + ord(key[i % key_len]) % 256)
        output.append(tmp)
    return output


def VigenereDecrypt(data, key):
    key_len = len(key)
    output = []
    for i in range(len(data)):
        tmp = chr(ord(data[i]) - ord(key[i % key_len]) % 256)
        output.append(tmp)
    return output


def PrintUsage():
    print"Enter parameters:"
    print"<name of program> <file_in> <file_key> <file_out> <c / d>"
    sys.exit(-1)


def GetArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('inFile')
    parser.add_argument('keyFile')
    parser.add_argument('outFile')
    parser.add_argument('cryptOrDecrypt', choices=['c', 'd'])
    return parser.parse_args()	


def main():
    print"Vigenere"
    args = GetArgs()
    data = ReadFile(args.inFile)
    key = ReadFile(args.keyFile)
    if args.cryptOrDecrypt == 'c':
        print"Crypt:"
        res = VigenereCrypt(data, key)
    else:
        print"Decrypt:"
        res = VigenereDecrypt(data, key)
    WriteFile(args.outFile, res)


if __name__ == "__main__":
    main()