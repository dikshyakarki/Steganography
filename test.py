from image_aes import *
from image_encoder import *

encoder = ImageEncoder("Half-Moon.png")
encoder.encode("The secret message is secret")
encoder.save_image("Half-Moon-2.png")
hashkey = generate_key("secret password")
initVector = encrypt("Half-Moon-2.png", hashkey)
store_init_vector("Half-Moon-2.png", initVector)

key = generate_key("secret password")
init_vector = load_init_vector("iv_Half-Moon-2.png")
decrypt("encrypted_Half-Moon-2.png", key, init_vector)
print(decode("new_Half-Moon-2.png"))