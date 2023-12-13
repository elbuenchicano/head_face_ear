####################################################################################################
####################################################################################################
###### imports

#from    PIL                 import Image
from    tqdm                import tqdm
from    utils               import *
from    torchvision.io      import  read_image

import  torch
import  shutil
import  os 
import  yaml
import  pandas              as      pd 
import  matplotlib.pyplot   as      plt
import  matplotlib.patches  as      patches
from    facenet_pytorch     import  MTCNN, InceptionResnetV1



####################################################################################################
####### Face detection using mtcnn##################################################################
# this funciont is just to confire the bbox info


def coxface(info, local_pt, model):
    '''
    This function extracts heads for cox partitions, info contains the paths for pandas df
    '''
    names = ['st_', 'c1_', 'c2_', 'c3_']
    #names = ['c1_']
    db_pt = info['db_pts'][u_whichOS()]

    ### for each view .............................................................................
    for name in names:
        view    = pd.read_json(local_pt + info[name + 'pt']).to_numpy()
        head    = pd.read_json(local_pt + info[name + 'head_pt']).to_numpy()

        bbox    = []
        probs   = []

        #view = view[5196:]
        #head = head[5196:]

        for (_, pt), (head_prop, bb)  in tqdm(zip(view, head), name):
            
            if head_prop:
                im_pt   = db_pt + pt
                im      = read_image(im_pt)
                im      = np.transpose(im, (1,2,0))
                hd      = im[bb[1]:bb[3], bb[0]:bb[2]]

                try:
                    bb, pb  = model.detect(hd)#landmarks=True
            
                    if pb[0] != None:
                        pb  = np.around(pb[0], 2)
                        bb  = np.rint(bb[0].tolist()).astype(int)
                        # x = hd[bb[1]:bb[3],bb[0]:bb[2]] just to show    

                        probs.append(pb)
                        bbox.append(bb)

                    else :
                        probs.append(0)
                        bbox.append([0,0,0,0])

                except:

                    probs.append(0)
                    bbox.append([0,0,0,0])

            else :
                probs.append(0)
                bbox.append([0,0,0,0])

            #break


        #..........................................................................................
        # saving view data on pandas json        
        df      = pd.DataFrame({'prob':probs, 'bbox':bbox})
        view_pt = f'/{name}face.json'
        df.to_json(local_pt + view_pt)
        
        # updating cox info dict    
        info[f'{name}face_pt'] = view_pt

    #..........................................................................................
            
#---------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------|-
def mtcnnFaceDet(info, dir):
    '''
    It receives the dict with pandas paths, dir is the general directory
    '''
    local_pt    = dir + '/cox' 
    device      = "cuda" if torch.cuda.is_available() else "cpu"
    model       = MTCNN(device=device)
    print(f'The device is {device}')
    coxface(info, local_pt, model)
    


