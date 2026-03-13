from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def cifrar_con_rsa(mensaje: bytes, public_key_pem: bytes) -> bytes:
    key = RSA.import_key(public_key_pem)
    cipher = PKCS1_OAEP.new(key)
    cifrado = cipher.encrypt(mensaje)
    return cifrado

def descifrar_con_rsa(cifrado: bytes, private_key_pem: bytes) -> bytes:
    key = RSA.import_key(private_key_pem, passphrase="lab04uvg")
    cipher = PKCS1_OAEP.new(key)
    descifrado = cipher.decrypt(cifrado)
    return descifrado

if __name__ == '__main__':
    # Cargar claves generadas en el ejercicio anterior
    with open("public_key.pem", "rb") as f:
        pub = f.read()
    with open("private_key.pem", "rb") as f:
        priv = f.read()

    mensaje_original = b"El mensaje sera la clave secreta de AES"
    cifrado   = cifrar_con_rsa(mensaje_original, pub)
    descifrado = descifrar_con_rsa(cifrado, priv)

    print(f"Original  : {mensaje_original}")
    print(f"Cifrado   : {cifrado.hex()[:64]}...")  # primeros 64 chars hex
    print(f"Descifrado: {descifrado}")


    # Pregunta: ¿Por qué cifrar el mismo mensaje dos veces produce
    # resultados distintos? Demuéstralo y explica qué propiedad de OAEP lo causa.
    c1 = cifrar_con_rsa(mensaje_original, pub)
    print("Cifrado 1: ", c1.hex()[:64], "...")  # primeros 64 chars hex
    c2 = cifrar_con_rsa(mensaje_original, pub)
    print("Cifrado 2: ", c2.hex()[:64], "...")  # primeros 64 chars hex
    print(f"\nc1 == c2: {c1 == c2}")   # Esperado: False