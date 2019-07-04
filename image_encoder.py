from PIL import Image
import random
import sys


'''
ImageEncoder
    a class to load, encode, and save an image file using random spacing of 
    the set of 3 pixels needed to encode a character
Attributes:
    filename: the filename of the image to encode
'''
class ImageEncoder:
    def __init__( self, filename ):
        self.image_file = filename

        try:
            self.original_image = Image.open( self.image_file )
        except:
            print("File could not be opened.")
            sys.exit(1)

        self.image_format = self.original_image.format

        self.encoded_image = self.original_image.copy()
        self.pixel_matrix = self.encoded_image.load()

        self.image_width = self.encoded_image.size[0]
        self.image_height = self.encoded_image.size[1]
        self.pixel_num = self.image_width * self.image_height

        self.stored_data = ""
        self.encoded = False

    def encode( self, data ):
        '''
        encode
            encodes the data passed to the image using least significant 
            bit steganography
        Parameters:
            data: a string of characters to hide within the image
        Returns:
            True: on success
            False: if the image has already been encoded or if the data
            string is too long to be stored in the image
        '''
        NUM_PIXELS_FOR_CHAR = 3

        if self.encoded:
            print( "Image has already been encoded with data." )
            return False

        if len(data) * NUM_PIXELS_FOR_CHAR > self.pixel_num:
            print( "Size of input is too large for image to store." )
            return False

        self.stored_data = data

        pixels_used = len( data ) * NUM_PIXELS_FOR_CHAR
        max_index = ( ( self.pixel_num - pixels_used ) // pixels_used )
        section_size = max_index + NUM_PIXELS_FOR_CHAR

        current_col = 0
        current_row = 0

        for i in range( len( data ) ):
            random_index = random.randint( 0, max_index )
            
            for j in range( random_index ):
                self.pixel_matrix[current_col, current_row] = self.zero_pixel( self.pixel_matrix[current_col, current_row] )
                current_col += 1
                if current_col >= self.image_width:
                    current_col = 0
                    current_row += 1

            pixel_set = []
            pixel_set_coordinates = []
            for j in range( NUM_PIXELS_FOR_CHAR ):
                pixel_set.append( self.pixel_matrix[current_col, current_row] )
                pixel_set_coordinates.append( ( current_col, current_row ) )
                current_col += 1
                if current_col >= self.image_width:
                    current_col = 0
                    current_row += 1

            new_pixel_set = self.store_char( data[0], pixel_set )
            data = data[1:]

            for new_pixel in new_pixel_set:
                self.pixel_matrix[pixel_set_coordinates[0][0], pixel_set_coordinates[0][1]] = new_pixel
                pixel_set_coordinates = pixel_set_coordinates[1:]

            for j in range( section_size - ( random_index + NUM_PIXELS_FOR_CHAR ) ):
                self.pixel_matrix[current_col, current_row] = self.zero_pixel( self.pixel_matrix[current_col, current_row] )
                current_col += 1
                if current_col >= self.image_width:
                    current_col = 0
                    current_row += 1

        while current_col < self.image_width and current_row < self.image_height:
            self.pixel_matrix[current_col, current_row] = self.zero_pixel( self.pixel_matrix[current_col, current_row] )
            current_col += 1
            if current_col >= self.image_width:
                current_col = 0
                current_row += 1

        self.encoded = True

        return True

    def reset_image( self ):
        '''
        reset_image
            resets the encoded image back to the original image
        '''
        self.encoded_image = self.original_image.copy()
        self.encoded = False

    @staticmethod
    def bin_to_pixel( bin_pixel ):
        '''
        bin_to_pixel
            converts a tuple with three binary values into a tuple containing
            the integer representations of those values
        Parameters:
            bin_pixel: a tuple with three binary values
        Returns
            a tuple with the binary values converted to integers
        '''
        return ( int( bin_pixel[0], 2 ), int( bin_pixel[1], 2 ), int( bin_pixel[2], 2 ) )

    def zero_pixel( self, pixel ):
        '''
        zero_pixel
            sets the least significant bit of the first value in the pixel
            tuple to zero
        Parameters:
            pixel: the pixel tuple to zero the first value for
        Returns:
            zeroed_pixel: the zeroed pixel tuple
        '''
        bin_pixel = self.pixel_to_bin( pixel )
        zeroed_position = str(bin_pixel[0][:-1]) + "0"
        zeroed_pixel = ( zeroed_position, bin_pixel[1], bin_pixel[2] )
        zeroed_pixel = self.bin_to_pixel( zeroed_pixel )
        return zeroed_pixel

    @staticmethod
    def pixel_to_bin( rgb_tuple ):
        '''
        pixel_to_bin
            converts a tuple with three integer values into a tuple containing
            the binary representations of those values
        Parameters:
            rgb_tuple: a pixel tuple of three integers 0-255
        Returns:
            a tuple with the integer values converted to binary
        '''
        return ( "{0:08b}".format( rgb_tuple[0] ) , "{0:08b}".format( rgb_tuple[1] ), "{0:08b}".format( rgb_tuple[2] ) )

    def store_char( self, char, pixel_list ):
        '''
        store_char
            stores a single character into a set of three pixels, setting the
            first of the nine least significant bits to 1 to designate the 
            start of an encoded pixel block
        Parameters:
            char: the single character to store in the pixel set

            pixel_list: a list containing three pixel tuples to store the 
            character in
        Returns:
            new_pixel_list: a list containing the three pixel tuples encoded
            with the character in their least significant bits
        '''
        char_value = ord( char )
        char_bin = "{0:08b}".format( char_value )

        bin_pixel_list = []
        for pixel in pixel_list:
            bin_pixel_list.append( self.pixel_to_bin( pixel ) )

        new_pixel_list = []

        first_bin_val = True
        for pixel in bin_pixel_list:
            new_bin_values = []
            for bin_val in pixel:
                if not first_bin_val:
                    new_bin_values.append( bin_val[:-1] + char_bin[0] )
                    char_bin = char_bin[1:]
                else:
                    new_bin_values.append( str(bin_val[:-1]) + "1" )
                    first_bin_val = False
            new_pixel_list.append( tuple( new_bin_values ) )

        for i in range( len( new_pixel_list ) ):
            new_pixel_list[i] = self.bin_to_pixel( new_pixel_list[i] )

        return new_pixel_list

    def save_image( self, filename ):
        '''
        save_image
            saves the encoded image to a file using the passed filename and
            png format
        Parameters:
            filename: the new image filename as a string, without the .format 
            on the end
        Returns:
            True: on success

            False: if the image could not be saved
        '''
        try:
            self.encoded_image.save( filename, "png" )
            return True
        except:
            print( "Incorrect filename or format specified." )
            return False

def decode( filename ):
    '''
    decode
        searches through an image, attempting to decode each pixel's least 
        significant bit information into characters
    Parameters:
        filename: the filename of the image to extract data from
    Returns:
        decoded_text: a string of characters decoded from the image
    '''
    image_to_decode = Image.open( filename )
    pixel_matrix = image_to_decode.load()
    decoded_text = ""

    pixel_set = []
    in_pixel_set = False
    for i in range( image_to_decode.size[1] ):
        for j in range( image_to_decode.size[0] ):
            current_pixel = pixel_matrix[j, i]
            binary_pixel = ImageEncoder.pixel_to_bin( current_pixel )

            if in_pixel_set:
                pixel_set.append( binary_pixel )
            elif binary_pixel[0][-1] == "0":
                continue
            else:
                in_pixel_set = True
                pixel_set.append( binary_pixel )

            if len(pixel_set) > 2:
                in_pixel_set = False
                decoded_text += pixels_to_char( pixel_set) 
                pixel_set = []

    return decoded_text

def pixels_to_char( pixel_set ):
    '''
    pixels_to_char
        converts a list of three pixels with binary values into a character
    Parameters:
        pixel_set: a list of three pixel tuples with values as binary strings
    Returns:
        converted_char: a single character decoded from the pixel set
    '''
    PIXEL_SET_LENGTH = 3

    bin_string = ""
    for pixel in pixel_set:
        for i in range( PIXEL_SET_LENGTH ):
            bin_string += pixel[i][-1]

    bin_string = bin_string[1:]
    char_value = int( bin_string, 2 )

    converted_char = chr( char_value )
    return converted_char

def encoder_main(user_choice, filename):
    if user_choice == "E" or user_choice == "e":
        encoder = ImageEncoder(filename)
        message = input("Enter the message to hide: ")
        encoder.encode(message)
        encoded_file_name = "encoded_" + filename
        encoder.save_image(encoded_file_name)

        return encoded_file_name
    elif user_choice == "D" or user_choice == "d":
        hidden_text = decode(filename)
        print(hidden_text)
    else:
        print("Incorrect input. Exiting...")