## Ejercicio RSA — Cifrado Híbrido RSA + AES-GCM

* **RSA-OAEP** para cifrado asimétrico
* **AES-256-GCM** para cifrado simétrico autenticado

Se demuestra cómo funcionan los sistemas de cifrado híbrido usados en protocolos como **TLS, SSH y certificados X.509**.

---

# Estructura del proyecto

```
generar_claves.py
rsa_OAEP.py
rsa_AES_GCM.py

public_key.pem (para generarla correr generar_claves)
private_key.pem (para generarla correr generar_claves)
README.md
```

---

# Requisitos

Instalar dependencia:

```bash
pip install pycryptodome
```

---

# Generación de claves RSA

Ejecutar:

```bash
python generar_claves.py
```

Se generan:

```
private_key.pem
public_key.pem
```

La clave privada se guarda protegida con passphrase **"lab04uvg"**.

---

# Cifrado RSA-OAEP

Ejecutar:

```bash
python rsa_OAEP.py
```

Esto:

1. cifra un mensaje con la clave pública
2. lo descifra con la clave privada
3. demuestra que cifrar dos veces produce resultados distintos.

---

# Cifrado híbrido RSA + AES

Ejecutar:

```bash
python rsa_AES_GCM.py
```

Proceso:

```
Documento
 ↓
AES-256-GCM cifra el documento
 ↓
RSA-OAEP cifra la clave AES
```

El sistema permite cifrar documentos grandes (ejemplo de **1MB**).

---

# Respuestas a las preguntas

## ¿Por qué no cifrar documentos directamente con RSA?
Porque el RSA tiene un alto costo computacional para su generación de llaves, entonces lo que se hace usualmente es combinarlo con otros algoritmos para mayor seguridad y viabilidad. Entonces por eso usamos el RSA que protege la clave (porque abarca el tema de autenticación) y luego con AES ciframos el documento.

---

## ¿Qué contiene un archivo .pem?

Cuando se abre el archivo pem, de la clave privada tiene cómo este formato:
```
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-EDE3-CBC,DAAF6BED13DA8E35
kqhkiG9 Blablabla clave kqhkiG9
-----END RSA PRIVATE KEY-----
```

entonces, nos da 2 headers en la seccion de private key, que es el Proc-Type que nos indica que el archivo está cifrado y que tiene una clave. Y DEK-Info que nos da el algoritmo de cómo fue cifrado, en el ejemplo anterior nos dice que es triple DES en modo CBC, después procede a llevar la clave y termina con el END RSA.
En cambio el .pem del público es algo asi:
```
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A...
-----END PUBLIC KEY-----
```
La clave pública incluye principalmente:

* módulo RSA (n)
* exponente público (e)

---

## ¿Por qué cifrar el mismo mensaje dos veces produce resultados distintos?

Porque para generarla tiene aleatoreidad por el algoritmo de pareidad. RSA-OAEP usa **padding probabilístico** que introduce aleatoriedad antes del cifrado.

Esto significa que:

```
encrypt(mensaje) ≠ encrypt(mensaje)
```

aunque el mensaje sea el mismo.