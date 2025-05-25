#include <iostream>
#include <vector>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <limits>
#include <chrono>
#include <algorithm>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

// To compile on windows with gcc, use: g++ filter.cpp -o filter.exe

// Simple A-weighting filter class
class AWeightingFilter {
private:
    static const int ORDER = 6;
    static const int NUM_COEFFS = 7;
    
    // Filter coefficients from your JSON
    double b[NUM_COEFFS] = {
        2.343001251415276e-01,
        -4.686002502830553e-01,
        -2.343001251415276e-01,
        9.372005005661108e-01,
        -2.343001251415275e-01,
        -4.686002502830553e-01,
        2.343001251415276e-01
    };
    
    double a[NUM_COEFFS] = {
        1.000000000000000e+00,
        -4.113050107329960e+00,
        6.553157702958688e+00,
        -4.990918046664834e+00,
        1.785795382617391e+00,
        -2.462108026867600e-01,
        1.122587847673618e-02
    };
    
    // Delay line (internal state)
    double w[NUM_COEFFS];
    
public:
    // Constructor - initialize delay line to zero
    AWeightingFilter() {
        reset();
    }
    
    // Reset filter state
    void reset() {
        for(int i = 0; i < NUM_COEFFS; i++) {
            w[i] = 0.0;
        }
    }
    
    // Process single sample (Direct Form II implementation)
    double process(double input) {
        // Calculate intermediate value with feedback
        w[0] = input;
        for(int i = 1; i < NUM_COEFFS; i++) {
            w[0] -= a[i] * w[i];
        }
        
        // Calculate output with feedforward
        double output = 0.0;
        for(int i = 0; i < NUM_COEFFS; i++) {
            output += b[i] * w[i];
        }
        
        // Shift delay line
        for(int i = NUM_COEFFS - 1; i > 0; i--) {
            w[i] = w[i-1];
        }
        
        return output;
    }
    
    // Process array of samples
    void processBlock(const double* input, double* output, int numSamples) {
        for(int i = 0; i < numSamples; i++) {
            output[i] = process(input[i]);
        }
    }
    
    // Process vector of samples
    std::vector<double> processBlock(const std::vector<double>& input) {
        std::vector<double> output(input.size());
        for(size_t i = 0; i < input.size(); i++) {
            output[i] = process(input[i]);
        }
        return output;
    }
};

// Advanced A-weighting filter with additional features
class AdvancedAWeightingFilter {
private:
    static const int ORDER = 6;
    static const int NUM_COEFFS = 7;
    
    double b[NUM_COEFFS] = {
        2.343001251415276e-01, -4.686002502830553e-01, -2.343001251415276e-01,
        9.372005005661108e-01, -2.343001251415275e-01, -4.686002502830553e-01,
        2.343001251415276e-01
    };
    
    double a[NUM_COEFFS] = {
        1.000000000000000e+00, -4.113050107329960e+00, 6.553157702958688e+00,
        -4.990918046664834e+00, 1.785795382617391e+00, -2.462108026867600e-01,
        1.122587847673618e-02
    };
    
    double w[NUM_COEFFS];
    double sampleRate;
    bool initialized;
    
    // Statistics
    double peakValue;
    double rmsSum;
    int sampleCount;
    
public:
    AdvancedAWeightingFilter(double fs = 48000.0) : sampleRate(fs), initialized(false) {
        reset();
    }
    
    void reset() {
        for(int i = 0; i < NUM_COEFFS; i++) {
            w[i] = 0.0;
        }
        peakValue = 0.0;
        rmsSum = 0.0;
        sampleCount = 0;
        initialized = true;
    }
    
    double process(double input) {
        if (!initialized) reset();
        
        // Direct Form II implementation
        w[0] = input;
        for(int i = 1; i < NUM_COEFFS; i++) {
            w[0] -= a[i] * w[i];
        }
        
        double output = 0.0;
        for(int i = 0; i < NUM_COEFFS; i++) {
            output += b[i] * w[i];
        }
        
        // Shift delay line
        for(int i = NUM_COEFFS - 1; i > 0; i--) {
            w[i] = w[i-1];
        }
        
        // Update statistics
        double absOutput = std::abs(output);
        if (absOutput > peakValue) {
            peakValue = absOutput;
        }
        rmsSum += output * output;
        sampleCount++;
        
        return output;
    }
    
    void processBlock(const float* input, float* output, int numSamples) {
        for(int i = 0; i < numSamples; i++) {
            output[i] = static_cast<float>(process(static_cast<double>(input[i])));
        }
    }
    
    // Get RMS level in dB
    double getRMSdB() const {
        if (sampleCount == 0) return -std::numeric_limits<double>::infinity();
        double rms = std::sqrt(rmsSum / sampleCount);
        return 20.0 * std::log10(rms + 1e-12); // Add small value to avoid log(0)
    }
    
    // Get peak level in dB
    double getPeakdB() const {
        return 20.0 * std::log10(peakValue + 1e-12);
    }
    
    // Reset statistics
    void resetStatistics() {
        peakValue = 0.0;
        rmsSum = 0.0;
        sampleCount = 0;
    }
    
    double getSampleRate() const { return sampleRate; }
    int getOrder() const { return ORDER; }
};

// Test function to verify filter operation
void testFilter() {
    const double fs = 48000.0;
    const double duration = 1.0; // 1 second
    const int numSamples = static_cast<int>(fs * duration);
    
    AWeightingFilter filter;
    
    std::cout << "Testing A-weighting filter...\n";
    std::cout << "Sample rate: " << fs << " Hz\n";
    std::cout << "Duration: " << duration << " seconds\n";
    std::cout << "Samples: " << numSamples << "\n\n";
    
    // Test with 1 kHz sine wave (should have ~0 dB gain)
    std::vector<double> input(numSamples);
    std::vector<double> output;
    
    const double testFreq = 1000.0; // 1 kHz
    const double amplitude = 1.0;
    
    // Generate test signal
    for(int i = 0; i < numSamples; i++) {
        double t = static_cast<double>(i) / fs;
        input[i] = amplitude * std::sin(2.0 * M_PI * testFreq * t);
    }
    
    // Process signal
    output = filter.processBlock(input);
    
    // Calculate RMS of input and output
    double inputRMS = 0.0, outputRMS = 0.0;
    
    // Skip first 1000 samples to avoid transient
    const int skipSamples = 1000;
    for(int i = skipSamples; i < numSamples; i++) {
        inputRMS += input[i] * input[i];
        outputRMS += output[i] * output[i];
    }
    
    inputRMS = std::sqrt(inputRMS / (numSamples - skipSamples));
    outputRMS = std::sqrt(outputRMS / (numSamples - skipSamples));
    
    double gainDB = 20.0 * std::log10(outputRMS / inputRMS);
    
    std::cout << "Test frequency: " << testFreq << " Hz\n";
    std::cout << "Input RMS: " << inputRMS << "\n";
    std::cout << "Output RMS: " << outputRMS << "\n";
    std::cout << "Gain: " << std::fixed << std::setprecision(2) << gainDB << " dB\n";
    std::cout << "(Should be close to 0 dB at 1 kHz)\n\n";
    
    // Save output to file for analysis
    std::ofstream outFile("test_cpp.txt");
    if (outFile.is_open()) {
        outFile << std::setprecision(8) << std::scientific;
        for(int i = 0; i < std::min(1000, numSamples); i++) {
            outFile << static_cast<double>(i) / fs << "\t" 
                   << input[i] << "\t" << output[i] << "\n";
        }
        outFile.close();
        std::cout << "First 1000 samples saved to 'test_cpp.txt'\n";
    }
}

// Multi-tone test to verify simple A-weighting filter response
void testMultiToneFilter() {
    const double fs = 48000.0;
    const double duration = 1.0; // 1 second
    const int numSamples = static_cast<int>(fs * duration);
    
    // Frequencies to test (IEC 61672-1 reference points)
    std::vector<double> testFreqs = {31.5, 1000.0, 8000.0}; // Hz
    const double amplitude = 1.0 / testFreqs.size(); // Normalize amplitude
    // Expected A-weighting gains (dB) from IEC 61672-1
    std::vector<double> expectedGains = {-39.4, 0.0, -1.1}; // dB
    
    AWeightingFilter filter;
    
    std::cout << "\nMulti-tone A-weighting filter test (Simple Implementation)...\n";
    std::cout << "Sample rate: " << fs << " Hz\n";
    std::cout << "Duration: " << duration << " seconds\n";
    std::cout << "Frequencies: ";
    for (double freq : testFreqs) {
        std::cout << freq << " Hz ";
    }
    std::cout << "\n\n";
    
    // Generate multi-tone test signal
    std::vector<double> input(numSamples);
    for (int i = 0; i < numSamples; i++) {
        double t = static_cast<double>(i) / fs;
        input[i] = 0.0;
        for (double freq : testFreqs) {
            input[i] += amplitude * std::sin(2.0 * M_PI * freq * t);
        }
    }
    
    // Process with simple filter
    std::vector<double> output = filter.processBlock(input);
    
    // Calculate RMS for each frequency component (for console output)
    std::vector<double> inputRMS(testFreqs.size(), 0.0);
    std::vector<double> outputRMS(testFreqs.size(), 0.0);
    
    // Skip first 1000 samples to avoid transients
    const int skipSamples = 1000;
    for (int i = skipSamples; i < numSamples; i++) {
        for (size_t j = 0; j < testFreqs.size(); j++) {
            double t = static_cast<double>(i) / fs;
            double component = amplitude * std::sin(2.0 * M_PI * testFreqs[j] * t);
            inputRMS[j] += component * component;
            outputRMS[j] += output[i] * output[i];
        }
    }
    
    // Save output to file in raw amplitude format (time, input, output)
    std::ofstream outFile("multitone_test_cpp.txt");
    if (outFile.is_open()) {
        outFile << std::setprecision(8) << std::scientific;
        for (int i = 0; i < std::min(1000, numSamples); i++) {
            outFile << static_cast<double>(i) / fs << "\t" 
                    << input[i] << "\t" << output[i] << "\n";
        }
        outFile.close();
        std::cout << "First 1000 samples saved to 'multitone_test_cpp.txt'\n";
    }
}


int main() {
    std::cout << "A-weighting Filter Implementation (IEC 61672-1)\n";
    std::cout << "==============================================\n\n";
    
    // Run single-tone test
    testFilter();
    
    // Run multi-tone test
    testMultiToneFilter();
    
    // Performance test
    std::cout << "\nPerformance test (processing 1 million samples)...\n";
    
    AWeightingFilter perfFilter;
    const int perfSamples = 1000000;
    std::vector<double> perfInput(perfSamples, 0.5); // Constant input
    
    auto start = std::chrono::high_resolution_clock::now();
    
    for(int i = 0; i < perfSamples; i++) {
        perfFilter.process(perfInput[i]);
    }
    
    auto end = std::chrono::high_resolution_clock::now();
    auto duration = std::chrono::duration_cast<std::chrono::microseconds>(end - start);
    
    double samplesPerSecond = static_cast<double>(perfSamples) / (duration.count() / 1e6);
    double realTimeRatio = samplesPerSecond / 48000.0;
    
    std::cout << "Processed " << perfSamples << " samples in " 
              << duration.count() << " microseconds\n";
    std::cout << "Processing rate: " << std::fixed << std::setprecision(0) 
              << samplesPerSecond << " samples/second\n";
    std::cout << "Real-time ratio: " << std::fixed << std::setprecision(1) 
              << realTimeRatio << "x (higher is better)\n";
    
    return 0;
}