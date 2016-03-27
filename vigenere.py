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
    
    
    def strip_non_letters(self, text, case_sensitive=True):
        """
        Return a string that has been stripped of all characters not in
        the CryptoAlphabet
        """
        result = []
        for character in text:
            ok = (character in self._alphabet) or (not case_sensitive and character.lower() in self._alphabet)
            if ok:
                result.append(character)
                
        return "".join(result)
    
    def encrypt(self, plaintext, key, decrypt=False):
        """
        Encrypts or decrypts the given text with the given key.
        
        Capital letters will still be capital in the output, and non-letter
        characters will be preserved unchanged.
        
        Args:
            plaintext: The plaintext (or ciphertext, if decrypting)
            key: The key to use for encryption/decryption
            decrypt: If true, decrypts instead of encrypting
        """
        result = []
        key = key.lower()
        key = self.strip_non_letters(key)
        keyIndex = 0
        
        for character in plaintext:
            if character.lower() not in self._letter_index:
                # Space or punctuation - put it straight into result without
                # encrypting it
                result.append(character)
            else:
                is_capital = character.isupper() # remember if it's uppercase
                character = character.lower()
                letterVal = self._letter_index[character]
                keyVal = self._letter_index[key[keyIndex]]
                if decrypt: #To decrypt, we subtract keyVal instead of adding it
                    keyVal *= -1
                newChar = self._alphabet[(letterVal + keyVal) % self._alphaSize]
                if is_capital:
                    # If it was uppercase before, make it uppercase again
                    newChar = newChar.upper()
                result.append(newChar)
                keyIndex = (keyIndex + 1) % len(key) # add 1 to keyIndex modulo keysize
            
        return ''.join(result) #Turn result into a string and return it
        
        
    def crack(ciphertext):
        """
        Attempts to decrypt a Vigenère-encrypted text with an unknown key
        """
        pass
        # TODO: Write this

        
def do_a_test(alphabet, message, key):
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
        do_a_test(*tests[test_key])

if __name__ == "__main__":
    main()