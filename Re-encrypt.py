import sys
import json
from pre_mg07b                  import PreGA
from charm.toolbox.pairinggroup import PairingGroup
from charm.toolbox.integergroup import IntegerGroup
from charm.core.engine.util     import objectToBytes,bytesToObject


IDFrom    = sys.argv[1]
IDTo      = sys.argv[2]
file_name = sys.argv[3]

'''Group set up'''
group = PairingGroup('SS512', secparam=1024)  
ibp = PreGA(group)
f = open('./setup/master.param', 'r')
bin_data = f.read()
params = bytesToObject(bin_data ,group)
f.close()
''' End set up'''

''' Load re-encryption key '''
f = open('./re-keys/' + IDFrom + ""+ IDTo+'.key', 'r')
bin_data          = f.readline()
rk_json           = json.loads( bin_data)
N                 = bytesToObject( rk_json['N'], IntegerGroup())
R                 = bytesToObject( rk_json['R'] ,group)       
re_encryption_key = {'N':N,'R':R}
f.close() 
''' End lre-encryption key '''

''' Load ciphertexts '''
f = open('./ciphertexts/' + IDFrom + file_name + '.enc', 'r')
bin_data = f.readline()
ct = json.loads( bin_data)
A  = bytesToObject( ct['CA'], group)
B  = bytesToObject( ct['CB'], group)
C  = bytesToObject( ct['CC'], IntegerGroup())
S  = bytesToObject( ct['S'] ,group)     
C_ = {'A':A, 'B':B, 'C':C}     
encr_key   = {'S':S,'C':C_} 
f.close()
''' End loading ciphertexts '''

''' Re-encrypt key and store file '''
encr_key_2 = ibp.reEncrypt(params, IDFrom, re_encryption_key, encr_key)
f = open('./ciphertexts/' + IDTo + file_name + '.enc', 'w')
ct_2 = { 
       'A'    : objectToBytes(encr_key_2['A'], group),
       'B'    : objectToBytes(encr_key_2['B'], group),
       'C'    : objectToBytes(encr_key_2['C'], IntegerGroup()),
       'N'    : objectToBytes(encr_key_2['N'], IntegerGroup()),
       'IDsrc': encr_key_2['IDsrc'],
       'Data' : ct['Data']
       }
f.write(json.dumps(ct_2))
f.close()


