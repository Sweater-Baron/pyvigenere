import vigenere

def main():
    alphabet = vigenere.CryptoAlphabet("abcdefghijklmnopqrstuvwxyz")
    text = input("Enter some text to encrypt: ")
    key = input("Enter a key to use for encryption: ")
    print("Your encrypted text is: {}".format(alphabet.encrypt(text, key)))
    input("Press enter to exit")
    
if __name__ == "__main__":
    main()