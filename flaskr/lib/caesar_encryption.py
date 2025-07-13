def encrypt_text(plaintext, n: int):
    ans = ""
    # iterate over the given text
    for i in range(len(plaintext)):
        ch = plaintext[i]
        # check if space is there then simply add space
        if ch == " ":
            ans += " "
        # check if a character is uppercase then encrypt it accordingly
        elif (ch.isupper()):
            ans += chr((ord(ch) + n-65) % 26 + 65)
        # check if a character is lowercase then encrypt it accordingly
        else:
            ans += chr((ord(ch) + n-97) % 26 + 97)
    return ans


def decrypt(encrypted_message, k: int):
    # enter your encrypted message(string) below
    # encrypted_message = input("Enter the message i.e to be decrypted: ").strip()
    letters = "abcdefghijklmnopqrstuvwxyz"
    # enter the key value to decrypt
    # k = int(input("Enter the key to decrypt: "))
    decrypted_message = ""
    for ch in encrypted_message:
        if ch in letters:
            position = letters.find(ch)
            new_pos = (position - k) % 26
            new_char = letters[new_pos]
            decrypted_message += new_char
        else:
            decrypted_message += ch
    # print("Your decrypted message is:\n")
    return decrypted_message

def main():
    # print(decrypt("lnltlao dcfevs guaqthd", -3))
    plaintext = "jupiter" #"hellow evryone"
    n = -3
    print("Plain Text is : " + plaintext)
    print("Shift pattern is : " + str(n))
    encripted = encrypt_text(plaintext, n)
    print("Cipher Text is: " + encripted)
    print("Your decrypted message is: ", decrypt(encripted, n))

if __name__ == '__main__':
    main()