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
        """Creates a CryptoAlphabet object.
        
        Args:
            alphabetString: A string containing each letter of your alphabet,
                in order
        
        Returns:
            A CryptoAlphabet object for the given alphabet
        """
        self._alphabet = alphabetString.lower()
        self._alphaSize = len(self._alphabet)
        for i in range(len(self._alphabet)):
            self._letter_index[self._alphabet[i]] = i
    
    
    def sanitize(self, text):
        """
        Converts text to lowercase and strips any characters not in alphabet
        """
        result = []
        for character in text.lower():
            if character in self._alphabet:
                result.append(character)
        return "".join(result)
    
    def encrypt(self, plaintext, key, decrypt=False):
        """
        Encrypts or decrypts the given text with the given key.
        
        Everything will be converted to lowercase, and characters not in the
        alphabet will be removed.
        
        Args:
            plaintext: The plaintext (or ciphertext, if decrypting)
            key: The key to use for encryption/decryption
            decrypt: If true, decrypts instead of encrypting
        """
        result = []
        key = self.sanitize(key)
        plaintext = self.sanitize(plaintext)
        keyIndex = 0
        
        for character in plaintext:
            letterVal = self._letter_index[character]
            keyVal = self._letter_index[key[keyIndex]]
            if decrypt: #To decrypt, we subtract keyVal instead of adding it
                keyVal *= -1
            newChar = self._alphabet[(letterVal + keyVal) % self._alphaSize]
            result.append(newChar)
            keyIndex = (keyIndex + 1) % len(key) # add 1 to keyIndex modulo keysize
            
        return ''.join(result) #Turn result into a string and return it
        
        
    def crack(self, ciphertext):
        """
        Attempts to decrypt a Vigenère-encrypted text with an unknown key
        """
        pass
        # TODO: Write this

    def index_of_coincidence(self, text):
        """
        Calculates the index of coincidence for this text
        
        The index of coincidence represents the probability of selecting two of
        the same letter from the text, if we "drew" two letters from the text
        like a deck of cards.
        """
        # Count how many times each letter appears in this text:
        # First we make a dictionary with every letter having a count of 0:
        letter_frequencies = {letter:0 for letter in self._alphabet}
        # Now we count:
        for letter in text:
            letter_frequencies[letter] += 1
        # Find index of coincidence:
        textlength = len(text)
        sum = 0
        for letter in self._alphabet:
            frequency = letter_frequencies[letter]
            sum += (frequency/textlength) * ((frequency-1)/(textlength-1))
        return sum
        
    def get_columns(self, ciphertext, width):
        """
        Puts text into a matrix; returns a list with each column as a string
        
        Fills the top row of the matrix from left to right, then the next row,
        and keeps adding rows till the text is all gone. If there's empty space
        at the end of the last row, we just treat those columns as one shorter
        than the rest.
        
        args:
            ciphertext: The text to put into the matrix
            width: The width of the matrix
        """
        # Create empty "matrix":
        matrix = [[] for i in range(width)]
        column = 0
        for letter in ciphertext:
            matrix[column].append(letter)
            column = (column + 1) % width
        # Turn each column into a string:
        strings = []
        for column in matrix:
            strings.append("".join(column))
        return strings
        
    def find_likely_key_lengths(self, ciphertext, min_length, max_length):
        """
        Returns a list of tuples: (key_length, likelihood) sorted by likelihood
        
        If you put a Vigenère cipher into a matrix of width x, and you
        calculate the index of coincidence for each column in that matrix,
        the indices of coincidence will be higher if the key length is a factor
        of the width of the matrix.
        
        This becomes increasingly less effective as the length of the key
        approaches the length of the text. If the key is more than half as
        long as the text, this is very unlikely to work.
        
        We make tuples (key_length, likelihood), where likelihood is the sum
        of indices of coincidence for each column in the matrix of width
        key_length. Likelihood values are not normalized.
        
        args:
            ciphertext: The text to analyze
            min_length: The minimum possible key length
            max_length: The maximum possible key length
        """
        results = []
        for i in range(min_length, max_length):
            columns = self.get_columns(ciphertext, i)
            likelihood = 0
            for column in columns:
                likelihood += self.index_of_coincidence(column)
            results.append((i, likelihood/i))
        # Sort tuples by their second value (likelihood):
        results.sort(key=lambda x:x[1], reverse=True)
        return results
        
        
def do_a_test(alphabet, message, key):
    alphabet = CryptoAlphabet(alphabet)
    encrypted = alphabet.encrypt(message, key)
    decrypted = alphabet.encrypt(encrypted, key, decrypt=True)
    key_lengths = alphabet.find_likely_key_lengths(encrypted, 3, 20)
    print("Original message: {}".format(message))
    print("Encrypted message: {}".format(encrypted))
    print("Decrypted message: {}".format(decrypted))
    print("Likely key lengths: {}".format([x[0] for x in key_lengths[0:5]]))
    if alphabet.sanitize(message) == decrypted:
        print("Decrypted text matches original! Good job!")
    else:
        for i in range(100):
            print("PLEASE TO HELP I AM NOT GOOD WITH COMPUTER")
        
        
def main():
    tests = {"English": ("abcdefghijklmnopqrstuvwxyz", "It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of Darkness, it was the spring of hope, it was the winter of despair.", "Dickens"),
             "Russian": ("абвгдеёжзийклмнопрстуфхцчшщъыьэюя", "Я земной шар чуть не весь обошел,— и жизнь хороша, и жить хорошо. А в нашей буче, боевой, кипучей, и того лучше.", "Маяковский")}
    for test_key in tests:
        do_a_test(*tests[test_key])

if __name__ == "__main__":
    main()
