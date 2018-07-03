import numpy as np
import audio_utilities
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

def plot(samples):
    fig = plt.figure(figsize=(1, 1))
    gs = gridspec.GridSpec(1, 1)
    gs.update(wspace=0.05, hspace=0.05)

    ax = plt.subplot(gs[0])
    plt.axis('off')
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_aspect('equal')
    plt.imshow(samples, cmap='Greys_r')
    

    return fig

stft_full = np.load('testog.npy')[0]
print(stft_full.dtype)
print(stft_full.shape)
print(np.amax(stft_full))
asdf
fig = plot(stft_full[:,:341])
plt.savefig('test.png', bbox_inches='tight', dpi=1000)
plt.close(fig)
stft_full = stft_full[:,:341] + 1j * stft_full[:,341:]
stft_full = stft_full.T
print(stft_full.shape)
output_signal = audio_utilities.istft_for_reconstruction(stft_full, 1024, 256)
audio_utilities.save_audio_to_file(output_signal, 44100, outfile='test.wav')