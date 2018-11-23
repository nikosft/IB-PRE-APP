import sys
import json
from charm.toolbox.pairinggroup import PairingGroup
from charm.toolbox.integergroup import IntegerGroup
from pre_mg07b                  import PreGA
from charm.core.engine.util     import objectToBytes,bytesToObject
from charm.toolbox.symcrypto    import AuthenticatedCryptoAbstraction
from charm.toolbox.securerandom import OpenSSLRand

ID        = sys.argv[1]
file_name = sys.argv[2]

'''Group set up'''
group = PairingGroup('SS512', secparam=1024)  
ibp = PreGA(group)
f = open('./setup/master.param', 'r')
bin_data = f.read()
params = bytesToObject(bin_data ,group)
f.close()
''' End set up'''

'''Symmetric encryption key and algorithm set up'''
sym_key = OpenSSLRand().getRandomBytes(16)
sym_cipher = AuthenticatedCryptoAbstraction(sym_key)
'''End set up'''

'''Encryption proccess'''
sym_key_ciphertext = ibp.encrypt(params, ID, sym_key); # encrypt the symmetric encryption key
f = open(file_name, 'r')
file_data = f.read()
file_ciphertext = sym_cipher.encrypt(file_data)
'''End of encryption process'''

ct = { 'CA'  : objectToBytes(sym_key_ciphertext['C']['A'], group),
       'CB'  : objectToBytes(sym_key_ciphertext['C']['B'], group),
       'CC'  : objectToBytes(sym_key_ciphertext['C']['C'], IntegerGroup()),
       'S'   : objectToBytes(sym_key_ciphertext['S'], group),
       'Data': file_ciphertext
       }
f = open('./ciphertexts/' + ID + file_name + '.enc', 'w')
f.write(json.dumps(ct))
f.close()


