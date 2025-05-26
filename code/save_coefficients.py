import json

def export_coefficients_for_cpp(b, a, filename="data/a_weighting_coeffs.json"):
    """Export filter coefficients in a format suitable for C++"""
    
    coeffs = {
        "filter_type": "A-weighting IEC 61672-1",
        "sample_rate": 48000,
        "order": len(a) - 1,
        "numerator_coeffs": b.tolist(),
        "denominator_coeffs": a.tolist(),
        "cpp_code_example": """
// C++ implementation example:
class AWeightingFilter {
private:
    static const int ORDER = """ + str(len(a)-1) + """;
    double b[""" + str(len(b)) + """] = {""" + ", ".join([f"{coeff:.15e}" for coeff in b]) + """};
    double a[""" + str(len(a)) + """] = {""" + ", ".join([f"{coeff:.15e}" for coeff in a]) + """};
    double w[""" + str(max(len(a), len(b))) + """] = {0}; // delay line
    
public:
    double process(double input) {
        // Direct Form II implementation
        w[0] = input;
        for(int i = 1; i < """ + str(len(a)) + """; i++) {
            w[0] -= a[i] * w[i];
        }
        
        double output = 0;
        for(int i = 0; i < """ + str(len(b)) + """; i++) {
            output += b[i] * w[i];
        }
        
        // Shift delay line
        for(int i = """ + str(max(len(a), len(b))-1) + """; i > 0; i--) {
            w[i] = w[i-1];
        }
        
        return output;
    }
};
"""
    }
    
    with open(filename, 'w') as f:
        json.dump(coeffs, f, indent=2)
    
    print(f"Coefficients exported to {filename}")
    print("\nFilter coefficients:")
    print(f"Numerator (b): {len(b)} coefficients")
    print(f"Denominator (a): {len(a)} coefficients")
    print(f"Filter order: {len(a)-1}")
    
    return coeffs