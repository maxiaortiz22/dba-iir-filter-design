import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq

# Read multi-tone or single-tone test data
data = pd.read_csv("data/multitone_test_cpp.txt", sep="\t", header=None)
#data = pd.read_csv("data/test_cpp.txt", sep="\t", header=None)
data.columns = ["Time (s)", "Input", "A-weighted Output"]

# Plot time domain
plt.figure(figsize=(12, 6))
plt.rcParams.update({'font.size': 14})
plt.plot(data["Time (s)"], data["Input"], label="Input Signal", alpha=0.7)
plt.plot(data["Time (s)"], data["A-weighted Output"], label="A-weighted Output", linewidth=2)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("Multi-tone A-weighting Filter Test - Time Domain")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Compute frequency response
fs = 48000
N = len(data["Input"])
yf_input = fft(data["Input"].to_numpy())
yf_output = fft(data["A-weighted Output"].to_numpy())
xf = fftfreq(N, 1/fs)[:N//2]

# Plot frequency response
plt.figure(figsize=(12, 6))
plt.rcParams.update({'font.size': 14})
plt.semilogx(xf, 20 * np.log10(np.abs(yf_input[:N//2]) / (N/2) + 1e-12), label="Input Signal", alpha=0.7)
plt.semilogx(xf, 20 * np.log10(np.abs(yf_output[:N//2]) / (N/2) + 1e-12), label="A-weighted Output", linewidth=2)

plt.xticks([20, 31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000], 
           ['20', '31.5', '63', '125', '250', '500', '1k', '2k', '4k', '8k', '16k'])
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude (dB)")
plt.title("Multi-tone A-weighting Filter Test - Frequency Domain")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()