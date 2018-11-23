import sys
import json
from charm.toolbox.pairinggroup import PairingGroup, GT
from pre_mg07b                  import PreGA
from charm.toolbox.integergroup import IntegerGroup
from charm.core.engine.util     import objectToBytes,bytesToObject
from charm.toolbox.symcrypto    import AuthenticatedCryptoAbstraction

ID        = sys.argv[1]
file_name = sys.argv[2]

'''Group set up'''
group = PairingGroup('SS512', secparam=1024)
ibp = PreGA(group)
f = open('./setup/master.param', 'r')
bin_data = f.read()
params = bytesToObject(bin_data ,group)
''' End set up'''

''' Load user key'''
f = open('./userkeys/' + ID + '.key', 'r')
bin_data = f.read()
id_secret_key = bytesToObject( bin_data ,group)
f.close()
''' End loading user key '''

''' Load ciphertexts '''
f = open('./ciphertexts/' + ID + file_name + '.enc', 'r')
bin_data = f.readline()
ct = json.loads( bin_data)
A  = bytesToObject( ct['CA'], group)
B  = bytesToObject( ct['CB'], group)
C  = bytesToObject( ct['CC'], IntegerGroup())
S  = bytesToObject( ct['S'] ,group)     
C_ = {'A':A, 'B':B, 'C':C}     
encr_key   = {'S':S,'C':C_} 
ciphertext =  ct['Data']
f.close()
''' End loading ciphertexts '''


'''Symmetric encryption key and algorithm set up'''
sym_key = ibp.decryptFirstLevel(params,id_secret_key, encr_key, ID)
sym_cipher = AuthenticatedCryptoAbstraction(sym_key)
'''End set up'''

''' File decyption process '''
file_decrypted = sym_cipher.decrypt(ciphertext)
f = open('./plaintexts/' + file_name, 'w')
f.write( file_decrypted)
f.close()
