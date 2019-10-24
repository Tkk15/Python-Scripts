'''
Python Security Toolkit
Zip File Cracker
http://www.sourceforge.net/p/pythonsecuritytoolkit

This program is written in Python 3.  Please run it with a Python 3 interpreter.

Python Security Toolkit is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
Python Security Toolkit is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''



import zipfile
import argparse
import sys
import time



def extract_file(zipFile, passwd, stringword):
    '''
    ***********************************************************************
    * Method name:    extract_file
    * Method purpose: To test dictionary words against zip file
    * Date created:   November 15, 2013
    * Last modified:  January 12, 2014, by: bbishop423
    * Parameters:     Zip File Object, Byte String Object, String
    * Return:         Boolean
    ***********************************************************************
    '''
    try:
        zipFile.extractall(pwd=passwd)
        print("Success! Password is: " + stringword)
        zip_extracted = True
    except:
        zip_extracted = False
    return zip_extracted



def main():
    '''
    ***********************************************************************
    * Method name:    main
    * Method purpose: To parse command line arguments, open dictionary file,
        create zip file object, pass word from dictionary, and zip file
        object to extract_file()
    * Date created:   November 15, 2013
    * Last modified:  January 12, 2014, by: bbishop423
    * Parameters:     None
    * Return:         Void
    ***********************************************************************
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("dict", help="file containing dictionary to be used.")
    parser.add_argument("zip", help="zip file to run dictionary against.")
    args = parser.parse_args()
    dictfile = sys.argv[1]
    zippedfile = sys.argv[2]
    try:
        dict_file = open(dictfile, 'r')
    except:
        print('Error! Could not open dictionary file.')
        sys.exit(0)
    zip_file = zipfile.ZipFile(zippedfile)
    start_time = time.time()
    count_var = 0
    for word in dict_file:
        word = word.strip('\n')
        word = word.strip('\r')
        string_word = word
        word = str.encode(word)
        zip_extract = extract_file(zip_file, word, string_word)
        count_var = count_var + 1
        if ((count_var % 1000) == 0):
            sys.stdout.write('.')
            sys.stdout.flush()
        if (zip_extract):
            break
        else:
            continue
    dict_file.close()
    end_time = time.time()
    end_time = (end_time - start_time)
    end_time = str(end_time)
    if (zip_extract):
        print('Password was found in the dictionary in ' + end_time + ' seconds.')
        sys.exit(0)
    else:
        print('Password was not found in current dictionary.')
        print('The program took ' + end_time + ' seconds to check through all the words in the dictionary.')
        sys.exit(0)



if __name__ == '__main__':
    main()
