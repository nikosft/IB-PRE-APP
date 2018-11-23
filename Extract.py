import sys
from charm.toolbox.pairinggroup import PairingGroup
from pre_mg07b                  import PreGA
from charm.core.engine.util     import objectToBytes,bytesToObject

ID = sys.argv[1]
group = PairingGroup('SS512', secparam=1024)  
ibp = PreGA(group)
f = open('./setup/master.key', 'r')
bin_data = f.read()
master_secret_key = bytesToObject( bin_data ,group)
f.close()
f = open('./setup/master.param', 'r')
bin_data = f.read()
params = bytesToObject(bin_data ,group)
f.close()
id_secret_key = ibp.keyGen(master_secret_key, ID)
f = open('./userkeys/' + ID + '.key', 'w')
f.write( objectToBytes( id_secret_key, group))
f.close()

