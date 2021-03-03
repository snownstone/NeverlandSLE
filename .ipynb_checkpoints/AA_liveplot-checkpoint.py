import matplotlib.pyplot as plt
import numpy as np
plt.style.use('ggplot')

def live_plotter(x_vec, y1_data, line1, identifier='', pause_time=0.01):
    
    if line1==[]:
        # turn the interactive mode on
        plt.ion()          
        fig = plt.figure(figsize=(13,6))
        # 111 分别对应行数、列数、index
        ax = fig.add_subplot(111)     
        
        # 下方逗号必需加，ax.plot返回的是一个 Line2D list，not subscriptable，no len()
        # 不加逗号，就是一个list中的元素，subscriptable，has len()
        line1, = ax.plot(x_vec, y1_data, '-o', alpha=0.8)
        plt.ylabel('Y Label')
        plt.title('Title: {}'.format(identifier))
        
    
    # 后续只需要更新 y1_data
    line1.set_ydata(y1_data)
    if np.min(y1_data)<=line1.axes.get_ylim()[0] or np.max(y1_data)>=line1.axes.get_ylim()[1]:
        plt.ylim([np.min(y1_data)-np.std(y1_data), np.max(y1_data)+np.std(y1_data)])
    plt.pause(pause_time)
    
    return line1

size = 100
x_vec = np.linspace(0,1,size,endpoint=False)
y_vec = np.random.randn(len(x_vec))
line1 = []
while True:
    # np.random.randn():Return a sample (or samples) from the “standard normal” distribution.
    rand_val = np.random.randn(1)  
    y_vec[-1] = rand_val
    line1 = live_plotter(x_vec, y_vec, line1)
    y_vec = np.append(y_vec[1:],0.0)