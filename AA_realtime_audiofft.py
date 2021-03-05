import pyaudio
import numpy as np
import time

from codelab_adapter_client import AdapterNode

class MyNode(AdapterNode):
    NODE_ID = "linda/test"

    def __init__(self):
        super().__init__()
        
node = MyNode()
node.receive_loop_as_thread()



time.sleep(0.1)

buff_size = 8820                    
wanted_num_of_bins = 12              
fs = 44100
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=fs, input=True, frames_per_buffer=int(buff_size))


end_index = []
for i in np.arange(12):    
    end_index.append(int((buff_size/2)/2**i))
end_index.reverse()

    
start_index = [0]
for i in end_index[:-1]:
    start_index.append(i+1)        

#n=0

while True:

    block = stream.read(int(buff_size))
    data = np.fromstring(block, dtype=np.int16)

    x = np.array(data)/(2**15)
    seg_len = len(x)

    
    X = np.abs(np.fft.fft(x))[0:int(seg_len/2)]


    X2 = []
    for i in np.arange(12):
        XX = np.mean(X[start_index[i]:end_index[i]])
        # XX 可能为 0，则下面无法求 log10，所以为 0 时，令其等于一个非常小的值
        if XX == 0:
            XX = 1e-300
        # 下面是将振幅转为分贝，就是以10为底取对数，因为相比线性关系
        # 对数关系更符合人耳对声音响度的辨别机制 
        # 取绝对值是因为分贝尺度中，符号没影响
        
        XXdB = 20*np.log10(XX)
        XXout = np.abs(XXdB)
        X2.append(XXout)
        #X2.append(XX)
        i=i+1
    
    outlist = ['X2_12',X2]
    
    node.linda_out(outlist)

    # n = n + 1


