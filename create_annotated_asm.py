#!/usr/bin/env python3
"""
Generate assembly with meaningful variable names by analyzing C++ structure
"""

import re
import os

def analyze_cpp_variables():
    """Analyze C++ code to extract variable names and their usage"""
    
    try:
        with open("main.cpp", 'r') as f:
            cpp_content = f.read()
    except:
        print("Warning: Could not read main.cpp")
        return {}
    
    # Extract variable information
    variables = {}
    
    # Find variable declarations
    var_patterns = [
        r'double\s+(\w+)',
        r'int\s+(\w+)',
        r'Point\s+(\w+)',
        r'vector<Point>\s+(\w+)',
        r'for\s*\(\s*int\s+(\w+)',
    ]
    
    for pattern in var_patterns:
        matches = re.findall(pattern, cpp_content)
        for match in matches:
            if match not in ['double', 'int', 'Point', 'vector', 'for']:
                variables[match] = 'local_var'
    
    # Find function parameters
    func_pattern = r'(\w+)\s+(\w+)\s*\(([^)]*)\)'
    for match in re.finditer(func_pattern, cpp_content):
        func_name = match.group(2)
        params = match.group(3)
        if params:
            param_matches = re.findall(r'(\w+)\s+(\w+)', params)
            for param_type, param_name in param_matches:
                variables[param_name] = f'param_{func_name}'
    
    return variables

def create_annotated_assembly():
    """Create assembly with variable annotations"""
    
    # Analyze C++ variables
    cpp_vars = analyze_cpp_variables()
    
    # Read the original assembly
    try:
        with open("solve_cpp.asm", 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except:
        print("Error: solve_cpp.asm not found")
        return
    
    # Create annotated version
    output_lines = []
    
    # Header
    output_lines.extend([
        "; ================================================================================",
        "; ANNOTATED ASSEMBLY WITH VARIABLE NAMES",
        "; Generated from C++ source analysis",
        "; ================================================================================",
        "",
    ])
    
    # Add variable mapping
    if cpp_vars:
        output_lines.append("; DETECTED C++ VARIABLES:")
        for var, context in cpp_vars.items():
            output_lines.append(f"; {var} - {context}")
        output_lines.append(";")
    
    # Memory offset mappings for common patterns
    offset_mappings = {
        '[rsp]': 'stack_var_0',
        '[rsp + 8]': 'stack_var_1', 
        '[rsp + 16]': 'stack_var_2',
        '[rsp + 24]': 'stack_var_3',
        '[rsp + 32]': 'stack_var_4',
        '[rdx]': 'point_x',
        '[rdx + 8]': 'point_y',
        '[rdx + 16]': 'point_z',
        '[rcx]': 'result_x',
        '[rcx + 8]': 'result_y',
        '[rcx + 16]': 'result_z',
    }
    
    # Process each line
    lines = content.split('\n')
    in_function = False
    
    for line in lines:
        original_line = line
        line = line.strip()
        
        # Skip directives
        if line.startswith(('.file', '.def', '.scl', '.type', '.endef')):
            continue
        
        # Detect function starts
        if 'main:' in line or ('@@' in line and ':' in line):
            in_function = True
            output_lines.append(line)
            continue
        
        # Detect function ends
        if '# -- End function' in line:
            in_function = False
            output_lines.append(line)
            continue
        
        # Process instructions
        if in_function and line:
            # Add meaningful comments for memory operations
            annotated_line = line
            comment = ""
            
            # Check for Point structure access patterns
            if 'qword ptr [' in line:
                for pattern, meaning in offset_mappings.items():
                    if pattern in line:
                        comment = f" ; Access {meaning}"
                        break
            
            # Check for floating point operations
            if 'movsd' in line and 'qword ptr' in line:
                if not comment:
                    comment = " ; Load double precision coordinate"
            elif 'addsd' in line:
                comment = " ; Add coordinates"
            elif 'subsd' in line:
                comment = " ; Subtract coordinates"
            elif 'mulsd' in line:
                comment = " ; Multiply coordinate"
            
            output_lines.append(f"    {annotated_line:<50}{comment}")
        elif line:
            output_lines.append(line)
    
    # Write the annotated version
    with open("solve_cpp_annotated.asm", 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print("Created annotated assembly: solve_cpp_annotated.asm")

def create_variable_mapping_guide():
    """Create a guide showing variable mappings"""
    
    guide_content = """# Variable Mapping Guide

## Assembly to C++ Variable Correspondence

### Memory Layout Understanding

#### Point Structure Access
```cpp
// C++ Code
struct Point {
    double x, y, z;
};
Point p;
```

```assembly
; Assembly equivalent
; Point p is allocated 24 bytes on stack
; p.x at [address + 0]
; p.y at [address + 8] 
; p.z at [address + 16]
```

#### Common Patterns

##### Loading Point Coordinates
```cpp
// C++ Code
double x = p.x;
double y = p.y;
double z = p.z;
```

```assembly
; Assembly equivalent
movsd xmm0, qword ptr [rdx]      ; Load p.x into xmm0
movsd xmm1, qword ptr [rdx + 8]  ; Load p.y into xmm1
movsd xmm2, qword ptr [rdx + 16] ; Load p.z into xmm2
```

##### Point Addition
```cpp
// C++ Code
Point result = p1 + p2;
// result.x = p1.x + p2.x;
// result.y = p1.y + p2.y;
// result.z = p1.z + p2.z;
```

```assembly
; Assembly equivalent
movsd xmm0, qword ptr [rdx]      ; Load p1.x
addsd xmm0, qword ptr [r8]       ; Add p2.x
movsd qword ptr [rcx], xmm0      ; Store result.x

movsd xmm0, qword ptr [rdx + 8]  ; Load p1.y
addsd xmm0, qword ptr [r8 + 8]   ; Add p2.y
movsd qword ptr [rcx + 8], xmm0  ; Store result.y

movsd xmm0, qword ptr [rdx + 16] ; Load p1.z
addsd xmm0, qword ptr [r8 + 16]  ; Add p2.z
movsd qword ptr [rcx + 16], xmm0 ; Store result.z
```

### Register Usage Conventions

#### Function Arguments (Windows x64)
- rcx: 1st argument (often result pointer)
- rdx: 2nd argument (often first operand pointer)
- r8:  3rd argument (often second operand pointer)
- r9:  4th argument (often scalar value)

#### Floating Point Operations
- xmm0: Primary floating point register
- xmm1-xmm3: Temporary floating point values
- Used for all double-precision calculations

#### Stack Variables
- [rsp + offset]: Local variables
- [rsp + 0]: First local variable
- [rsp + 8]: Second local variable
- etc.

### Function Naming Patterns

#### C++ Mangled Names → Readable Names
- `??H@YA?AUPoint@@AEBU0@0@Z` → `add_two_points`
- `??G@YA?AUPoint@@AEBU0@0@Z` → `subtract_two_points`
- `??D@YA?AUPoint@@AEBU0@N@Z` → `multiply_point_by_scalar`

#### Common Function Signatures
```cpp
Point add_two_points(Point& result, const Point& p1, const Point& p2);
Point subtract_two_points(Point& result, const Point& p1, const Point& p2);
Point multiply_point_by_scalar(Point& result, const Point& p, double scalar);
```

### Debugging with Variable Names

#### Memory Watchpoints
- Set breakpoints on Point structure access
- Watch for coordinate modifications
- Monitor floating point register changes

#### Stack Frame Analysis
- Track local variable allocation
- Monitor stack pointer changes
- Verify function parameter passing

#### Example Debugging Session
```
1. Set breakpoint at point addition function
2. Watch xmm0 register for coordinate values
3. Check memory at [rcx], [rcx+8], [rcx+16] for result
4. Verify stack cleanup after function return
```

This guide helps bridge the gap between high-level C++ code and low-level assembly implementation.
"""
    
    with open("variable_mapping_guide.md", 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print("Created variable mapping guide: variable_mapping_guide.md")

if __name__ == "__main__":
    print("Creating annotated assembly with variable names...")
    create_annotated_assembly()
    create_variable_mapping_guide()
    print("Done!")
