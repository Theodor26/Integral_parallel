from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd
from pandas.tools.plotting import table

def plot_3d(fig, pos, title, data):

    ax = fig.add_subplot(pos, projection='3d')
    ax.view_init(15, 300)

    x = np.array([1, 2, 4, 8, 16, 32, 64, 128])
    x_scaled = np.arange(8)
    y = np.array([100000000, 200000000, 400000000, 800000000])
    y_labels = np.array([1, 2, 4, 8])
    X, Y = np.meshgrid(x_scaled, y)
    ax.plot_surface(X, Y, data)
    ax.set_title("Time 3D-plot for functon "+title)

    ax.set_xlabel('Num of threads, n')
    ax.set_xticks(x_scaled)
    ax.set_xticklabels(x)

    ax.set_ylabel('Number of segments, 1e+8')
    ax.set_yticks(y)
    ax.set_yticklabels(y_labels)

    ax.set_zlabel('Time, s')

def plot_3d_grid(data_list):
    fig = plt.figure(figsize=(10, 10))
    legends = ['5', 'x', 'x^3 – 3*x^2 + 6*x – 3', 'cos(x)*exp(x) / (sqrt(x+1) + 1)']
    for i, data in enumerate(data_list):
        plot_3d(fig=fig, pos=221+i, title=legends[i], data=data)
    plt.subplots_adjust(left=0.03, right=0.97, top=0.99, bottom=0.01, wspace=0.03, hspace=0.05)
    plt.savefig('plots1.png')

def plot_2d(fig, pos, title, data):
    ax = fig.add_subplot(pos)
    x = np.array([1, 2, 4, 8, 16, 32, 64, 128])
    x_ticks = np.array([1, 4, 8, 16, 32, 64, 128])
    legends = ['5', 'x', 'x^3 – 3*x^2 + 6*x – 3', 'cos(x)*exp(x) / (sqrt(x+1) + 1)']

    for i, d in enumerate(data[1:]):
        ax.plot(x, data[0][i]/d, label=legends[i])

    ax.plot(np.arange(30), np.arange(30), label='theoretical maximum')

    ax.set_title("Speedup for "+title+"e+8 segments")

    ax.set_xscale('log', basex=2)
    ax.set_xlabel('Num of threads, n')
    ax.set_xticks(x)
    ax.set_xticklabels(x)

    ax.set_ylabel("Speedup")
    ax.legend()

def plot_improvments(data_list):
    fig = plt.figure(figsize=(10, 10))
    for i in range(len(data_list) - 1):
        plot_2d(fig=fig, pos=221+i, title=str(2**i), data=[x[i] for x in data_list])
    plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1, wspace=0.18, hspace=0.18)
    # plt.show()
    plt.savefig('plots2.png')

def plot_baseline(data):
    df = pd.DataFrame(data)
    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)
    x = np.array([100000000, 200000000, 400000000, 800000000])
    legends = ['5', 'x', 'x^3 – 3*x^2 + 6*x – 3', 'cos(x)*exp(x) / (sqrt(x+1) + 1)']
    for i in range(data.shape[0]):
        ax.plot(x, data[i], label=legends[i])

    ax.set_title("Baseline times")
    x_labels = np.array([1, 2, 4, 8])
    ax.set_xlabel('Number of segments, 1e+8')
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels)
    ax.set_ylabel('Time, s')
    ax.legend()

    plt.savefig('plots3.png')


t1 = np.array([[0.802945, 0.343306, 0.192145, 0.111418, 0.081109, 0.057638, 0.044680, 0.048219],
               [1.407624, 0.736348, 0.331637, 0.182383, 0.140456, 0.105269, 0.083282, 0.073499],
               [2.916452, 1.421541, 0.700857, 0.414886, 0.303172, 0.230988, 0.174660, 0.170218],
               [5.425115, 2.894065, 1.420551, 0.960026, 0.591916, 0.421368, 0.337610, 0.254602]])

t2 = np.array([[0.822104, 0.454519, 0.196831, 0.113132, 0.098316, 0.059304, 0.047328, 0.043623],
               [1.752019, 0.885294, 0.473899, 0.308920, 0.191291, 0.116715, 0.092045, 0.086535],
               [3.408470, 1.809323, 0.879313, 0.543115, 0.365563, 0.269463, 0.187459, 0.171236],
               [8.875437, 5.127204, 2.614182, 1.063620, 0.728377, 0.491140, 0.388541, 0.341308]])

t3 = np.array([[1.384841, 0.859509, 0.437942, 0.221654, 0.131602, 0.095595, 0.086765, 0.073663],
               [2.926003, 1.446265, 0.874269, 0.431830, 0.309539, 0.183305, 0.151902, 0.114200],
               [5.717930, 3.026848, 1.511332, 0.906797, 0.558742, 0.367077, 0.302326, 0.236425],
               [11.425679, 6.188951, 3.087805, 1.814468, 1.277032, 0.867640, 0.601787, 0.447665]])

t4 = np.array([[7.317283, 4.095276, 2.112512, 1.168493, 0.865351, 0.589287, 0.431328, 0.319202],
               [15.814978, 8.173528, 4.309955, 2.196992, 1.624703, 1.370049, 0.857015, 0.556044],
               [30.508328, 20.267319, 8.993891, 4.524134, 3.609187, 2.321845, 1.656797, 1.089916],
               [63.738901, 33.706602, 16.616497, 9.207244, 5.910189, 4.483510, 3.353104, 1.882826]])

t0= np.array([[0.592909, 1.192507, 2.374168, 4.765317],
                   [0.700169, 1.398317, 2.792076, 5.604007],
                   [1.271858, 2.544031, 5.087550, 10.175281],
                   [7.009836, 14.011827, 28.039213, 56.082085]])

plot_3d_grid([t1, t2, t3, t4])
plot_improvments([np.transpose(t0), t1, t2, t3, t4])
plot_baseline(t0)
