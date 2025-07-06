# ICPC 2012 World Finals - Problem J: Spherical Flight Path

## Problem Description
Calculate the shortest flight path on Earth's surface given a sequence of waypoints using great circle distances.

## Solutions Provided
- **C++ Solution**: `main.cpp` - Main solution with comprehensive algorithm
- **C Solution**: `main.c` - Alternative C implementation
- **Assembly Analysis**: Multiple readable assembly versions for educational purposes

## Files Overview

### Source Code
- `main.cpp` - C++ solution (recommended)
- `main.c` - C solution (alternative)

### Test Data
- `shortest/` - Directory containing test cases (input/output files)

### Testing Scripts
- `test_cpp_solution.py` - Test the C++ solution
- `test_c_solution.py` - Test the C solution
- `test_cpp_asm_solution.py` - Test assembly version

### Assembly Analysis (Educational)
- `solve_cpp_ultimate_readable.asm` - Most readable assembly version
- `solve_cpp_human_readable.asm` - Enhanced readable assembly
- `solve_cpp_annotated.asm` - Variable-annotated assembly
- `solve_cpp_readable.asm` - Basic readable assembly

### Documentation
- `assembly_understanding_guide.md` - Detailed assembly analysis guide
- `variable_mapping_guide.md` - C++ to assembly mapping guide
- `complete_assembly_guide.md` - Complete reference for all files
- `assembly_variable_guide.md` - Register usage and memory layout

### Tools
- `create_ultimate_readable_asm.py` - Generate readable assembly
- `create_annotated_asm.py` - Generate annotated assembly
- `list_generated_files.py` - List all generated files
- Other assembly generation scripts

## How to Use

### Run the C++ Solution
```bash
g++ -o main main.cpp -std=c++17
./main < shortest/input1.in
```

### Test All Cases
```bash
python test_cpp_solution.py
```

### Generate Readable Assembly
```bash
python create_ultimate_readable_asm.py
```

## Algorithm Overview
1. Convert latitude/longitude coordinates to 3D Cartesian coordinates
2. Calculate great circle distances between consecutive waypoints
3. Sum all segment distances using spherical geometry

## Mathematical Formulas
- **Spherical to Cartesian**: `x = cos(lat)*cos(lon)`, `y = cos(lat)*sin(lon)`, `z = sin(lat)`
- **Great Circle Distance**: `d = R * arccos(dot_product(p1, p2))`
- **Earth Radius**: `R = 6371.0 km`

## Educational Value
This project demonstrates:
- Spherical geometry calculations
- C++ to assembly code analysis
- Floating-point precision handling
- Algorithm optimization techniques
- Cross-platform development practices

## Contest Information
- **Contest**: ICPC 2012 World Finals
- **Problem**: J - Spherical Flight Path
- **Category**: Computational geometry, spherical mathematics

## License
This is educational content for competitive programming practice. Original problem from ICPC 2012 World Finals.
