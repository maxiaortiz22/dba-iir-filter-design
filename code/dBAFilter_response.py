import numpy as np

def dBAFilter_frequency_response():
    """
    Calculate theorical A-weighting frequency response according to IEC 61672-1
    """
    # Define poles:
    f1 = 20.60  # Hz
    f2 = 107.7  # Hz
    f3 = 737.9  # Hz
    f4 = 12194  # Hz

    # Filter equation:
    A = np.array([])
    freq = np.arange(0.1, 20000, 0.1)  # Start from 0.1 to avoid division by zero
    
    for f in freq:
        aux = (f4**2 * f**4) / ((f**2 + f1**2) * np.sqrt(f**2 + f2**2) * np.sqrt(f**2 + f3**2) * (f**2 + f4**2))
        aux = aux**2
        A = np.append(A, 10 * np.log10(aux))

    # Normalize to 0 dB at 1000 Hz
    f0 = 1000
    f0_index = np.where(np.abs(freq - f0) < 0.05)[0][0]  # Find closest to 1000 Hz
    A0 = A[f0_index]
    A = A - A0

    return A, freq