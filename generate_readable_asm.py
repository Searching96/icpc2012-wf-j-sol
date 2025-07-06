#!/usr/bin/env python3
"""
Script to generate more readable assembly from C++ code
"""
import subprocess
import os
import sys
from pathlib import Path

def generate_readable_assembly():
    """Generate readable assembly with various techniques"""
    
    print("🔧 Generating readable assembly files...")
    
    # Technique 1: No optimization + debug symbols
    print("\n1️⃣ Generating unoptimized assembly with debug symbols...")
    try:
        result = subprocess.run([
            "g++", "-S", "-O0", "-g", "-fverbose-asm", 
            "-fno-omit-frame-pointer", "-masm=intel",
            "main.cpp", "-o", "main_readable.s"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Created main_readable.s (unoptimized with debug info)")
        else:
            print(f"❌ Failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Technique 2: Mixed source and assembly
    print("\n2️⃣ Generating mixed source/assembly listing...")
    try:
        # First compile with debug info
        subprocess.run([
            "g++", "-c", "-O0", "-g", "main.cpp", "-o", "main_debug.o"
        ], capture_output=True, text=True)
        
        # Then disassemble with source
        result = subprocess.run([
            "objdump", "-S", "-M", "intel", "main_debug.o"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            with open("main_mixed.s", "w") as f:
                f.write(result.stdout)
            print("✅ Created main_mixed.s (mixed source/assembly)")
        else:
            print(f"❌ objdump failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Technique 3: Annotated assembly with comments
    print("\n3️⃣ Generating heavily commented assembly...")
    try:
        result = subprocess.run([
            "g++", "-S", "-O1", "-g", "-fverbose-asm",
            "-fno-omit-frame-pointer", "-masm=intel",
            "-fstack-protector-all", "-fcf-protection=none",
            "main.cpp", "-o", "main_commented.s"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Created main_commented.s (heavily commented)")
        else:
            print(f"❌ Failed: {result.stderr}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Technique 4: Create a simplified version with manual annotations
    print("\n4️⃣ Creating manually annotated version...")
    create_manually_annotated_version()
    
    print("\n📋 Generated assembly files:")
    asm_files = [
        ("main_readable.s", "Unoptimized with debug symbols"),
        ("main_mixed.s", "Mixed source/assembly from objdump"),
        ("main_commented.s", "Heavily commented by compiler"),
        ("main_manual.s", "Manually annotated simple version")
    ]
    
    for filename, description in asm_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  📄 {filename} ({size:,} bytes) - {description}")
    
    return True

def create_manually_annotated_version():
    """Create a manually annotated assembly version"""
    manual_asm = '''# Manually Annotated Assembly for Flight Path Problem
# This is a simplified, readable version with clear variable names
# Generated from main.cpp

.intel_syntax noprefix
.text

# Global constants
.section .rodata
earth_radius:     .quad 0x40b8f00000000000  # 6370.0
pi_constant:      .quad 0x400921fb54442d18  # 3.14159265358979323846
epsilon:          .quad 0x3e45798ee2308c3a  # 1e-9

# Function: convert_lat_lon_to_xyz
# Input: latitude (degrees), longitude (degrees)  
# Output: x, y, z coordinates
.globl convert_lat_lon_to_xyz
convert_lat_lon_to_xyz:
    push rbp
    mov rbp, rsp
    
    # Convert degrees to radians
    # lat_rad = lat_deg * PI / 180
    movsd xmm2, [pi_constant]
    mulsd xmm0, xmm2              # lat_deg * PI
    mov rax, 0x4066800000000000   # 180.0
    movsd xmm3, [rax]
    divsd xmm0, xmm3              # lat_rad = lat_deg * PI / 180
    
    # lon_rad = lon_deg * PI / 180  
    mulsd xmm1, xmm2              # lon_deg * PI
    divsd xmm1, xmm3              # lon_rad = lon_deg * PI / 180
    
    # Calculate x = R * cos(lat) * cos(lon)
    movsd xmm4, [earth_radius]
    call cos                      # cos(lat_rad)
    mulsd xmm0, xmm4              # R * cos(lat)
    movsd xmm5, xmm0              # store R * cos(lat)
    
    movsd xmm0, xmm1              # lon_rad
    call cos                      # cos(lon_rad)
    mulsd xmm0, xmm5              # x = R * cos(lat) * cos(lon)
    
    # Similar calculations for y and z...
    # (truncated for brevity)
    
    pop rbp
    ret

# Function: calculate_great_circle_distance
# Input: point1 (x1,y1,z1), point2 (x2,y2,z2)
# Output: distance in km
.globl calculate_great_circle_distance
calculate_great_circle_distance:
    push rbp
    mov rbp, rsp
    
    # Normalize vectors
    # u1 = normalize(p1)
    # u2 = normalize(p2)
    
    # Calculate dot product
    # dot_product = u1.x * u2.x + u1.y * u2.y + u1.z * u2.z
    
    # Clamp to [-1, 1] range
    # dot_product = max(-1.0, min(1.0, dot_product))
    
    # Calculate angle
    # angle = acos(dot_product)
    
    # Calculate distance
    # distance = angle * earth_radius
    
    pop rbp
    ret

# Main function with readable variable names
.globl main
main:
    push rbp
    mov rbp, rsp
    sub rsp, 64                   # allocate stack space for local variables
    
    # Local variables (stack offsets):
    # -8(rbp)  = num_airports
    # -16(rbp) = fuel_range  
    # -24(rbp) = num_queries
    # -32(rbp) = source_airport
    # -40(rbp) = dest_airport
    # -48(rbp) = fuel_capacity
    
read_input_loop:
    # Read N (number of airports) and R (fuel range)
    lea rdi, [rip + input_format]     # "%d %lf"
    lea rsi, [rbp - 8]                # &num_airports
    lea rdx, [rbp - 16]               # &fuel_range
    call scanf
    
    # Check for end of input
    cmp eax, 2
    jne end_program
    
    # Read airport coordinates
    mov rcx, [rbp - 8]                # num_airports
    test rcx, rcx
    jz read_input_loop
    
process_airports_loop:
    # Read latitude and longitude for each airport
    lea rdi, [rip + coord_format]     # "%lf %lf"
    lea rsi, [rbp - 56]               # &longitude
    lea rdx, [rbp - 64]               # &latitude
    call scanf
    
    # Convert to XYZ coordinates
    movsd xmm0, [rbp - 64]            # latitude
    movsd xmm1, [rbp - 56]            # longitude
    call convert_lat_lon_to_xyz
    
    # Store in airport array
    # ... (airport storage code)
    
    loop process_airports_loop
    
    # Build graph and process queries
    call build_flight_graph
    call process_flight_queries
    
    jmp read_input_loop

end_program:
    mov rax, 0                        # return 0
    add rsp, 64                       # deallocate stack
    pop rbp
    ret

# Data section with readable names
.section .data
input_format:     .asciz "%d %lf"
coord_format:     .asciz "%lf %lf"
query_format:     .asciz "%d %d %lf"
output_format:    .asciz "%.3f\\n"
impossible_msg:   .asciz "impossible\\n"
case_format:      .asciz "Case %d:\\n"

# BSS section for variables
.section .bss
.lcomm airport_coordinates, 8000     # space for airport coordinates
.lcomm distance_matrix, 40000        # space for distance matrix
.lcomm case_counter, 4               # current case number
'''
    
    with open("main_manual.s", "w") as f:
        f.write(manual_asm)
    
    print("✅ Created main_manual.s (manually annotated)")

def create_compilation_guide():
    """Create a guide for generating readable assembly"""
    guide = '''# Guide: Generating Readable Assembly from C++

## Compiler Flags for Readable Assembly

### 1. Basic Readable Assembly
```bash
g++ -S -O0 -g -fverbose-asm -masm=intel main.cpp -o main_readable.s
```
- `-S`: Generate assembly instead of object code
- `-O0`: No optimization (keeps variable names)
- `-g`: Include debug information
- `-fverbose-asm`: Add comments to assembly
- `-masm=intel`: Use Intel syntax (more readable than AT&T)

### 2. Mixed Source/Assembly
```bash
g++ -c -O0 -g main.cpp -o main_debug.o
objdump -S -M intel main_debug.o > main_mixed.s
```
- Interleaves original C++ source with assembly
- Shows which assembly corresponds to which C++ code

### 3. Heavily Commented Assembly
```bash
g++ -S -O1 -g -fverbose-asm -fno-omit-frame-pointer main.cpp -o main_commented.s
```
- `-fno-omit-frame-pointer`: Keep frame pointers for debugging
- Light optimization (-O1) while keeping readability

### 4. Function Name Preservation
```bash
g++ -S -O0 -g -fno-inline -fno-omit-frame-pointer main.cpp -o main_functions.s
```
- `-fno-inline`: Prevent function inlining
- Preserves individual function boundaries

## Key Techniques for Readable Assembly

1. **Use No Optimization (-O0)**
   - Keeps all variables in memory
   - Preserves function call structure
   - Maintains clear code flow

2. **Add Debug Symbols (-g)**
   - Includes original variable names in debug info
   - Enables source-level debugging
   - Required for mixed source/assembly

3. **Verbose Assembly (-fverbose-asm)**
   - Adds explanatory comments
   - Shows register usage
   - Explains memory operations

4. **Intel Syntax (-masm=intel)**
   - More readable than AT&T syntax
   - Destination comes first: `mov eax, 5`
   - No % or $ prefixes needed

5. **Manual Annotation**
   - Add your own comments explaining algorithms
   - Use meaningful label names
   - Document function parameters and return values

## Example Readable Assembly Features

```assembly
# Clear function names
calculate_great_circle_distance:
    push rbp
    mov rbp, rsp
    
    # Meaningful variable names in comments
    movsd xmm0, [rbp-8]     # latitude_degrees
    movsd xmm1, [rbp-16]    # longitude_degrees
    
    # Algorithm explanation
    # Convert degrees to radians: rad = deg * PI / 180
    mulsd xmm0, [pi_constant]
    divsd xmm0, [degrees_to_radians]
    
    # Clear section labels
.calculate_distance:
    # Distance = acos(dot_product) * earth_radius
    call acos
    mulsd xmm0, [earth_radius]
    ret
```

## Tools for Analysis

1. **objdump**: Disassemble with source
2. **readelf**: Examine symbol tables
3. **addr2line**: Convert addresses to source lines
4. **gdb**: Interactive debugging with assembly view

## Limitations

- C++ name mangling still occurs
- Heavy optimization eliminates variables
- Template instantiation creates complex names
- Modern CPUs reorder instructions

## Best Practices

1. Compile with `-O0 -g` for maximum readability
2. Use meaningful function and variable names in C++
3. Add comments explaining complex algorithms
4. Consider writing critical sections in inline assembly
5. Use debugging tools to map assembly back to source
'''
    
    with open("assembly_guide.md", "w") as f:
        f.write(guide)
    
    print("✅ Created assembly_guide.md")

def main():
    # Change to the script's directory (relative path handling)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("🔧 Generating readable assembly files from C++ code...")
    print("This will create several versions with different readability techniques.")
    
    # Check if main.cpp exists
    if not os.path.exists("main.cpp"):
        print("❌ main.cpp not found!")
        return 1
    
    # Generate readable assembly files
    generate_readable_assembly()
    
    # Create compilation guide
    create_compilation_guide()
    
    print("\n📖 Usage Guide:")
    print("1. main_readable.s    - Unoptimized with verbose comments")
    print("2. main_mixed.s       - Source code interleaved with assembly")
    print("3. main_commented.s   - Heavily commented by compiler")
    print("4. main_manual.s      - Manually annotated example")
    print("5. assembly_guide.md  - Complete guide for readable assembly")
    
    print("\n💡 Tips for Maximum Readability:")
    print("- Use main_mixed.s to see C++ source with corresponding assembly")
    print("- Use main_readable.s for clearest variable tracking")
    print("- Refer to assembly_guide.md for compilation techniques")
    print("- Consider adding inline assembly for critical sections")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
