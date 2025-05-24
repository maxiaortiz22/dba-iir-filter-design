import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

def test_real_time_filtering(b, a, fs=48000):
    """Test the filter with a real-time-like implementation"""
    
    # Generate test signal (multiple frequencies)
    duration = 2.0
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    
    # Multi-tone test signal
    freqs_test = [100, 500, 1000, 2000, 5000]
    x = np.zeros_like(t)
    for f in freqs_test:
        x += np.sin(2 * np.pi * f * t) / len(freqs_test)
    
    # Add some noise
    x += 0.1 * np.random.randn(len(x))
    
    # Apply filter using scipy (for comparison)
    y_scipy = signal.lfilter(b, a, x)
    
    # Manual implementation (suitable for real-time)
    y_manual = real_time_filter(x, b, a)
    
    # Plot results
    plt.figure(figsize=(12, 6))
    
    plt.subplot(2, 1, 1)
    t_plot = t[:int(0.1 * fs)]  # Show first 100ms
    plt.plot(t_plot * 1000, x[:len(t_plot)], label='Input', alpha=0.7)
    plt.plot(t_plot * 1000, y_scipy[:len(t_plot)], label='A-weighted (scipy)', linewidth=2)
    plt.plot(t_plot * 1000, y_manual[:len(t_plot)], '--', label='A-weighted (manual)', alpha=0.8)
    plt.xlabel('Time (ms)')
    plt.ylabel('Amplitude')
    plt.title('A-weighting Filter Test - Time Domain')
    plt.legend()
    plt.grid(True)
    
    # Frequency domain comparison
    plt.subplot(2, 1, 2)
    f_fft = np.fft.fftfreq(len(x), 1/fs)
    X = np.fft.fft(x)
    Y_scipy = np.fft.fft(y_scipy)
    Y_manual = np.fft.fft(y_manual)
    
    mask = f_fft > 0
    plt.loglog(f_fft[mask], np.abs(X[mask]), label='Input', alpha=0.7)
    plt.loglog(f_fft[mask], np.abs(Y_scipy[mask]), label='A-weighted (scipy)', linewidth=2)
    plt.loglog(f_fft[mask], np.abs(Y_manual[mask]), '--', label='A-weighted (manual)', alpha=0.8)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.title('A-weighting Filter Test - Frequency Domain')
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()
    
    return y_manual, y_scipy

def real_time_filter(x, b, a):
    """
    Real-time filter implementation suitable for C++ translation
    """
    # Initialize delay lines
    w = np.zeros(max(len(a), len(b)))  # Internal state
    y = np.zeros_like(x)
    
    # Process sample by sample
    for n in range(len(x)):
        # Input with feedback
        w[0] = x[n]
        for i in range(1, len(a)):
            if i < len(w):
                w[0] -= a[i] * w[i]
        
        # Output calculation
        y[n] = 0
        for i in range(len(b)):
            if i < len(w):
                y[n] += b[i] * w[i]
        
        # Shift delay line
        for i in range(len(w)-1, 0, -1):
            w[i] = w[i-1]
    
    return y