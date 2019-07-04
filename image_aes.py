from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad, unpad

def encrypt(filename, key):
    '''
    encrypt
        encrypts a file with a key using CBC AES
    Parameters:
        filename: the name of the file to encrypt

        key: the key used for the file's AES encryption
    Returns:
        init_vector: the initialization vector used in the file's encryption
    '''
    AES_BLOCK_SIZE = 16

    aes_encryptor = AES.new(key, AES.MODE_CBC)
    init_vector = aes_encryptor.iv
    encrypted_file = "encrypted_" + filename

    with open(filename, 'rb') as infile:
        with open(encrypted_file, 'wb') as outfile:
            chunk = infile.read(AES_BLOCK_SIZE)
            while len(chunk) > 0:
                if len(chunk) % 16 == 0:
                    outfile.write(aes_encryptor.encrypt(chunk))
                else:
                    outfile.write(aes_encryptor.encrypt(pad(chunk, AES_BLOCK_SIZE)))
                
                chunk = infile.read(AES_BLOCK_SIZE)

    return init_vector


def decrypt(filename, key, init_vector):
    '''
    decrypt
        decrypts a file with a key and initialization vector using CBC AES
    Parameters:
        filename: the name of the file to decrypt

        key: the key used for the file's AES encryption

        init_vector: the initialization vector used it the file's encryption
    '''
    AES_BLOCK_SIZE = 16

    aes_decryptor = AES.new(key, AES.MODE_CBC, init_vector)
    decrypted_file = "new_" + filename[10:]

    with open(filename, 'rb') as infile:
        with open(decrypted_file, 'wb') as outfile:
            chunk = infile.read(AES_BLOCK_SIZE)
            while len(chunk) > 0:
                outfile.write(aes_decryptor.decrypt(chunk))
                chunk = infile.read(AES_BLOCK_SIZE)
            

def generate_key(key_text):
    '''
    generate_key
        returns the SHA256 hash of a key string
    Parameters:
        key_text: the key provided by the user
    Returns:
        the 32 byte SHA256 digest of key_text
    '''
    key_hash = SHA256.new(key_text.encode("utf8"))
    return key_hash.digest()

def load_init_vector(iv_file):
    '''
    load_init_vector
        loads an initialization vector from file
    Parameters:
        iv_file: the filename of the initialization vector
    Returns:
        init_vector: the intialization vector loaded from iv_file
    '''
    with open(iv_file, 'rb') as outfile:
        init_vector = outfile.read()

    return init_vector

def store_init_vector(filename, init_vector):
    '''
    store_init_vector
        saves an initialization vector to a file
    Parameters:
        filename: the filename of the original, unencrypted file

        init_vector: the initialization vector to save
    '''
    iv_file = "iv_" + filename

    with open(iv_file, 'wb') as outfile:
        outfile.write(init_vector)

def aes_main(user_choice, filename):
    if user_choice == "E" or user_choice == "e":
        key = input("Enter the password: ")
        key = generate_key(key)
        init_vector = encrypt(filename, key)
        store_init_vector(filename, init_vector)
    elif user_choice == "D" or user_choice == "d":
        key = input("Enter the password: ")
        key = generate_key(key)
        iv_file_name = "iv_" + filename[10:]
        init_vector = load_init_vector(iv_file_name)
        decrypt(filename, key, init_vector)

        return "new_" + filename[10:]
    else:
        print("Incorrect input. Exiting...")