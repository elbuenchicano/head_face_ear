'''
Configurations of these functions are in the ####_confs.json
'''
####################################################################################################
###################### Imports #####################################################################
from    utils                   import *
from    CoxSetup                import *
from    HeadDet                 import *

####################################################################################################
####################################################################################################
####################################### Main functions #############################################
#### Organize cox files ############################################################################
####
def initCox(confs): 
    dir         = confs['prefix_path'][u_whichOS()] + '/' + confs['directory']
    db_confs    = confs['cox']

    organizeCox(db_confs, dir)
    
#### Head detection ################################################################################   
#### 
def headDetection(confs):
    dir         = confs['prefix_path'][u_whichOS()] + '/' + confs['directory']
    cox_if_pt   = dir + '/cox/cox_info.json'
    cox_if      = u_loadJson(cox_if_pt)

    yoloHeadDet(cox_if, dir)

    u_saveDict2File(cox_if_pt, cox_if)

    

    




