import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz
from code.dBAFilter_response import dBAFilter_frequency_response

def plot_a_weighting_response(b, a, fs=48000):
    """Plot the frequency response of the A-weighting filter and compare with theoretical"""
    
    # Calculate filter frequency response
    w, h = freqz(b, a, worN=8192, fs=fs)
    h_db = 20 * np.log10(abs(h))
    
    # Calculate theoretical A-weighting response
    A_theoretical, freq_theoretical = dBAFilter_frequency_response()
    
    plt.figure(figsize=(14, 10))
    
    # Plot magnitude response comparison
    plt.subplot(2, 1, 1)
    plt.semilogx(w, h_db, 'b-', linewidth=2, label='IIR Filter Response')
    plt.semilogx(freq_theoretical, A_theoretical, 'r--', linewidth=1, alpha=0.8, label='Theoretical A-weighting')
    
    plt.title('A-weighting Filter: IIR Filter vs Theoretical Response')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True)
    plt.xlim([10, fs/2])
    plt.ylim([-80, 5])
    
    # Add reference points from IEC 61672-1
    ref_freqs = [31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000]
    ref_values = [-39.4, -26.2, -16.1, -8.6, -3.2, 0, 1.2, 1.0, -1.1, -6.6]
    plt.scatter(ref_freqs, ref_values, color='green', s=60, zorder=5, marker='o', 
                label='IEC 61672-1 Reference', edgecolors='black', linewidth=1)
    
    # Customize x-axis ticks
    ticks = [20, 31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000, 20000]
    tick_labels = ['20', '31.5', '63', '125', '250', '500', '1k', '2k', '4k', '8k', '16k', '20k']
    plt.xticks(ticks, tick_labels)
    
    plt.legend()
    
    # Plot phase response
    plt.subplot(2, 1, 2)
    plt.semilogx(w, np.angle(h) * 180 / np.pi, 'b-', linewidth=2)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Phase (degrees)')
    plt.title('A-weighting Filter Phase Response')
    plt.grid(True)
    plt.xlim([10, fs/2])
    plt.xticks(ticks, tick_labels)
    
    plt.tight_layout()
    plt.show()
    
    # Print accuracy comparison at reference frequencies
    print("\nAccuracy comparison at IEC 61672-1 reference frequencies:")
    print("Freq (Hz) | IEC Ref | Filter | Error (dB)")
    print("-" * 45)
    
    for freq_ref, val_ref in zip(ref_freqs, ref_values):
        if freq_ref < fs/2:
            # Find closest frequency in filter response
            idx = np.argmin(np.abs(w - freq_ref))
            filter_val = h_db[idx]
            error = abs(filter_val - val_ref)
            print(f"{freq_ref:8.1f} | {val_ref:7.1f} | {filter_val:6.1f} | {error:5.2f}")
    
    return w, h_db