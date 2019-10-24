'''
Python Security Toolkit
Hash Decrypter
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



import hashlib
import sys
import argparse
import time



def menu():
    '''
    ***********************************************************************
    * Method name:    menu
    * Method purpose: To retrieve input for user's selection
    * Date created:   November 15, 2013
    * Last modified:  January 12, 2014, by: bbishop423
    * Parameters:     None
    * Return:         Integer
    ***********************************************************************
    '''
    menu_valid = True
    while (menu_valid):
        
        print("\n"*75)
        print(" Python Security Toolkit")
        print(" Hash Decrypter")
        print("\n ------------------ menu ------------------ ")
        print(" Please select your hash's algorithm.")
        print("  1.) MD5")
        print("  2.) SHA1")
        print("  3.) SHA224")
        print("  4.) SHA256")
        print("  5.) SHA384")
        print("  6.) SHA512")
        print("  7.) Exit program.\n")
        
        try:
            menu_selection = int(input(" Please enter your selection: "))
            if ((menu_selection > 0) and (menu_selection < 8)):
                menu_valid = False
            else:
                print("\n Invalid Selection.\n")
                input(" Press enter to continue.")
        except:
            print("\n Invalid selection.\n")
            input(" Press enter to continue.")
    return menu_selection



def test_pass(option_selected):
    '''
    ***********************************************************************
    * Method name:    test_pass
    * Method purpose: To test words against algorithm the user chose
    * Date created:   November 15, 2013
    * Last modified:  January 12, 2014, by: bbishop423
    * Parameters:     Integer
    * Return:         Void
    ***********************************************************************
    '''
    if ((option_selected > 0) and (option_selected < 7)):
        dictfile = sys.argv[1]
        hashfile = sys.argv[2]
        try:
            dict_file = open(dictfile, 'r')
        except:
            print(" Error! Could not open dictionary file.")
            sys.exit(0)
        try:
            hash_file = open(hashfile, 'r')
        except:
            print(" Error! Could not open hash file.")
            dict_file.close()
            sys.exit(0)
        hash_compare_word = hash_file.read()
        start_time = time.time()
        count_var = 0
        for word in dict_file:
            word = word.strip('\n')
            word = word.strip('\r')
            string_word = word
            try:
                word = str.encode(word, errors="strict")
            except UnicodeError:
                print(" Error converting unicode string in dictionary file to bytes.")
                dict_file.close()
                hash_file.close()
                sys.exit(0)
            if (option_selected == 1):
                hash_word = hashlib.md5()
            elif (option_selected == 2):
                hash_word = hashlib.sha1()
            elif (option_selected == 3):
                hash_word = hashlib.sha224()
            elif (option_selected == 4):
                hash_word = hashlib.sha256()
            elif (option_selected == 5):
                hash_word = hashlib.sha384()
            elif (option_selected == 6):
                hash_word = hashlib.sha512()
            hash_word.update(word)
            dict_compare_word = hash_word.hexdigest()
            count_var = count_var + 1
            if ((count_var % 1000) == 0):
                sys.stdout.write('.')
                sys.stdout.flush()
            if (str(hash_compare_word) == str(dict_compare_word)):
                end_time = time.time()
                end_time = (end_time - start_time)
                end_time = str(end_time)
                print("\n Match found.  Encrypted word is " + string_word)
                print(" Your encrypted word was found in " + end_time + " seconds.")
                dict_file.close()
                hash_file.close()
                sys.exit(0)
        end_time = time.time()
        end_time = (end_time - start_time)
        end_time = str(end_time)
        print("\n No match found.  Your word is not in the current dictionary file.")
        print(" It took " + end_time + " seconds to test each word in your dictionary file against the encrypted word.")
        dict_file.close()
        hash_file.close()
        sys.exit(0)
    else:
        print(" Thank you for using my program.  Goodbye.")
        sys.exit(0)



def main():
    '''
    ***********************************************************************
    * Method name:    main
    * Method purpose: To check command line for arguments and run menu function
    * Date created:   November 15, 2013
    * Last modified:  January 12, 2014, by: bbishop423
    * Parameters:     None
    * Return:         Void
    ***********************************************************************
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("dict", help="file containing dictionary to be used.")
    parser.add_argument("hash", help="file containing hash to be decoded.")
    args = parser.parse_args()
    user_selection = menu()
    test_pass(user_selection)



if __name__ == '__main__':
    main()
