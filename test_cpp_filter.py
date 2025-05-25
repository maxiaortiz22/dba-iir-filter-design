import pandas as pd
import matplotlib.pyplot as plt

"""Test the real-time implementation of the A-weighting filter in C++.
This script reads the output of the filter.cpp script that processes a 1kHz sine wave.
The filtered signal is expected to be similar to the original signal since the A-weighting filter is designed to have a flat response at 1kHz."""

# Read the test data from the C++ output file
# The file should contain three columns: Time (s), Input, and A-weighted output
data = pd.read_csv("test_cpp.txt", sep="\t", header=None)
data.columns = ["Time (s)", "Input", "A-weighted output"]

# Plot the input and A-weighted output signals
plt.figure(figsize=(12, 6))
plt.plot(data["Time (s)"], data["Input"], label="Input Signal", alpha=0.7)
plt.plot(data["Time (s)"], data["A-weighted output"], label="A-weighted Output", linewidth=2)
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.title("A-weighting Filter Test - Time Domain")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#Calculate the frequency response of the Input and A-weighted output
from scipy.fft import fft, fftfreq
import numpy as np
# Sampling frequency
fs = 48000
# Number of samples
N = len(data["Input"])
# Compute the FFT
yf_input = fft(data["Input"].to_numpy())
yf_output = fft(data["A-weighted output"].to_numpy())
# Compute the frequencies
xf = fftfreq(N, 1/fs)[:N//2]

# Plot the frequency response
plt.figure(figsize=(12, 6))
plt.semilogx(xf, 2.0/N * np.abs(yf_input[:N//2]), label="Input Signal", alpha=0.7)
plt.semilogx(xf, 2.0/N * np.abs(yf_output[:N//2]), label="A-weighted Output", linewidth=2)
plt.xticks([20, 31.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000], 
           ['20', '31.5', '63', '125', '250', '500', '1k', '2k', '4k', '8k', '16k'])
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("A-weighting Filter Test - Frequency Domain")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()