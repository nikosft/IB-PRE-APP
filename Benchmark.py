import sys
import json
from charm.toolbox.pairinggroup import PairingGroup
from charm.toolbox.integergroup import IntegerGroup
from pre_mg07b                  import PreGA
from charm.core.engine.util     import objectToBytes,bytesToObject
from charm.toolbox.symcrypto    import AuthenticatedCryptoAbstraction
from charm.toolbox.securerandom import OpenSSLRand

ID        = sys.argv[1]
msg       = sys.argv[2]

'''Group set up'''
group = PairingGroup('SS512', secparam=1024)  
ibp = PreGA(group)
f = open('./setup/master.param', 'r')
bin_data = f.read()
params = bytesToObject(bin_data ,group)
f.close()
''' End set up'''

''' Load user key'''
f = open('./userkeys/' + ID + '.key', 'r')
bin_data = f.read()
id_secret_key = bytesToObject( bin_data ,group)
f.close()
''' End loading user key '''

'''Symmetric encryption key and algorithm set up'''
sym_key = OpenSSLRand().getRandomBytes(16)
sym_cipher = AuthenticatedCryptoAbstraction(sym_key)
'''End set up'''

'''Encryption proccess'''
assert group.InitBenchmark(), "failed to initialize benchmark"
group.StartBenchmark(["RealTime", "CpuTime"])
sym_key_ciphertext = ibp.encrypt(params, ID, sym_key); # encrypt the symmetric encryption key
msg_ciphertext = sym_cipher.encrypt(msg)
group.EndBenchmark()

msmtDict = group.GetGeneralBenchmarks()
print("=== Encryption Benchmarks ===")
print("RealTime := ", msmtDict["RealTime"])
print("CpuTime := ", msmtDict["CpuTime"])
'''End of encryption process'''

''' Message descyption process '''
assert group.InitBenchmark(), "failed to initialize benchmark"
group.StartBenchmark(["RealTime", "CpuTime"])
sym_dec_key = ibp.decryptFirstLevel(params,id_secret_key, sym_key_ciphertext, ID )
sym_cipher = AuthenticatedCryptoAbstraction(sym_dec_key)
msg_decrypted = sym_cipher.decrypt(msg_ciphertext)
group.EndBenchmark()

msmtDict = group.GetGeneralBenchmarks()
print("=== Decryption Benchmarks ===")
print("RealTime := ", msmtDict["RealTime"])
print("CpuTime := ", msmtDict["CpuTime"])
print msg_decrypted
'''End of decryption process'''
