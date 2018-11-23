from charm.toolbox.pairinggroup import PairingGroup
from pre_mg07b                  import PreGA
from charm.core.engine.util     import objectToBytes,bytesToObject

group = PairingGroup('SS512', secparam=1024) 
ibp = PreGA(group)
(master_secret_key, params) = ibp.setup()

f = open('./setup/master.key', 'w')
f.write( objectToBytes(master_secret_key, group))
f.close()
f = open('./setup/master.param', 'w')
f.write( objectToBytes( params, group))
f.close()

