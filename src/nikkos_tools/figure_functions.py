import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

def plot_snr_hist(line, linelabel, dfs, labels, colors, save_path=False):
    plt.figure(figsize=(10,10))
    for i, df in enumerate(dfs): 
        plt.hist(df[df.line == line]['snr_line'],  label=labels[i], color=colors[i], alpha=0.5)
    plt.xlabel(f'S/N$_{{{linelabel}}}$')
    plt.ylabel('Number of Objects')
    plt.legend()
    if save_path:
        plt.savefig(save_path)


def plot_spectrum_minimalist(x, y, save_path=False):
    fig = plt.figure(figsize = (20 , 10))
    gs = GridSpec(nrows=3, ncols=5)
    gs.update(wspace=0, hspace=0)

    ax = fig.add_subplot(gs[0:3, 0:5])
    ax.plot(x,y, color='k')
    ax.tick_params(labelleft=False, left=False, top=False, right=False)
    ax.minorticks_off()
    ax.axis('off')
    if save_path:
        plt.savefig(f'{save_path}', transparent=True)
