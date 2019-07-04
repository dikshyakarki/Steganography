from image_encoder import encoder_main
from image_aes import aes_main

def main():
    user_choice = input("Enter 'S' to send or 'R' to receive: ")
    if user_choice == "S" or user_choice == "s":
        file_to_e = input("Enter the name of the image file: ")
        encoded_image = encoder_main("E", file_to_e)
        aes_main("E", encoded_image)
    elif user_choice == "R" or user_choice == "r":
        file_to_d = input("Enter the name of the encrypted file: ")
        decrypted_file = aes_main("D", file_to_d)
        encoder_main("D", decrypted_file)
    else:
        print("Incorrect input. Exiting...")

main()