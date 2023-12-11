import matplotlib.pyplot as plt
import numpy as np

####################################################################################################
####################################################################################################
####################################################################################################
def pltImagList(imgs, rc = (2,2), fsize= (12,8), title='', titles=None):
    '''
    List of imgs (w,h,c), 
    rows and columns - tuple,  
    figure size  - tuple
    title of figure - str
    titles for each figure - list [strs]
    -> plt.figure
    '''
    if titles == None:
        titles = [f'Img {i}' for i in range(len (imgs))]

    rows, cols  = rc
    fig         = plt.figure(figsize= fsize) 

    for id, img in enumerate(imgs): 
        fig.add_subplot(rows, cols, id+1) 
        plt.imshow(img) 
        #plt.axis('off') 
        plt.title(titles[id])

    fig.suptitle(title)
    return fig

####################################################################################################
####################################################################################################
####################################################################################################