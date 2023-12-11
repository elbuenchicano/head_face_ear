from PIL            import Image
from ultralytics    import YOLO
from tqdm           import tqdm
from utils          import *


import  torch
import  shutil
import  os 
import  yaml
import  pandas              as  pd 
import  matplotlib.pyplot   as  plt
import  matplotlib.patches  as  patches

####################################################################################################
####################################################################################################
####################################################################################################
####### Head detection using yolo ##################################################################
# this funciont is just to confire the bbox info
def plotDet(im_pt, xyxy, prob):
    ima     = np.array(Image.open(im_pt))
    fig, ax = plt.subplots()
    ax.imshow(ima)
    rect = patches.Rectangle((xyxy[0], xyxy[1]), xyxy[2] - xyxy[0], xyxy[3] - xyxy[1], 
                             linewidth=1, edgecolor='r', facecolor='none')

    ax.text(xyxy[0], xyxy[1], f'{prob}', fontsize = 10,  
                bbox = dict(facecolor = 'gray', alpha = 0.8, edgecolor='none')) 

    ax.add_patch(rect)
    plt.show()

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
def coxhead(info, local_pt, model):
    '''
    This function extracts heads for cox partitions, info contains the paths for pandas df
    '''
    names = ['st_', 'c1_', 'c2_', 'c3_']
    db_pt = info['db_pts'][u_whichOS()]

    ### for each view .............................................................................
    for name in names:
        view    = pd.read_json(local_pt + info[name + 'pt']).to_numpy()

        bbox    = []
        probs   = []

        for _, pt in tqdm(view, name):
            im_pt   = db_pt + pt
            results = model.predict(im_pt) 

            if len(results):
                xyxy        = results[0].boxes.xyxy.cpu().numpy()
                xyxy        = np.rint(xyxy[0]).astype(int)
                prob        = np.round(results[0].boxes.conf[0].item(), 2)

                probs.append(prob)
                bbox.append(xyxy)

                #plotDet(im_pt, xyxy, prob)                

            else :
                probs.append(0)
                bbox.append([0,0,0,0])

            break

        #..........................................................................................
        # saving view data on pandas json        
        df      = pd.DataFrame({'prob':probs, 'bbox':bbox})
        view_pt = f'/{name}head.json'
        df.to_json(local_pt + view_pt)
        
        # updating cox info dict    
        info[f'/{name}head_pt'] = view_pt

    #..........................................................................................
            

#---------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------
def yoloHeadDet(info, dir):
    '''
    It receives the dict with pandas paths, dir is the general directory
    '''
    local_pt    = dir + '/cox' 
    model       = YOLO('./saves/best.pt')

    coxhead(info, local_pt, model)
    
    
    



