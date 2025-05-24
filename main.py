from code.design import design_a_weighting_filter
from code.filter_plot import plot_a_weighting_response
from code.test import test_real_time_filtering
from code.save_coefficients import export_coefficients_for_cpp


# Script to design and test A-weighting filter according to IEC 61672-1
if __name__ == "__main__":
    print("Designing A-weighting filter according to IEC 61672-1...")
    
    # Design the filter
    b, a, f1, f2, f3, f4 = design_a_weighting_filter(fs=48000)
    
    print(f"Pole frequencies: f1={f1}, f2={f2}, f3={f3}, f4={f4} Hz")
    print(f"Filter order: {len(a)-1}")
    
    # Plot frequency response with comparison to your original method
    w, h_db = plot_a_weighting_response(b, a)
    
    # Test real-time filtering
    print("\nTesting real-time implementation...")
    y_manual, y_scipy = test_real_time_filtering(b, a)
    
    # Export for C++
    coeffs = export_coefficients_for_cpp(b, a)
    
    print("\nA-weighting filter design complete!")
    print("The filter coefficients are ready for C++ real-time implementation.")