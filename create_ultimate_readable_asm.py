#!/usr/bin/env python3
"""
Ultimate Assembly Readability Tool
Creates the most readable version possible with:
- Meaningful function names
- Variable name annotations
- Algorithm explanations
- Visual formatting
- Cross-references to C++ code
"""

import re
import os

def create_ultimate_readable_assembly():
    """Create the ultimate readable version"""
    
    # Read the original assembly
    try:
        with open("solve_cpp.asm", 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        print("Error: solve_cpp.asm not found")
        return
    
    # Create the ultimate version
    output_lines = []
    
    # Header with complete documentation
    output_lines.extend([
        "; ################################################################################",
        "; #                                                                              #",
        "; #                    ULTIMATE READABLE ASSEMBLY VERSION                       #",
        "; #                                                                              #",
        "; #                ICPC 2012 World Finals - Problem J                           #",
        "; #                     Spherical Flight Path                                    #",
        "; #                                                                              #",
        "; ################################################################################",
        ";",
        "; PROBLEM STATEMENT:",
        "; Given a sequence of waypoints on Earth's surface (latitude, longitude),",
        "; calculate the shortest flight path distance using great circles.",
        ";",
        "; MATHEMATICAL APPROACH:",
        "; 1. Convert spherical coordinates to 3D Cartesian coordinates",
        "; 2. Calculate great circle distances between consecutive waypoints",
        "; 3. Sum all segment distances",
        ";",
        "; KEY FORMULAS:",
        "; - Spherical to Cartesian: x=cos(lat)*cos(lon), y=cos(lat)*sin(lon), z=sin(lat)",
        "; - Great circle distance: d = R * arccos(dot_product(p1, p2))",
        "; - Earth radius: R = 6371.0 km",
        ";",
        "; ASSEMBLY STRUCTURE:",
        "; - Point operations: add, subtract, multiply by scalar",
        "; - Vector operations: length, normalize, dot product",
        "; - Coordinate conversion functions",
        "; - Main calculation loop",
        ";",
        "; REGISTERS AND MEMORY:",
        "; - xmm0-xmm15: SSE floating point registers (64-bit doubles)",
        "; - rcx, rdx, r8, r9: Function arguments (Windows x64 calling convention)",
        "; - rax: Return value register",
        "; - rsp: Stack pointer",
        "; - Point structure: 24 bytes (3 doubles: x, y, z)",
        ";",
        "; CALLING CONVENTION (Windows x64):",
        "; - 1st arg: rcx, 2nd arg: rdx, 3rd arg: r8, 4th arg: r9",
        "; - FP args: xmm0, xmm1, xmm2, xmm3",
        "; - Return: rax (integer), xmm0 (floating point)",
        "; - Caller saves: rax, rcx, rdx, r8-r11, xmm0-xmm5",
        "; - Callee saves: rbx, rbp, rdi, rsi, rsp, r12-r15, xmm6-xmm15",
        ";",
        "",
    ])
    
    # Function descriptions
    function_descriptions = {
        'point_add': {
            'name': 'Vector Addition',
            'signature': 'Point add_points(Point* result, const Point* p1, const Point* p2)',
            'description': 'Adds two 3D points component-wise',
            'algorithm': 'result.x = p1.x + p2.x; result.y = p1.y + p2.y; result.z = p1.z + p2.z',
            'complexity': 'O(1) - 3 floating point additions'
        },
        'point_subtract': {
            'name': 'Vector Subtraction', 
            'signature': 'Point subtract_points(Point* result, const Point* p1, const Point* p2)',
            'description': 'Subtracts two 3D points component-wise',
            'algorithm': 'result.x = p1.x - p2.x; result.y = p1.y - p2.y; result.z = p1.z - p2.z',
            'complexity': 'O(1) - 3 floating point subtractions'
        },
        'point_multiply': {
            'name': 'Scalar Multiplication',
            'signature': 'Point multiply_point(Point* result, const Point* p, double scalar)',
            'description': 'Multiplies a 3D point by a scalar value',
            'algorithm': 'result.x = p.x * scalar; result.y = p.y * scalar; result.z = p.z * scalar',
            'complexity': 'O(1) - 3 floating point multiplications'
        },
        'main': {
            'name': 'Main Program',
            'signature': 'int main()',
            'description': 'Main program logic for calculating flight path',
            'algorithm': 'Read waypoints, convert coordinates, calculate distances, output result',
            'complexity': 'O(n) - where n is number of waypoints'
        }
    }
    
    # Process the assembly file
    lines = content.split('\n')
    current_function = None
    function_line_count = 0
    
    for line in lines:
        line = line.strip()
        
        # Skip unnecessary directives
        if line.startswith(('.file', '.def', '.scl', '.type', '.endef', '.set')):
            continue
        
        # Handle function definitions
        if '.globl' in line:
            # Map mangled names to readable names
            mangled_to_readable = {
                '??H@YA?AUPoint@@AEBU0@0@Z': 'point_add',
                '??G@YA?AUPoint@@AEBU0@0@Z': 'point_subtract', 
                '??D@YA?AUPoint@@AEBU0@N@Z': 'point_multiply',
                'main': 'main'
            }
            
            for mangled, readable in mangled_to_readable.items():
                if mangled in line:
                    current_function = readable
                    func_info = function_descriptions.get(readable, {})
                    
                    output_lines.extend([
                        "; " + "=" * 80,
                        f"; FUNCTION: {func_info.get('name', readable.upper())}",
                        "; " + "=" * 80,
                        f"; Signature: {func_info.get('signature', 'Unknown')}",
                        f"; Description: {func_info.get('description', 'No description')}",
                        f"; Algorithm: {func_info.get('algorithm', 'No algorithm description')}",
                        f"; Complexity: {func_info.get('complexity', 'Unknown')}",
                        ";",
                        "; REGISTER USAGE:",
                        "; rcx - Pointer to result structure",
                        "; rdx - Pointer to first operand",
                        "; r8  - Pointer to second operand (or scalar in xmm2)",
                        "; xmm0-xmm2 - Floating point temporary values",
                        "; rax - Return value (pointer to result)",
                        ";",
                        f".globl {readable}",
                    ])
                    function_line_count = 0
                    break
            continue
        
        # Handle function labels
        if ':' in line and current_function:
            mangled_names = ['@@', 'main']
            if any(name in line for name in mangled_names):
                output_lines.extend([
                    f"{current_function}:",
                    f"; BEGIN {current_function.upper()} IMPLEMENTATION",
                    f"; Line count will be tracked for complexity analysis",
                    "",
                ])
                continue
        
        # Handle function end
        if '# -- End function' in line:
            if current_function:
                output_lines.extend([
                    "",
                    f"; END {current_function.upper()} IMPLEMENTATION",
                    f"; Total assembly lines: {function_line_count}",
                    "; " + "-" * 80,
                    "",
                ])
            current_function = None
            function_line_count = 0
            continue
        
        # Process instructions with detailed comments
        if line and not line.startswith('#'):
            function_line_count += 1
            
            # Get detailed instruction explanation
            instruction_parts = line.split()
            if instruction_parts:
                opcode = instruction_parts[0]
                detailed_comment = get_detailed_instruction_comment(line, opcode)
                
                # Format with proper indentation and alignment
                formatted_line = f"    {line:<60} ; {detailed_comment}"
                output_lines.append(formatted_line)
        elif line:
            output_lines.append(line)
    
    # Add footer
    output_lines.extend([
        "",
        "; ################################################################################",
        "; #                               END OF PROGRAM                                #",
        "; ################################################################################",
        ";",
        "; PERFORMANCE NOTES:",
        "; - Uses SSE instructions for efficient floating point operations",
        "; - Optimized memory access patterns",
        "; - Minimal function call overhead",
        "; - Cache-friendly data structures",
        ";",
        "; ACCURACY CONSIDERATIONS:",
        "; - IEEE 754 double precision (15-17 significant decimal digits)",
        "; - Potential floating point rounding errors",
        "; - Suitable for Earth-scale distance calculations",
        ";",
        "; DEBUGGING HINTS:",
        "; - Set breakpoints on function entry/exit",
        "; - Watch xmm registers for floating point values",
        "; - Monitor Point structure memory layout",
        "; - Check stack alignment and cleanup",
        "",
    ])
    
    # Write the ultimate version
    with open("solve_cpp_ultimate_readable.asm", 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print("Created ultimate readable assembly: solve_cpp_ultimate_readable.asm")

def get_detailed_instruction_comment(line, opcode):
    """Get detailed comment for an instruction"""
    
    # Detailed instruction explanations
    detailed_explanations = {
        'movsd': {
            'desc': 'Move Scalar Double-Precision',
            'detail': 'Copies 64-bit double from source to destination'
        },
        'addsd': {
            'desc': 'Add Scalar Double-Precision',
            'detail': 'Adds two 64-bit doubles, stores result in destination'
        },
        'subsd': {
            'desc': 'Subtract Scalar Double-Precision',
            'detail': 'Subtracts source from destination double'
        },
        'mulsd': {
            'desc': 'Multiply Scalar Double-Precision',
            'detail': 'Multiplies two 64-bit doubles'
        },
        'divsd': {
            'desc': 'Divide Scalar Double-Precision',
            'detail': 'Divides destination by source double'
        },
        'sqrtsd': {
            'desc': 'Square Root Scalar Double-Precision',
            'detail': 'Computes square root of double-precision value'
        },
        'mov': {
            'desc': 'Move Data',
            'detail': 'Copies data from source to destination'
        },
        'sub': {
            'desc': 'Subtract',
            'detail': 'Integer subtraction operation'
        },
        'add': {
            'desc': 'Add',
            'detail': 'Integer addition operation'
        },
        'call': {
            'desc': 'Call Function',
            'detail': 'Pushes return address and jumps to function'
        },
        'ret': {
            'desc': 'Return from Function',
            'detail': 'Pops return address and jumps back to caller'
        },
        'push': {
            'desc': 'Push to Stack',
            'detail': 'Decrements stack pointer and stores value'
        },
        'pop': {
            'desc': 'Pop from Stack',
            'detail': 'Loads value from stack and increments stack pointer'
        }
    }
    
    # Get base explanation
    base_info = detailed_explanations.get(opcode, {'desc': 'Unknown', 'detail': 'No description'})
    
    # Add context-specific information
    context_info = ""
    
    # Memory access patterns
    if 'qword ptr' in line:
        if '[rdx]' in line:
            context_info = " | Accessing Point.x coordinate"
        elif '[rdx + 8]' in line:
            context_info = " | Accessing Point.y coordinate"
        elif '[rdx + 16]' in line:
            context_info = " | Accessing Point.z coordinate"
        elif '[rcx]' in line:
            context_info = " | Storing to result.x"
        elif '[rcx + 8]' in line:
            context_info = " | Storing to result.y"
        elif '[rcx + 16]' in line:
            context_info = " | Storing to result.z"
        elif '[rsp' in line:
            context_info = " | Stack variable access"
    
    # Register usage
    if 'xmm0' in line:
        context_info += " | Primary FP register"
    elif 'xmm1' in line:
        context_info += " | Secondary FP register"
    
    return f"{base_info['desc']}: {base_info['detail']}{context_info}"

def create_final_guide():
    """Create a comprehensive final guide"""
    
    guide_content = """# Complete Assembly Analysis Guide

## Files Generated

1. **solve_cpp_readable.asm** - Basic readable version with function names
2. **solve_cpp_human_readable.asm** - Enhanced version with detailed comments
3. **solve_cpp_annotated.asm** - Variable-annotated version
4. **solve_cpp_ultimate_readable.asm** - Most comprehensive readable version

## Understanding the Assembly

### Function Mapping
- C++ mangled names are converted to readable names
- Each function has detailed header documentation
- Parameter passing follows Windows x64 convention

### Memory Layout
- Point structure: 24 bytes (3 × 8-byte doubles)
- Stack grows downward
- Proper alignment for SSE instructions

### Key Patterns to Recognize

#### Point Addition Pattern
```assembly
movsd xmm0, qword ptr [rdx]      ; Load p1.x
addsd xmm0, qword ptr [r8]       ; Add p2.x  
movsd qword ptr [rcx], xmm0      ; Store result.x
```

#### Stack Frame Setup
```assembly
sub rsp, 32                      ; Allocate stack space
; ... function body ...
add rsp, 32                      ; Clean up stack
ret                              ; Return to caller
```

#### Floating Point Operations
```assembly
movsd xmm0, qword ptr [address]  ; Load double
mulsd xmm0, xmm1                 ; Multiply doubles
sqrtsd xmm0, xmm0                ; Square root
```

### Debugging Tips

1. **Set Breakpoints**: On function entry/exit
2. **Watch Registers**: xmm0-xmm3 for FP values
3. **Monitor Memory**: Point structure locations
4. **Check Stack**: Proper allocation/cleanup

### Performance Analysis

- **SSE Instructions**: Efficient FP operations
- **Memory Access**: Aligned for best performance
- **Function Calls**: Minimal overhead
- **Cache Usage**: Good locality of reference

## Tools for Further Analysis

### Disassemblers
- **objdump**: Basic disassembly
- **IDA Pro**: Advanced analysis
- **Ghidra**: Free alternative to IDA

### Debuggers
- **GDB**: Command-line debugging
- **Visual Studio**: GUI debugging
- **Intel VTune**: Performance profiling

### Assembly Learning Resources
- Intel Software Developer Manual
- Microsoft x64 calling convention documentation
- SSE instruction set reference
- Assembly language tutorials

This guide provides everything needed to understand and analyze the generated assembly code.
"""
    
    with open("complete_assembly_guide.md", 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("Created complete assembly guide: complete_assembly_guide.md")

if __name__ == "__main__":
    print("Creating ultimate readable assembly version...")
    create_ultimate_readable_assembly()
    create_final_guide()
    print("Done! Check the generated files for the most readable assembly possible.")
