import  os
import  torch
import  matplotlib.pyplot   as      plt
import  pandas              as      pd       


from    torch.utils.data    import  Dataset
from    utils               import  *
from    plot_utils          import  *
from    tqdm                import  tqdm

####################################################################################################
####################################################################################################
####################################################################################################
#######Cox dataset organizer########################################################################

def still(item_list, ids_int_pt, st_pt):
    '''
    item list is u_filelist2dic2 format, ids2int path, still file path
    '''
    ids_int     = {}
    still_files = item_list['still']['_files']
    still_pt    = item_list['still']['_path']

    ids         = []
    pts         = []
    
    for it, pt in enumerate(still_files):
        id          = pt[:12]
        ids_int[id] = it
        ids.append(it)
        pts.append(still_pt +'/'+ pt)
    
    #..............................................................................................
    
    df = pd.DataFrame({'id':ids, 'pt_file':pts})
    df.to_json(st_pt) 
    u_saveDict2File(ids_int_pt, ids_int)
    return ids_int

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
def cameras(item_list, db_pt, ids_int, c_pts):
    '''
    item list is u_filelist2dic2 format, ids2int path, still file path
    '''
    for i, camera_pt in enumerate(c_pts):
        cam     = 'cam' + str(i+1) 
        ids     = []
        pts     = []
        
        for id in ids_int:
            for file in item_list['video'][cam][id]['_files']:
                path    = item_list['video'][cam][id]['_path']
        
                ids.append(ids_int[id])
                pts.append(path + '/'+ file)

            print(f'camera: {i+1}, id: {ids_int[id]}')

        df = pd.DataFrame({ 'id':ids, 'pt_file':pts })
        print(f'Saving file: {camera_pt}')
        df.to_json(camera_pt) 
        

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
def organizeCox(db_confs, outdir):
    '''
    The idea is to have separated files for any feature but pointing to the same id or pos in table
    db_pts is the locations in os's outdir is the output directory
    '''
    local_pt    = outdir + '/cox'
    db_pt       = db_confs['db_pts'][u_whichOS()]
    
    #### main paths ...............................................................................
    conf_pt         = '/cox_info.json'   
    item_pt         = '/item_list.json'   
    ids_int_pt      = '/ids_int.json' 
    st_pt           = '/st.json'  
    c1_pt           = '/c1.json'  
    c2_pt           = '/c2.json'  
    c3_pt           = '/c3.json'  

    #### creating output directory ................................................................
    u_mkdir(local_pt)

    #### loading cox information ..................................................................
    if not os.path.isfile(local_pt + item_pt):
        item_list   = u_listFileAllDic_2(db_pt, '', 'jpg')
        u_saveDict2File(local_pt + item_pt, local_pt + item_list)

    item_list   = u_loadJson(local_pt + item_pt)

    #### building still and camera info ...........................................................
    ids_int = still(item_list, local_pt + ids_int_pt, local_pt + st_pt)
    cameras(item_list, db_pt, ids_int, [local_pt + i for i in [c1_pt, c2_pt, c3_pt]] )

    #### saving path info .........................................................................

    confs = {}
        
    confs['item_pt'     ] = item_pt
    confs['ids_int_pt'  ] = ids_int_pt
    confs['st_pt'       ] = st_pt
    confs['c1_pt'       ] = c1_pt
    confs['c2_pt'       ] = c2_pt
    confs['c3_pt'       ] = c3_pt
    confs['db_pts'      ] = db_confs['db_pts']
    
    u_saveDict2File(local_pt + conf_pt, confs)

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
def testOrganization ():
    pts         = u_loadJson("I:/research/Head_face_ear/cox/cox_info.json")
    local_pt    = 'I:/research/Head_face_ear/cox'
    c3  = pd.read_json(local_pt+ pts['c3_pt']) 

    


