import matplotlib.pyplot as plt
import numpy as np 

def plot_waves(pls):

    # compute number of samplings and segments
    num_samplings = len(pls.channels)
    max_num_segments = 0

    for sampling_idx in range(num_samplings):
        num_segments = len(pls.channels[sampling_idx].waveSegment)
        if max_num_segments < num_segments:
            max_num_segments = num_segments

    # set up a plot
    plt.rc('figure', figsize=(3*num_samplings,5*max_num_segments))

    fig, axes = plt.subplots(max_num_segments, num_samplings, 
                                 #sharey=True,
                                 #sharex = 'col'
                                 #constrained_layout=True
                                )

    axes_occupation = np.full_like(axes, False)
    
    max_num_samples = 0
    max_amplitudes = np.zeros(num_samplings)

    # plot
    for sampling_idx in range(num_samplings):
        num_segments = len(pls.channels[sampling_idx].waveSegment)
        for segment_idx in range(num_segments):
            
            echoes = echoes = pls.channels[sampling_idx].waveSegment[segment_idx].echo
            
            num_samples = len(echoes)
            if max_num_samples < num_samples:
                max_num_samples = num_samples
                
            if max_amplitudes[sampling_idx] < max(echoes):
                max_amplitudes[sampling_idx] = max(echoes)
            
            if max_num_segments >1:
                ax = axes[segment_idx, sampling_idx]
                axes_occupation[segment_idx, sampling_idx] = True
            else:
                ax = axes[sampling_idx]
                axes_occupation[sampling_idx] = True
            
            ax.plot(echoes, np.arange(num_samples), 
                         linewidth=1.0,
                         c='k',
                         drawstyle = 'steps-post'
                        )

            ax.set_title('{0} - seg #{1}'.format(channel_labels[sampling_idx], segment_idx))

    #ax.invert_yaxis()  


    # delete empty axes
    for i in range(max_num_segments):
        for j in range(num_samplings):

            if max_num_segments >1:
                ax = axes[i,j]
                axo = axes_occupation[i, j]
            else:
                ax = axes[j]
                axo = axes_occupation[j]

            if not axo:
                fig.delaxes(ax)
                #print(i, j)
            else:
                ax.set_xlim(0, max_amplitudes[j]+5)
                ax.set_ylim(max_num_samples, 0)
                ax.spines['right'].set_visible(False)
                ax.spines['top'].set_visible(False)
                #print(i, j, max_amplitudes[j])

                    
    
    return fig, axes

channel_labels = ['Reference Power', 'Low Power', 'High Power']