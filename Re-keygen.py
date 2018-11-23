import sys
import json
from pre_mg07b                  import PreGA
from charm.toolbox.pairinggroup import PairingGroup
from charm.toolbox.integergroup import IntegerGroup
from charm.core.engine.util     import objectToBytes,bytesToObject


IDFrom = sys.argv[1]
IDTo = sys.argv[2]
group = PairingGroup('SS512', secparam=1024)
ibp = PreGA(group)
f = open('./setup/master.param', 'r')
bin_data = f.read()
params = bytesToObject(bin_data ,group)
f = open('./userkeys/'+IDFrom+'.key', 'r')
bin_data = f.read()
id_secret_key = bytesToObject( bin_data ,group)
f.close()
f = open('./setup/master.param', 'r')
bin_data = f.read()
params = bytesToObject(bin_data ,group)
f.close()
re_encryption_key = ibp.rkGen(params,id_secret_key, IDFrom, IDTo)
rk_json = { 
           'N'  : objectToBytes(re_encryption_key['N'], IntegerGroup()),
           'R'  : objectToBytes(re_encryption_key['R'], group),
           }
f = open('./re-keys/' + IDFrom + ""+ IDTo+'.key', 'w')
f.write(json.dumps(rk_json))
f.close()

