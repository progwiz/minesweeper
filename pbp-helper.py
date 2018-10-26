from PIL import Image
import numpy as np
import os

if __name__ == "__main__":
    for file in os.listdir("play-by-play/"):
        pilimg=Image.open("play-by-play/"+file)
        nparr=np.asarray(pilimg,dtype=np.uint8)
        nparr=nparr[30:300,570:]
        pilimg=Image.fromarray(nparr)
        pilimg.save("play-by-play2/"+file)