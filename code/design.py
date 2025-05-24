import numpy as np
from scipy.signal import bilinear, freqs

def design_a_weighting_filter(fs=48000):
    """
    Design A-weighting filter according to IEC 61672-1
    Returns filter coefficients for real-time implementation
    """
    
    # IEC 61672-1 pole frequencies (Hz)
    f1 = 20.60
    f2 = 107.7
    f3 = 737.9
    f4 = 12194
    
    # Convert to angular frequencies (rad/s)
    p1 = 2 * np.pi * f1
    p2 = 2 * np.pi * f2
    p3 = 2 * np.pi * f3
    p4 = 2 * np.pi * f4
    
    # A-weighting transfer function in s-domain
    # The frequency response given by the standard is: H(s) = K * s^4 / [(s^2 + p1^2) * sqrt(s^2 + p2^2) * sqrt(s^2 + p3^2) * (s^2 + p4^2)]
    # But to design filters, it is convenient to use the pole-zero form: H(s) = K * s^4 / [(s + p1)^2 * (s + p2) * (s + p3) * (s + p4)^2]
    
    # Numerator: s^4 (4 zeros at origin)
    num_s = np.array([1, 0, 0, 0, 0], dtype=float)  # s^4
    
    # Denominator: (s + p1)^2 * (s + p2) * (s + p3) * (s + p4)^2
    # Build each factor
    den1 = np.poly([-p1, -p1])  # (s + p1)^2
    den2 = np.poly([-p2])       # (s + p2)
    den3 = np.poly([-p3])       # (s + p3)
    den4 = np.poly([-p4, -p4])  # (s + p4)^2
    
    # Multiply all denominator polynomials
    den_s = np.convolve(den1, den2)
    den_s = np.convolve(den_s, den3)
    den_s = np.convolve(den_s, den4)
    
    # Calculate normalization constant A1000 for 0 dB at 1000 Hz
    w1000 = 2 * np.pi * 1000
    _, h1000 = freqs(num_s, den_s, [w1000])
    A1000 = 1.0 / abs(h1000[0])
    
    # Apply normalization
    num_s = num_s * A1000
    
    # Convert to digital filter using bilinear transform
    b, a = bilinear(num_s, den_s, fs)
    
    return b, a, f1, f2, f3, f4