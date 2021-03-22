import madmom
import numpy as np
from madmom.audio import signal, hpss, spectrogram
import time
from codelab_adapter_client import AdapterNode



class MyNode(AdapterNode):
    NODE_ID = "linda/test"

    def __init__(self):
        super().__init__()
        
node = MyNode()
node.receive_loop_as_thread()


kwargs = dict(
    sample_rate=44100,
    num_channels=1,
    frame_size=2048,
    hop_size=441,
    filterbank=madmom.audio.filters.MelFilterbank,
    num_bands=12
    
)
stream=signal.Stream(**kwargs)


spec_list = [i for i in range(10)]

n = 0

try:
    for frames in stream:  
        lindaout = ["LindaOut",0]
        #a=time.time()
        fs = madmom.audio.signal.FramedSignal(frames,**kwargs)
        stft = madmom.audio.stft.STFT(fs)
        spec = madmom.audio.spectrogram.LogarithmicFilteredSpectrogram(stft, **kwargs)
        i = n%2
        if i == 0:
            for j in range(len(spec)):
                spec_list[i*5+j]=np.ndarray.tolist(spec[j])
            n = n + 1
        elif i == 1:
            for j in range(len(spec)):
                spec_list[i*5+j]=np.ndarray.tolist(spec[j])
            lindaout[1]=spec_list
            #print(lindaout)
            node.linda_out(lindaout)
            n = n + 1   
            #b=time.time()
            #print(b-a)

except KeyboardInterrupt:
    print('interrupt by user')
