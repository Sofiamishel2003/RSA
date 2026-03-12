from Crypto.PublicKey import RSA

def generar_par_claves(bits: int = 3072):
    key = RSA.generate(bits)
    private_key = key.export_key(
        format="PEM",
        passphrase="lab04uvg"
    )
    public_key = key.publickey().export_key()

    # Guardar las claves en archivos
    with open("private_key.pem", "wb") as f:
        f.write(private_key)

    with open("public_key.pem", "wb") as f:
        f.write(public_key)

if __name__ == '__main__':
    generar_par_claves(3072)
    print("Claves generadas: private_key.pem y public_key.pem")