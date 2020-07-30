import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from . import pulsewaves_pb2 as pwproto

class PulseWaves:
    
    channel_labels = ['Reference Power', 'Low Power', 'High Power']
    
    def __init__(self, file_name):
        self.pwmsg = pwproto.PWListP()
        f = open(file_name, 'rb')
        self.pwmsg.ParseFromString(f.read())
        f.close()
        
        self.scale = pd.DataFrame(
                {
                    'offset': [self.pwmsg.xOffset, self.pwmsg.yOffset, self.pwmsg.zOffset, self.pwmsg.tOffset],
                    'scale': [self.pwmsg.xScale, self.pwmsg.yScale, self.pwmsg.zScale, self.pwmsg.tScale]
                },
                index = ['x','y', 'z', 't']
            )
        
    def get_pulse(self, pulse_idx):
        return self.pwmsg.pulse[pulse_idx]

    def num_pulses(self):
        return len(self.pwmsg)
    
    def get_sampling(self, pulse_idx, sampling_idx):
        return self.pwmsg.pulse[pulse_idx].channels[sampling_idx]
    
    def get_segment(self, pulse_idx, sampling_idx, segment_idx):
        return self.pwmsg.pulse[pulse_idx].channels[sampling_idx].waveSegment[segment_idx]
        
    def get_direction_vector(self, pulse):
        
        if type(pulse) == int:
            pulse = self.get_pulse(pulse)
        
        direction_vector = pd.DataFrame({
            'anchor': [pulse.anchorX, pulse.anchorY, pulse.anchorZ],
            'target': [pulse.targetX, pulse.targetY, pulse.targetZ]
            },
            index = ['x', 'y', 'z']
        )

        # scale
        direction_vector=direction_vector.mul(self.scale.loc['x':'z']['scale'], axis=0).add(self.scale.loc['x':'z']['offset'], axis=0)
        direction_vector['d'] = (direction_vector['target'] - direction_vector['anchor'])/1000
        
        return direction_vector
    
    def get_samples(self, pulse_idx = -1, sampling_idx = -1, segment_idx = -1, segment = None,  direction_vector = None, georef = True):
        
        if segment is None:
            segment = self.get_segment(pulse_idx, sampling_idx, segment_idx)
        
        samples = pd.DataFrame({'amplitude': segment.echo})
        
        if not georef:
            return samples
        else:
            if direction_vector is None:
                direction_vector = self.get_direction_vector(pulse_idx)
            duration_from_anchor = segment.durationFromAnchor
            range_values_in_sampling_unit=duration_from_anchor+pd.Series(samples.index)
            sample_coords = range_values_in_sampling_unit.apply(lambda _: _ * direction_vector['d']+direction_vector['anchor'])
            
            return samples.join(sample_coords)
        
    def plot_waves(self, 
                    pulse,
                   georef = True, title = None):
    
        if type(pulse) == int:
            pulse = self.get_pulse(pulse)
        
        direction_vector = self.get_direction_vector(pulse)

        # compute number of samplings and segments
        num_samplings = len(pulse.channels)
        max_num_segments = 0

        for sampling_idx in range(num_samplings):
            num_segments = len(pulse.channels[sampling_idx].waveSegment)
            if max_num_segments < num_segments:
                max_num_segments = num_segments

        # set up a plot
        plt.rc('figure', figsize=(3*num_samplings,5*max_num_segments))

        fig, axes = plt.subplots(max_num_segments, num_samplings, 
                                     #sharey=True,
                                     #sharex = 'col'
                                     constrained_layout=True
                                    )

        if title is not None:
            fig.suptitle(title, fontsize=12)

        # plot
        for sampling_idx in range(num_samplings):
            num_segments = len(pulse.channels[sampling_idx].waveSegment)
            for segment_idx in range(num_segments):
                segment = pulse.channels[sampling_idx].waveSegment[segment_idx]

                samples = self.get_samples(segment = segment, 
                                           direction_vector = direction_vector, 
                                           georef = georef)

                if len(axes.shape) == 1:
                    ax = axes[sampling_idx]
                elif len(axes.shape) == 2: 
                    ax = axes[segment_idx, sampling_idx]

                axo = True

                ax.plot(samples['amplitude'], samples['z'] if georef else samples.index, 
                             linewidth=1.0,
                             c='k',
                             drawstyle = 'steps-post'
                            )

                ax.set_title('{0} - seg #{1}'.format(PulseWaves.channel_labels[sampling_idx], segment_idx))

        # configure the axes
        axes_df = pd.DataFrame(axes)
        y_lim = axes_df.applymap(lambda _ : [_.axes.dataLim.ymin, _.axes.dataLim.ymax])
        max_height = axes_df.applymap(lambda _ : _.axes.dataLim.height).to_numpy().max()

        if max_num_segments > 1:
            max_amplitude = axes_df.applymap(lambda _ : _.axes.dataLim.xmax).replace([np.inf, -np.inf], np.nan).max(axis=0)

        for i in range(max_num_segments):
            for j in range(num_samplings):
                if max_num_segments > 1:
                    ax = axes[i,j]
                    yl = y_lim.iloc[i][j]
                else:
                    ax = axes[j]
                    yl = y_lim.iloc[j][i]

                if ax.dataLim.xmax == np.inf:
                    fig.delaxes(ax)
                else:
                    if max_num_segments > 1:
                        ax.set_xlim(0, max_amplitude[j]+5)

                    if georef:
                        ax.set_ylim(yl[1] - max_height, yl[1])
                    else:
                        ax.set_ylim(yl[0]+max_height, yl[0])

                    ax.spines['right'].set_visible(False)
                    ax.spines['top'].set_visible(False)

                    ax.set_xlabel('Amplitude')
                    ax.set_ylabel('Elevation' if georef else 'Sample index')

        return fig, axes