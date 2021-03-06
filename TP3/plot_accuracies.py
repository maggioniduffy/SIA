from cProfile import label
import matplotlib.pyplot as plt
import numpy as np

def plot_acc(epochs, training, test, title=''):
    plt.style.use('default')
    fig, ax = plt.subplots()
    y_max = np.amax(np.array([np.amax(training),np.amax(test)]))
    plt.ylabel('Accuracy')
    plt.xlabel('Iteraciones')
    plt.title(title)
    length = len(epochs)
    ax.set(xlim=(0,length), xticks=np.arange(0,length, length/10),
            ylim=(0,y_max + 0.1), yticks=np.arange(0,y_max + 0.1, y_max/10))
    ax.plot(epochs,training, label='Training')
    ax.plot(epochs,test, label='Test')
    plt.legend()
    plt.show(block=True)