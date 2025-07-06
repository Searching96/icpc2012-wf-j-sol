#!/usr/bin/env python3
"""
Create a readable assembly version with meaningful names and comments
"""

import re
import os

def create_readable_assembly():
    """Create a readable version of the assembly file"""
    
    # Read the original assembly file
    input_file = "solve_cpp.asm"
    output_file = "solve_cpp_human_readable.asm"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found")
        return
    
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Create readable version
    readable_content = []
    readable_content.extend([
        "; ================================================================================",
        "; HUMAN READABLE ASSEMBLY VERSION",
        "; ICPC 2012 WF Problem J - Spherical Flight Path",
        "; ================================================================================",
        ";",
        "; ALGORITHM: Calculate shortest flight path on sphere using great circles",
        "; INPUT: Sequence of waypoints (latitude, longitude)",
        "; OUTPUT: Total distance in kilometers",
        ";",
        "; KEY COMPONENTS:",
        "; 1. Point structure with x, y, z coordinates (24 bytes)",
        "; 2. Vector operations (add, subtract, multiply, normalize)",
        "; 3. Spherical coordinate conversion",
        "; 4. Great circle distance calculation",
        "; 5. Main loop to process waypoints",
        ";",
        "; REGISTER USAGE:",
        "; xmm0-xmm3: Floating point calculations",
        "; rcx, rdx, r8, r9: Function arguments",
        "; rax: Return values",
        "; rsp: Stack pointer",
        ";",
        "; MEMORY LAYOUT:",
        "; Point structure: [x:8][y:8][z:8] = 24 bytes",
        "; Double precision: 8 bytes per coordinate",
        ";",
        "",
    ])
    
    # Function mappings
    function_mappings = {
        '??H@YA?AUPoint@@AEBU0@0@Z': 'add_two_points',
        '??G@YA?AUPoint@@AEBU0@0@Z': 'subtract_two_points',
        '??D@YA?AUPoint@@AEBU0@N@Z': 'multiply_point_by_scalar',
        'main': 'main_program',
    }
    
    # Process the assembly
    lines = content.split('\n')
    current_function = None
    
    for line in lines:
        line = line.strip()
        
        # Skip unnecessary directives
        if line.startswith(('.file', '.def', '.scl', '.type', '.endef', '.set')):
            continue
        
        # Handle function definitions
        if '.globl' in line:
            for mangled, readable in function_mappings.items():
                if mangled in line:
                    readable_content.extend([
                        f"; ----------------------------------------",
                        f"; FUNCTION: {readable}",
                        f"; ----------------------------------------",
                        get_function_description(readable),
                        f".globl {readable}",
                    ])
                    current_function = readable
                    break
            if current_function is None and 'main' not in line:
                readable_content.append(line)
            continue
        
        # Handle function labels
        if ':' in line and current_function:
            for mangled, readable in function_mappings.items():
                if mangled in line:
                    readable_content.extend([
                        f"{readable}:",
                        f"; Begin {readable}",
                    ])
                    break
            continue
        
        # Handle function end
        if '# -- End function' in line:
            if current_function:
                readable_content.extend([
                    f"; End {current_function}",
                    "",
                ])
            current_function = None
            continue
        
        # Process instructions
        if line and not line.startswith('#'):
            # Replace mangled names in the line
            modified_line = line
            for mangled, readable in function_mappings.items():
                if mangled in modified_line:
                    modified_line = modified_line.replace(mangled, readable)
            
            # Add instruction comments
            comment = get_instruction_comment(modified_line)
            if comment:
                readable_content.append(f"    {modified_line:<50} ; {comment}")
            else:
                readable_content.append(f"    {modified_line}")
        elif line:
            readable_content.append(line)
    
    # Write the readable version
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(readable_content))
    
    print(f"Created human readable assembly: {output_file}")

def get_function_description(func_name):
    """Get description for a function"""
    descriptions = {
        'add_two_points': "; Adds two 3D points: result = point1 + point2",
        'subtract_two_points': "; Subtracts two 3D points: result = point1 - point2",
        'multiply_point_by_scalar': "; Multiplies point by scalar: result = point * scalar",
        'main_program': "; Main program: reads input, calculates distance, outputs result",
    }
    return descriptions.get(func_name, f"; Function: {func_name}")

def get_instruction_comment(line):
    """Get comment for an instruction"""
    
    # Floating point operations
    if 'movsd' in line:
        if 'qword ptr' in line:
            return "Load 64-bit double"
        else:
            return "Move double precision value"
    elif 'addsd' in line:
        return "Add two doubles"
    elif 'subsd' in line:
        return "Subtract two doubles"
    elif 'mulsd' in line:
        return "Multiply two doubles"
    elif 'divsd' in line:
        return "Divide two doubles"
    elif 'sqrtsd' in line:
        return "Square root of double"
    
    # Memory operations
    elif 'mov' in line and 'qword ptr' in line:
        return "Move 64-bit value"
    elif 'mov' in line and 'dword ptr' in line:
        return "Move 32-bit value"
    
    # Stack operations
    elif 'sub rsp' in line:
        return "Allocate stack space"
    elif 'add rsp' in line:
        return "Deallocate stack space"
    elif 'push' in line:
        return "Push to stack"
    elif 'pop' in line:
        return "Pop from stack"
    
    # Control flow
    elif 'call' in line:
        return "Function call"
    elif 'ret' in line:
        return "Return from function"
    elif line.startswith('j'):
        return "Jump instruction"
    
    # Comparison
    elif 'cmp' in line:
        return "Compare values"
    elif 'test' in line:
        return "Test values"
    
    return ""

def create_detailed_guide():
    """Create a detailed guide for understanding the assembly"""
    
    guide_content = """# Assembly Code Guide for ICPC 2012 WF Problem J

## Overview
This guide explains the assembly code generated from the C++ solution for the spherical flight path problem.

## Problem Summary
Calculate the shortest flight path on a sphere (Earth) given waypoints in latitude/longitude coordinates.

## Algorithm Steps
1. Read N waypoints (latitude, longitude pairs)
2. Convert each waypoint to 3D Cartesian coordinates on unit sphere
3. For each consecutive pair of waypoints:
   - Calculate great circle distance using dot product
   - Distance = Earth_radius × arccos(dot_product)
4. Sum all segment distances
5. Output total distance

## Key Data Structures

### Point Structure (24 bytes)
```
struct Point {
    double x;  // offset 0, 8 bytes
    double y;  // offset 8, 8 bytes  
    double z;  // offset 16, 8 bytes
};
```

### Memory Layout
- Each coordinate is a 64-bit double (8 bytes)
- Total Point size: 24 bytes
- Alignment: 8-byte aligned

## Function Descriptions

### add_two_points(result, point1, point2)
- Purpose: Vector addition of two 3D points
- Operation: result = point1 + point2
- Assembly: Loads coordinates, adds with addsd, stores result

### subtract_two_points(result, point1, point2)
- Purpose: Vector subtraction of two 3D points
- Operation: result = point1 - point2
- Assembly: Similar to addition but uses subsd

### multiply_point_by_scalar(result, point, scalar)
- Purpose: Multiply vector by scalar value
- Operation: result = point * scalar
- Assembly: Loads point coordinates, multiplies each by scalar

### main_program()
- Purpose: Main program logic
- Reads input, processes waypoints, calculates total distance
- Contains the main calculation loop

## Register Usage Patterns

### Floating Point Registers (SSE)
- xmm0: Primary floating point accumulator
- xmm1-xmm3: Temporary floating point values
- Used for all double-precision operations

### General Purpose Registers
- rcx: 1st argument (Windows x64 calling convention)
- rdx: 2nd argument
- r8: 3rd argument
- r9: 4th argument
- rax: Return value
- rsp: Stack pointer

## Common Assembly Patterns

### Loading a Double Value
```assembly
movsd xmm0, qword ptr [address]  ; Load 8-byte double into xmm0
```

### Adding Two Doubles
```assembly
movsd xmm0, qword ptr [addr1]    ; Load first double
addsd xmm0, qword ptr [addr2]    ; Add second double
```

### Storing Result
```assembly
movsd qword ptr [result], xmm0   ; Store xmm0 to memory
```

### Function Call Setup
```assembly
mov rcx, result_ptr              ; 1st argument
mov rdx, point1_ptr              ; 2nd argument  
mov r8, point2_ptr               ; 3rd argument
call function_name               ; Call function
```

## Mathematical Operations

### Spherical to Cartesian Conversion
```
x = cos(latitude) × cos(longitude)
y = cos(latitude) × sin(longitude)  
z = sin(latitude)
```

### Great Circle Distance
```
distance = R × arccos(dot_product(p1, p2))
```

Where:
- R = Earth radius (6371 km)
- p1, p2 = normalized points on unit sphere
- dot_product = x1×x2 + y1×y2 + z1×z2

## Performance Considerations

### SSE Instructions
- Uses packed SSE instructions for double precision
- Efficient 64-bit floating point operations
- Hardware-accelerated square root and trigonometric functions

### Memory Access
- Aligned memory access for better performance
- Efficient use of registers to minimize memory loads/stores
- Stack space allocation optimized by compiler

## Debugging Tips

### Key Memory Locations
- Watch Point structure offsets (0, 8, 16)
- Monitor xmm registers for floating point values
- Check stack pointer (rsp) for proper cleanup

### Common Issues
- Floating point precision errors
- Stack imbalance (mismatched push/pop)
- Calling convention violations
- Uninitialized floating point registers

## Tools for Analysis

### Disassemblers
- objdump -d (Linux/MinGW)
- dumpbin /disasm (Windows)
- IDA Pro, Ghidra (advanced)

### Debuggers
- GDB with assembly view
- Visual Studio debugger
- Intel VTune for performance analysis

This guide provides the foundation for understanding the assembly code structure and execution flow.
"""
    
    with open("assembly_understanding_guide.md", 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("Created detailed assembly guide: assembly_understanding_guide.md")

if __name__ == "__main__":
    print("Creating human readable assembly version...")
    create_readable_assembly()
    create_detailed_guide()
    print("Done!")
