import  json
import  time
from    utils           import u_sec2dhms, u_loadJson
from    control         import *


############################### MAIN ##############################################################
def main():
    
    funcdict    = { 'initCox'       : initCox, 
                    'headDetection' : headDetection,
                    'faceDetection' : faceDetection
                   }
    
    print('_______________________________________')
    confs = u_loadJson('./general_confs.json')
    print('Function: ' + confs['function'])
    

    start = time.time()
    
    funcdict[confs['function']](confs)
    
    done = time.time()
    elapsed = u_sec2dhms(done - start)
    print(f'Tiempo total : {elapsed}')     
            
###################################################################################################
if __name__ == '__main__':
    main()
