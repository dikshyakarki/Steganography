# *Steganography*

Steganography is an encryption technique of embedding the messages in non-secret mediums such as graphics, sound, text, or HTML. One of the widely used steganographic technique is watermarking to protect copyrighted materials. The message that one wishes to send is hidden in a plain and harmless media referred to as a cover medium which might be text, image, audio or videos files that produce a stego-object. The cover medium is chosen keeping in mind the type and size of the secret message. Then, a key is used to control the the hiding process by restricting the detection and the recovery. The steganography equation is equal to the cover medium plus the secret message plus the key. 

We have implemented image steganography technique using least significant bit steganography. A colour pixel is composed of three values representing the red, green and blue compositions of the pixel, also known as RGB values. A change in any of the least significant bits for the values would be indistinguishable to the human eye as it’s only a change in value of one. So to hide characters in the image, a character is encoded into binary using ASCII values and then the least significant bits of each pixel are changed to reflect the ASCII values’ bits. Since ASCII values are represented by 8 bits (one byte), three pixels (nine least significant bits) would have to be used to store one ASCII character, with one bit to spare. We need to store the necessary information in the bits of RGB values. The program can hide all the data if it has enough space. An image could potentially store up to its height times its width integer divided by three. But, the more data we store in the file, the more it could be detected.

# Documentation
Docstrings for each function and method are provided in the code.

image_encoder.py: Handles the encoding and decoding of messages to an image using steganography.

image_aes.py: Handles the encrypting and decrypting of files using AES.

main.py: The main function to run that interfaces between the above files. It should be used for both encoding/encrypting and decoding/decrypting a file; either set of processes is specified at runtime.

ImageEncoder: A class to load, encode and save an image file using random spacing of the set of 3 pixels needed to encode a character. The class is instantiated by passing it an image filename. To encode the file, .encode() is run on the instantiated object. An image can be reset with .reset_image(), and once finished, the file is saved with .save_image(), passing the function a filename to save to.

encode(): Encodes the data passed to the function into the image using LSB steganography. If the encoding was successful, True is returned. False is returned if the data passed was too large to be stored in the image or if the image is currently encoded with data. 

save_image(): Saves the encoded image with the passed filename in a .png file format. On success True is returned, otherwise False is returned.

decode(): Non-class function that searches through an image sequentially pixel by pixel, attempting to decode each pixel’s LSB information into characters. The decoded message is returned.

encrypt(): Pass the name of the file to encrypt and the password. It saves a new encrypted file with the name “encrypted_” plus the original file name. The randomly generated initialization vector used to encrypt the file is returned.

decrypt(): Pass the name of the file to decrypt, the password, and the initialization vector used for the encryption of the file. It saves the decrypted file with the name “new_” plus the original file name.

# Algorithm/ Approach

For a single character to be stored in an image using least significant bit steganography, three pixels are needed. Each pixel contains three least significant bits (one for each of the R, G, and B values of the pixel), and with three pixels this brings us to nine total least significant bits: eight to store a character’s value as a byte, and one extra. In order to store the message within the image fairly randomly so that steganalysis would be less successful on decoding the messages. This randomness is being added by using the leftover bit in a pixel set (a set of three pixels storing a character value) to signify the start of a pixel set with a character stored within and adding random lengths of space between pixel sets. If a pixel is not apart of a pixel set, the least significant bit in its R value is set to 0. 

If a pixel begins a pixel set, the least significant bit in its R value is set to 1. For a given image, the maximum number of characters that can be stored in the image is the integer division of the number of pixels in the image by three. For small messages, this leaves a lot of extra room in the image. So the unused number of pixels are divided by the number of characters in the message that is to be stored, giving the max number of characters that could appear in between pixel sets. A random number is generated between zero and this max, and this random number (minus three) is used for the index of where to place the next pixel set. The pixels in an image are looped through sequentially column by row until all characters in the message are stored. The remaining pixels in the image also have the least significant bit in their R values set to zero.

When decoding the image, the pixels are looped through sequentially column by row, checking each pixel’s R value’s least significant bit. If the value is zero, the pixel is ignored. But if the value is 1, the next two pixels after the current pixel are selected for a pixel set to decode. The least significant bits are fetched from all of the pixels (minus the first), the value computed, and the character of that value added to the decoded message. This process continues until every pixel is read from the image. Reading and writing both images and pixels was done through python’s Pillow package, an expanded fork of PIL (Python Imaging Library).

Encryption and decryption was done using cipher block chaining AES. The key is provided by the user, extended or cropped to 16 characters, and the initialization vector is randomly generated. The initialization vector used during encryption is also saved to a file so that the encrypted file can be decrypted properly later with the same initialization vector. AES was implemented using a python package called PyCryptodome, a drop-in replacement for the outdated PyCrypto package. 

The main.py file is run whether sending the file or receiving the file. If sending the image, the program asks for a filename of the image, the message to store, and the password for aes encryption. If receiving, the program asks for the filename of the encrypted file, the password, and then outputs the message it has decoded from the image.
