# -*- coding: utf-8 -*-
"""
Vigenère cipher encryption/decryption toolkit
Author: Alex von Brandenfels

Allows working with non-Latin alphabets
"""

class CryptoAlphabet(object):
    """
    A class that represents a particular alphabet.
    
    TODO: Add more detailed documentation
    """
    _alphabet = ""
    _alphaSize = 0
    _letter_index = {}
    _letter_frequencies = {} # TODO: Implement this
    
    def __init__(self, alphabetString):
        """
        TODO: Add documentation
        """
        self._alphabet = alphabetString.lower()
        self._alphaSize = len(self._alphabet)
        for i in range(len(self._alphabet)):
            self._letter_index[self._alphabet[i]] = i
        
    def encrypt(self, plaintext, key, decrypt=False):
        """
        TODO: Add documentation
        """
        result = []
        key = key.lower()
        key = [char for char in key] #Convert key from string to list of characters
        for i in range(len(key)):
        # Remove characters from the key if they are not in the alphabet
        # that we are using:
            if key[i] not in self._letter_index:
                key.pop(i) #This is O(len(key)), rather than constant time
                # TODO: Maybe replace this with something that is constant time?
        keyIndex = 0
        
        for char in plaintext:
            if char.lower() not in self._letter_index:
                #Put it straight into result without encrypting it
                result.append(char)
            else:
                is_capital = char.isupper()
                char = char.lower()
                letterVal = self._letter_index[char]
                keyVal = self._letter_index[key[keyIndex]]
                if decrypt: #To decrypt, we subtract keyVal instead of adding it
                    keyVal *= -1
                newChar = self._alphabet[(letterVal + keyVal) % self._alphaSize]
                if is_capital:
                    newChar = newChar.upper()
                result.append(newChar)
                keyIndex = (keyIndex + 1) % len(key)
            
        return ''.join(result) #Turn result into a string and return it
        
    def crack(ciphertext):
        """
        Attempts to decrypt a Vigenère-encrypted text with an unknown key
        """
        pass
        # TODO: Write this

def do_a_test(test_case_tuple):
    alphabet, message, key = test_case_tuple
    alphabet = CryptoAlphabet(alphabet)
    encrypted = alphabet.encrypt(message, key)
    decrypted = alphabet.encrypt(encrypted, key, decrypt=True)
    print("Original message: {}".format(message))
    print("Encrypted message: {}".format(encrypted))
    print("Decrypted message: {}".format(decrypted))
    if message == decrypted:
        print("Decrypted text matches original! Good job!")
    else:
        for i in range(100):
            print("PLEASE TO HELP I AM NOT GOOD WITH COMPUTER")
        
def main():
    tests = {"English": ("abcdefghijklmnopqrstuvwxyz", "If it can be destroyed by the truth, it deserves to be destroyed by the truth.", "Sagan"),
             "Russian": ("абвгдеёжзийклмнопрстуфхцчшщъыьэюя", "И жизнь хороша, и жить хорошо.", "Маяковский")}
    for test_key in tests:
        do_a_test(tests[test_key])

if __name__ == "__main__":
    main()