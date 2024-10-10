import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from IPython import display


matplotlib.rcParams['toolbar'] = 'None'
plt.ion()  # interactive on; plots interactively


def plot(scores, mean_scores):
    display.clear_output(wait=True)
    display.display(plt.gcf())  # get current figure; create new if none exists
    plt.clf()  # clear current figure
    plt.gcf().canvas.manager.set_window_title("Training...")
    plt.xlabel('Number of Games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores) - 1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores) - 1, mean_scores[-1], str(mean_scores[-1]))
    plt.show(block=False)  # show the plot but don't block the program
    plt.pause(0.1)  # update the display before this; pause to perform event tasks
