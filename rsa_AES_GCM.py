import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from generar_claves import generar_par_claves


def encrypt_document(document: bytes, recipient_public_key_pem: bytes) -> bytes:
    # 1. Cifrar el documento con AES-256-GCM
    aes_key = os.urandom(32)
    cipher_aes = AES.new(aes_key, AES.MODE_GCM)
    ciphertext, tag = cipher_aes.encrypt_and_digest(document)
    nonce = cipher_aes.nonce
    # 2. Cifrar la clave AES con la clave pública RSA (OAEP)
    rsa_key = RSA.import_key(recipient_public_key_pem)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)

    return encrypted_aes_key + nonce + tag + ciphertext
    

def decrypt_document(pkg: bytes, recipient_private_key_pem: bytes) -> bytes:
    # 1. Extraer la clave AES cifrada, nonce, tag y ciphertext
    encrypted_aes_key = pkg[:256]  # RSA-2048 produce 256 bytes
    nonce = pkg[256:272]            # AES GCM nonce (16 bytes)
    tag = pkg[272:288]              # AES GCM tag (16 bytes)
    ciphertext = pkg[288:]          # Resto es el documento cifrado 
    # 2. Descifrar la clave AES con la clave privada RSA (OAEP)
    rsa_key = RSA.import_key(recipient_private_key_pem, passphrase="lab04uvg")
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    aes_key = cipher_rsa.decrypt(encrypted_aes_key)
    # 3. Descifrar el documento con AES-256-GCM
    cipher_aes = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    document = cipher_aes.decrypt_and_verify(ciphertext, tag)
    return document

if __name__ == '__main__':
    generar_par_claves(2048)

    with open("public_key.pem", "rb") as f: pub = f.read()
    with open("private_key.pem", "rb") as f: priv = f.read()

    # Generen un cifrado de un texto
    doc = b"Contrato de confidencialidad No. 2025-GT-001"
    pkg = encrypt_document(doc, pub)
    resultado = decrypt_document(pkg, priv)


    # Prueba con archivo de 1 MB (simula un contrato real)
    doc_grande = os.urandom(1024 * 1024)
    pkg2 = encrypt_document(doc_grande, pub)
    assert decrypt_document(pkg2, priv) == doc_grande
    print("Archivo 1 MB: OK")
