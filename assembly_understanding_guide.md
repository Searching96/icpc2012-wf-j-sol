# Assembly Code Guide for ICPC 2012 WF Problem J

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
