# A-Weighting IIR Filter Design for Real-Time Audio Processing

This repository contains the code for designing and implementing an A-weighting Infinite Impulse Response (IIR) filter based on the IEC 61672-1 standard, suitable for real-time audio processing in applications like sound level meters. The filter is designed in Python using SciPy, validated against the standard, and implemented in C++ for efficient real-time use, such as in an Android app. The project includes scripts for filter design, testing, and visualization, along with a performance evaluation to ensure real-time capability.

For a detailed explanation of the methodology, filter design process, and implementation, see my Medium post: [Designing an A-Weighting IIR Filter with Python for Real-Time Audio Apps: From IEC 61672-1 to C++.](https://medium.com/@maxiaortiz22/designing-an-a-weighting-iir-filter-with-python-for-real-time-audio-apps-from-iec-61672-1-to-c-fd3b3faa4fa0)

## Repository Contents

The repository is organized in a `code` folder containing all the necessary scripts:

- **`dBAFilterDesign4.py`**: The main Python script for designing the A-weighting IIR filter. It:
  - Calculates the theoretical A-weighting frequency response per IEC 61672-1.
  - Designs the digital IIR filter using SciPy’s bilinear transform.
  - Validates the filter against IEC reference points.
  - Tests the filter with a multi-tone signal and noise.
  - Exports filter coefficients to a JSON file for C++ integration.
  - Generates plots for frequency response and test results.

- **`filter.cpp`**: The C++ implementation of the A-weighting filter, including:
  - `AWeightingFilter`: A simple Direct Form II IIR filter implementation.
  - `AdvancedAWeightingFilter`: An experimental version with RMS and peak dB calculations for sound level meter applications.
  - Tests for a single-tone (1 kHz) and multi-tone (31.5 Hz, 1000 Hz, 8000 Hz) signal, saving results to `test_cpp.txt` and `multitone_test_cpp.txt`.
  - A performance test processing 1 million samples to evaluate real-time efficiency.

- **`test_cpp_filter.py`**: A Python script to analyze the C++ filter output (`test_cpp.txt` and `multitone_test_cpp.txt`). It generates time and frequency domain plots, comparing the C++ filter’s response to the theoretical A-weighting curve and IEC reference points.

- **`a_weighting_coeffs.json`**: The exported filter coefficients from `dBAFilterDesign4.py`, ready for use in the C++ implementation.

## Prerequisites

To run the code, you’ll need:
- **Python 3.x** with the following packages:
  - `numpy`
  - `scipy`
  - `matplotlib`
  - `pandas`
  Install them using:
  ```bash
  pip install numpy scipy matplotlib pandas
  ```

- **C++ Compiler**: A compiler like `g++` for building the C++ code. The provided compilation command is for Windows, but it can be adapted for other operating systems.

- A working directory with write permissions to save output files (`test_cpp.txt`, `multitone_test_cpp.txt`, `a_weighting_coeffs.json`).


## Usage

### 1. Running the Python Filter Design

The `main.py` script designs the A-weighting filter, validates it, and exports coefficients. To run it:

```bash
  python main.py
  ```

This will:

- Design the IIR filter for a 48 kHz sampling rate.
- Generate plots comparing the filter’s frequency response to the theoretical A-weighting curve and IEC 61672-1 reference points.
- Test the filter with a multi-tone signal and noise.
- Export the filter coefficients to `a_weighting_coeffs.json`.

The script outputs:

- Filter coefficients (numerator `b` and denominator `a`).
- Plots for frequency response and test results.
- A JSON file with coefficients and a C++ code snippet.


### 2. Compiling and Running the C++ Filter

The `filter.cpp` script implements the A-weighting filter in C++ and includes tests. To compile and run on Windows using `g++`:

```bash
  g++ filter.cpp -o filter.exe
  ./filter.exe
  ```

For other operating systems (e.g., Linux, macOS), use:

```bash
  g++ filter.cpp -o filter
  ./filter
  ```

This will:

- Run a single-tone test (1 kHz), saving results to `test_cpp.txt`.
- Run a multi-tone test (31.5 Hz, 1000 Hz, 8000 Hz), saving results to `multitone_test_cpp.txt`.
- Perform a performance test, processing 1 million samples to evaluate real-time efficiency.


### 3. Analyzing C++ Filter Results

To visualize and validate the C++ filter output, run:

```bash
  python test_cpp_filter.py
  ```

This script:

- Can be use the read `test_cpp.txt` (single-tone test) or `multitone_test_cpp.txt` (multi-tone test).
- Generates time domain plots showing input and A-weighted output.
- Perform a performance test, processing 1 million samples to evaluate real-time efficiency.


## Performance

The C++ filter was tested for real-time performance by processing 1 million samples:

```bash
    Performance test (processing 1 million samples)...
    Processed 1000000 samples in 39083 microseconds
    Processing rate: 25586572 samples/second
    Real-time ratio: 533.1x (higher is better)
  ```

This demonstrates that the filter processes samples over 533 times faster than real-time at a 48 kHz sampling rate, making it highly suitable for real-time audio processing in applications like Android sound level meters.

## Detailed Explanation

For a comprehensive walkthrough of the filter design, validation, and C++ implementation, read my Medium post: [Designing an A-Weighting IIR Filter with Python for Real-Time Audio Apps: From IEC 61672-1 to C++.](https://medium.com/@maxiaortiz22/designing-an-a-weighting-iir-filter-with-python-for-real-time-audio-apps-from-iec-61672-1-to-c-fd3b3faa4fa0) It covers:

- The IEC 61672-1 A-weighting formula and transfer function derivation.
- Designing the IIR filter with SciPy.
- Validating the filter against reference points.
- Implementing and testing the filter in C++ for real-time use.

## Contributing

Contributions are welcome! If you have improvements, bug fixes, or additional tests (e.g., other weighting filters like C-weighting), feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or feedback, contact me via github or [LinkedIn](https://www.linkedin.com/in/maximiliano-ortiz-7664541a9/).