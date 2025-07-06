#!/usr/bin/env python3
"""
Create a more readable version of the assembly file with:
- Human-readable function names
- Better variable names
- Comments explaining operations
- Simplified structure
"""

import re
import os

def create_readable_assembly():
    """Create a readable version of the assembly file"""
    
    # Read the original assembly file
    input_file = "solve_cpp.asm"
    output_file = "solve_cpp_readable.asm"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found")
        return
    
    with open(input_file, 'r') as f:
        content = f.read()
    
    # Function name mappings (based on C++ mangling patterns)
    function_mappings = {
        # Point operations
        '??H@YA?AUPoint@@AEBU0@0@Z': 'point_add',
        '??G@YA?AUPoint@@AEBU0@0@Z': 'point_subtract', 
        '??D@YA?AUPoint@@AEBU0@N@Z': 'point_multiply_scalar',
        '??$length@UPoint@@': 'point_length',
        '??$normalize@UPoint@@': 'point_normalize',
        '??$dot@UPoint@@': 'point_dot_product',
        '??$cross@UPoint@@': 'point_cross_product',
        
        # Math functions
        'main': 'main_function',
        '_Z4sqrtd': 'square_root',
        '_Z3cosd': 'cosine',
        '_Z3sind': 'sine',
        '_Z4acosf': 'arc_cosine',
        '_Z4atand': 'arc_tangent',
        '_Z4atan2dd': 'arc_tangent2',
        
        # String/IO functions
        'scanf': 'read_input',
        'printf': 'print_output',
        
        # Memory operations
        'memcpy': 'copy_memory',
        'memset': 'set_memory',
    }
    
    # Variable/register mappings for common patterns
    register_comments = {
        'xmm0': 'floating_point_accumulator',
        'xmm1': 'floating_point_temp1',
        'xmm2': 'floating_point_temp2',
        'xmm3': 'floating_point_temp3',
        'rax': 'return_value_register',
        'rbx': 'base_pointer',
        'rcx': 'counter_register',
        'rdx': 'data_register',
        'rsi': 'source_index',
        'rdi': 'destination_index',
        'rbp': 'base_pointer',
        'rsp': 'stack_pointer',
        'r8': 'argument_register_1',
        'r9': 'argument_register_2',
        'r10': 'temp_register_1',
        'r11': 'temp_register_2',
    }
    
    # Start creating readable version
    readable_content = []
    readable_content.append("; ========================================")
    readable_content.append("; Readable Assembly Version of C++ Solution")
    readable_content.append("; ICPC 2012 WF Problem J - Spherical Flight Path")
    readable_content.append("; ========================================")
    readable_content.append("")
    
    # Process line by line
    lines = content.split('\n')
    in_function = False
    current_function = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            readable_content.append("")
            continue
            
        # Skip some directives that aren't essential for readability
        if line.startswith(('.file', '.def', '.scl', '.type', '.endef', '.set', '@feat.00')):
            continue
            
        # Handle function definitions
        if '.globl' in line and any(func in line for func in function_mappings.keys()):
            for mangled, readable in function_mappings.items():
                if mangled in line:
                    readable_content.append(f"; Function: {readable}")
                    readable_content.append(f".globl {readable}")
                    current_function = readable
                    break
            continue
        
        # Handle function labels
        if ':' in line and any(func in line for func in function_mappings.keys()):
            for mangled, readable in function_mappings.items():
                if mangled in line:
                    readable_content.append(f"{readable}:")
                    readable_content.append(f"; Begin {readable}")
                    in_function = True
                    break
            continue
            
        # Handle function end
        if '# -- End function' in line:
            readable_content.append(f"; End {current_function}")
            readable_content.append("")
            in_function = False
            current_function = ""
            continue
        
        # Replace function names in calls
        modified_line = line
        for mangled, readable in function_mappings.items():
            if mangled in modified_line:
                modified_line = modified_line.replace(mangled, readable)
        
        # Add comments for common operations
        if in_function:
            comment = ""
            
            # Floating point operations
            if 'movsd' in modified_line:
                comment = "; Move double precision value"
            elif 'addsd' in modified_line:
                comment = "; Add double precision values"
            elif 'subsd' in modified_line:
                comment = "; Subtract double precision values"
            elif 'mulsd' in modified_line:
                comment = "; Multiply double precision values"
            elif 'divsd' in modified_line:
                comment = "; Divide double precision values"
            elif 'sqrtsd' in modified_line:
                comment = "; Square root of double precision value"
            
            # Memory operations
            elif 'mov' in modified_line and 'qword ptr' in modified_line:
                comment = "; Move 64-bit value"
            elif 'mov' in modified_line and 'dword ptr' in modified_line:
                comment = "; Move 32-bit value"
            
            # Stack operations
            elif 'push' in modified_line:
                comment = "; Push to stack"
            elif 'pop' in modified_line:
                comment = "; Pop from stack"
            elif 'sub rsp' in modified_line:
                comment = "; Allocate stack space"
            elif 'add rsp' in modified_line:
                comment = "; Deallocate stack space"
            
            # Control flow
            elif 'call' in modified_line:
                comment = "; Function call"
            elif 'ret' in modified_line:
                comment = "; Return from function"
            elif 'jmp' in modified_line:
                comment = "; Unconditional jump"
            elif modified_line.startswith('j') and len(modified_line) > 1:
                comment = "; Conditional jump"
            
            # Comparison operations
            elif 'cmp' in modified_line:
                comment = "; Compare values"
            elif 'test' in modified_line:
                comment = "; Test/bitwise AND"
            
            if comment:
                readable_content.append(f"    {modified_line:<40} {comment}")
            else:
                readable_content.append(f"    {modified_line}")
        else:
            readable_content.append(modified_line)
    
    # Write the readable version
    with open(output_file, 'w') as f:
        f.write('\n'.join(readable_content))
    
    print(f"Created readable assembly file: {output_file}")
    
    # Create a separate file with variable name mappings
    create_variable_guide()

def create_variable_guide():
    """Create a guide explaining variable names and memory layout"""
    
    guide_content = """# Assembly Variable Guide

## Register Usage Guide

### General Purpose Registers (64-bit)
- **rax**: Return value register / Accumulator
- **rbx**: Base register (callee-saved)
- **rcx**: Counter register / 1st argument (Windows)
- **rdx**: Data register / 2nd argument (Windows)
- **rsi**: Source index register
- **rdi**: Destination index register
- **rbp**: Base pointer (frame pointer)
- **rsp**: Stack pointer
- **r8**: 3rd argument register
- **r9**: 4th argument register
- **r10-r11**: Temporary registers (caller-saved)
- **r12-r15**: General purpose (callee-saved)

### Floating Point Registers (SSE)
- **xmm0**: 1st FP argument / FP return value
- **xmm1**: 2nd FP argument
- **xmm2**: 3rd FP argument
- **xmm3**: 4th FP argument
- **xmm4-xmm5**: Additional FP arguments
- **xmm6-xmm15**: Temporary FP registers

## Memory Layout Patterns

### Point Structure (24 bytes)
```
Offset 0:  double x     (8 bytes)
Offset 8:  double y     (8 bytes)
Offset 16: double z     (8 bytes)
```

### Common Stack Patterns
- `[rsp + offset]`: Local variables
- `[rbp + offset]`: Function parameters (positive offset)
- `[rbp - offset]`: Local variables (negative offset)

## Function Calling Convention (Windows x64)

### Integer/Pointer Arguments
1. rcx (1st argument)
2. rdx (2nd argument)
3. r8 (3rd argument)
4. r9 (4th argument)
5. Stack (additional arguments)

### Floating Point Arguments
1. xmm0 (1st FP argument)
2. xmm1 (2nd FP argument)
3. xmm2 (3rd FP argument)
4. xmm3 (4th FP argument)
5. Stack (additional arguments)

### Return Values
- Integer/Pointer: rax
- Floating Point: xmm0

## Common Assembly Patterns in this Code

### Point Addition
```assembly
movsd xmm0, qword ptr [point1_x]    ; Load point1.x
addsd xmm0, qword ptr [point2_x]    ; Add point2.x
movsd qword ptr [result_x], xmm0    ; Store result.x
```

### Vector Length Calculation
```assembly
; result = sqrt(x*x + y*y + z*z)
movsd xmm0, qword ptr [x]           ; Load x
mulsd xmm0, xmm0                    ; x*x
movsd xmm1, qword ptr [y]           ; Load y
mulsd xmm1, xmm1                    ; y*y
addsd xmm0, xmm1                    ; x*x + y*y
movsd xmm1, qword ptr [z]           ; Load z
mulsd xmm1, xmm1                    ; z*z
addsd xmm0, xmm1                    ; x*x + y*y + z*z
sqrtsd xmm0, xmm0                   ; sqrt(x*x + y*y + z*z)
```

### Function Prologue/Epilogue
```assembly
; Prologue
sub rsp, 32                         ; Allocate stack space
.seh_stackalloc 32                  ; SEH info for debugging

; Epilogue
add rsp, 32                         ; Deallocate stack space
ret                                 ; Return to caller
```
"""
    
    with open("assembly_variable_guide.md", 'w') as f:
        f.write(guide_content)
    
    print("Created variable guide: assembly_variable_guide.md")

def create_annotated_version():
    """Create a heavily annotated version focusing on the main algorithm"""
    
    # Read the C++ source to understand the algorithm
    try:
        with open("main.cpp", 'r') as f:
            cpp_content = f.read()
    except:
        print("Warning: Could not read main.cpp for algorithm context")
        cpp_content = ""
    
    annotated_content = []
    annotated_content.append("; ========================================")
    annotated_content.append("; HEAVILY ANNOTATED ASSEMBLY VERSION")
    annotated_content.append("; ICPC 2012 WF Problem J - Spherical Flight Path")
    annotated_content.append("; ========================================")
    annotated_content.append(";")
    annotated_content.append("; ALGORITHM OVERVIEW:")
    annotated_content.append("; 1. Read flight path points from input")
    annotated_content.append("; 2. For each segment, calculate great circle distance")
    annotated_content.append("; 3. Use spherical geometry formulas")
    annotated_content.append("; 4. Sum all segment distances")
    annotated_content.append("; 5. Output total distance")
    annotated_content.append(";")
    annotated_content.append("; KEY MATHEMATICAL CONCEPTS:")
    annotated_content.append("; - Great circle distance on a sphere")
    annotated_content.append("; - Spherical coordinates (lat, lon)")
    annotated_content.append("; - Dot product and cross product of 3D vectors")
    annotated_content.append("; - Arc length calculations")
    annotated_content.append("; ========================================")
    annotated_content.append("")
    
    with open("solve_cpp_annotated.asm", 'w') as f:
        f.write('\n'.join(annotated_content))
    
    print("Created annotated assembly file: solve_cpp_annotated.asm")

if __name__ == "__main__":
    print("Creating readable assembly versions...")
    create_readable_assembly()
    create_annotated_version()
    print("Done!")
