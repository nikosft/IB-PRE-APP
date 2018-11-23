IB-PRE-APP
===========
# About
A file encryption application based on the Identity-based proxy re-encryption scheme published in:<br/>

> M. Green, G. Ateniese, "Identity-Based Proxy Re-Encryption," in Applied Cryptography and Network Security. Springer Berlin/Heidelberg, 2007<br/>

Available at: http://link.springer.com/chapter/10.1007%2F978-3-540-72738-5_19

In order to use this class install Charm-Crypto library (http://charm-crypto.com/)

## Usage
### Setup
The Setup process is executed only once and it generates the master secret key and
the system parameters. Setup is executed as follows

> python Setup.py

### User key generation
It is assumed that each user is identified by an email address. The secret key
that corresponds to a user identity is generated using the Extrat process. For example:

> python Extract.py fotiou@example.com

### File encryption
A file is encrypted using a user identifier as the (public) key. File encryption is
done using the Encrypt.py and by supplying the user identifier and the filename.\
For example:

> python Encrypt.py fotiou@example.com Hello_world.txt

### File decryption
The file encrypted using the previos process is decrypted using the Decrypt script.
The scipt requires as input the user name and the file name used during the ecnryption process.
The decrypted file is outputed to the "plaintexts" folder. Usage example:

> python Decrypt.py fotiou@example.com Hello_world.txt

### Re-encryption key generation
A re-encryption key is used for re-encrypting a ciphertext generated using an identifier
A such that it can be decrypted using the private key that corresponds to an 
identifier B. An example of a re-encryption key generation follows.

> python Re-keygen.py fotiou@example.com fotiou-mobile@example.com

### File Re-encryption
An encrypted file can be re-encrypted using a re-encryption key. For example:

> python Re-encrypt.py fotiou@example.com fotiou-mobile@example.com Hello_world.txt

### Decryption of a re-encrypted file
A re-encrypted file is decrypted using the Re-decrypt script and the identifier used
for the re-encryption process. For example:

> python Re-decrypt.py fotiou-mobile@example.com Hello_world.txt 
