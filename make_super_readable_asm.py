#!/usr/bin/env python3
"""
Advanced Assembly Readability Tool
- Analyzes C++ source code to understand the algorithm
- Creates human-readable assembly with meaningful variable names
- Provides detailed explanations of each code section
"""

import re
import os

def analyze_cpp_source():
    """Analyze the C++ source to understand the algorithm structure"""
    
    try:
        with open("main.cpp", 'r') as f:
            cpp_content = f.read()
    except:
        print("Warning: Could not read main.cpp")
        return {}
    
    # Extract key information from C++ code
    info = {
        'structs': [],
        'functions': [],
        'variables': [],
        'constants': [],
        'algorithm_steps': []
    }
    
    # Find struct definitions
    struct_pattern = r'struct\s+(\w+)\s*\{([^}]+)\}'
    for match in re.finditer(struct_pattern, cpp_content):
        struct_name = match.group(1)
        struct_body = match.group(2)
        info['structs'].append({
            'name': struct_name,
            'body': struct_body.strip()
        })
    
    # Find function definitions
    func_pattern = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*\{'
    for match in re.finditer(func_pattern, cpp_content):
        return_type = match.group(1)
        func_name = match.group(2)
        if func_name not in ['if', 'for', 'while']:  # Skip control structures
            info['functions'].append({
                'name': func_name,
                'return_type': return_type
            })
    
    # Find constants
    const_pattern = r'const\s+\w+\s+(\w+)\s*=\s*([^;]+);'
    for match in re.finditer(const_pattern, cpp_content):
        const_name = match.group(1)
        const_value = match.group(2).strip()
        info['constants'].append({
            'name': const_name,
            'value': const_value
        })
    
    # Identify algorithm steps from comments
    comment_pattern = r'//\s*(.+)'
    for match in re.finditer(comment_pattern, cpp_content):
        comment = match.group(1).strip()
        if len(comment) > 10:  # Skip short comments
            info['algorithm_steps'].append(comment)
    
    return info

def create_super_readable_assembly():
    """Create the most readable assembly version possible"""
    
    # Analyze the C++ source
    cpp_info = analyze_cpp_source()
    
    # Read the original assembly
    try:
        with open("solve_cpp.asm", 'r') as f:
            asm_content = f.read()
    except:
        print("Error: solve_cpp.asm not found")
        return
    
    # Create the super readable version
    output_lines = []
    
    # Header with algorithm explanation
    output_lines.extend([
        "; ╔════════════════════════════════════════════════════════════════════════════════════╗",
        "; ║                    SUPER READABLE ASSEMBLY VERSION                                 ║",
        "; ║                 ICPC 2012 WF Problem J - Spherical Flight Path                    ║",
        "; ╚════════════════════════════════════════════════════════════════════════════════════╝",
        ";",
        "; PROBLEM DESCRIPTION:",
        "; Calculate the shortest flight path on a sphere (Earth) given a sequence of waypoints.",
        "; The path follows great circles between consecutive waypoints.",
        ";",
        "; ALGORITHM OVERVIEW:",
        "; 1. Read latitude/longitude coordinates for each waypoint",
        "; 2. Convert spherical coordinates to 3D Cartesian coordinates",
        "; 3. For each segment between waypoints:",
        ";    a. Calculate the great circle distance using spherical trigonometry",
        ";    b. Use the formula: distance = radius * arccos(dot_product(unit_vectors))",
        "; 4. Sum all segment distances",
        "; 5. Output the total distance",
        ";",
        "; KEY MATHEMATICAL CONCEPTS:",
        "; - Spherical coordinates: (latitude, longitude) -> (x, y, z)",
        "; - Great circle distance formula",
        "; - Dot product of unit vectors",
        "; - Arc cosine function",
        ";",
        "; COORDINATE SYSTEM:",
        "; - Earth radius: 6371 km",
        "; - Latitude: -90° to +90° (South to North)",
        "; - Longitude: -180° to +180° (West to East)",
        "; - Cartesian: x=East, y=North, z=Up",
        ";",
        "",
    ])
    
    # Add struct information
    if cpp_info.get('structs'):
        output_lines.append("; DATA STRUCTURES:")
        for struct in cpp_info['structs']:
            output_lines.append(f"; struct {struct['name']} {{")
            for line in struct['body'].split('\n'):
                if line.strip():
                    output_lines.append(f";     {line.strip()}")
            output_lines.append("; }")
        output_lines.append(";")
    
    # Add constants information
    if cpp_info.get('constants'):
        output_lines.append("; CONSTANTS:")
        for const in cpp_info['constants']:
            output_lines.append(f"; {const['name']} = {const['value']}")
        output_lines.append(";")
    
    # Function name mappings with detailed explanations
    function_explanations = {
        'point_add': {
            'description': 'Add two 3D points component-wise',
            'params': ['result_ptr', 'point1_ptr', 'point2_ptr'],
            'operation': 'result = point1 + point2'
        },
        'point_subtract': {
            'description': 'Subtract two 3D points component-wise',
            'params': ['result_ptr', 'point1_ptr', 'point2_ptr'],
            'operation': 'result = point1 - point2'
        },
        'point_multiply_scalar': {
            'description': 'Multiply a 3D point by a scalar value',
            'params': ['result_ptr', 'point_ptr', 'scalar'],
            'operation': 'result = point * scalar'
        },
        'point_length': {
            'description': 'Calculate the length (magnitude) of a 3D vector',
            'params': ['point_ptr'],
            'operation': 'return sqrt(x² + y² + z²)'
        },
        'point_normalize': {
            'description': 'Normalize a 3D vector to unit length',
            'params': ['result_ptr', 'point_ptr'],
            'operation': 'result = point / |point|'
        },
        'point_dot_product': {
            'description': 'Calculate dot product of two 3D vectors',
            'params': ['point1_ptr', 'point2_ptr'],
            'operation': 'return x1*x2 + y1*y2 + z1*z2'
        },
        'spherical_to_cartesian': {
            'description': 'Convert spherical coordinates to Cartesian',
            'params': ['result_ptr', 'latitude', 'longitude'],
            'operation': 'Convert (lat,lon) to (x,y,z) on unit sphere'
        },
        'great_circle_distance': {
            'description': 'Calculate great circle distance between two points',
            'params': ['point1_ptr', 'point2_ptr'],
            'operation': 'return acos(dot_product(normalize(p1), normalize(p2)))'
        },
        'main_function': {
            'description': 'Main program entry point',
            'params': [],
            'operation': 'Read input, calculate total distance, output result'
        }
    }
    
    # Process the assembly file
    lines = asm_content.split('\n')
    current_function = None
    in_function = False
    
    for line in lines:
        line = line.strip()
        
        # Skip unnecessary directives
        if line.startswith(('.file', '.def', '.scl', '.type', '.endef')):
            continue
        
        # Handle function starts
        if '.globl' in line and '@@' in line:
            # Try to map to a readable function name
            for mangled_part, readable_name in [
                ('??H@YA?AUPoint@@AEBU0@0@Z', 'point_add'),
                ('??G@YA?AUPoint@@AEBU0@0@Z', 'point_subtract'),
                ('??D@YA?AUPoint@@AEBU0@N@Z', 'point_multiply_scalar'),
                ('main', 'main_function'),
            ]:
                if mangled_part in line:
                    current_function = readable_name
                    output_lines.extend([
                        f"; ╔{'═' * 78}╗",
                        f"; ║ FUNCTION: {readable_name.upper():<65} ║",
                        f"; ╚{'═' * 78}╝",
                    ])
                    if readable_name in function_explanations:
                        func_info = function_explanations[readable_name]
                        output_lines.extend([
                            f"; Description: {func_info['description']}",
                            f"; Parameters: {', '.join(func_info['params'])}",
                            f"; Operation: {func_info['operation']}",
                        ])
                    output_lines.extend([
                        ";",
                        f".globl {readable_name}",
                    ])
                    break
            continue
        
        # Handle function labels
        if ':' in line and current_function and ('@@' in line or 'main' in line):
            output_lines.extend([
                f"{current_function}:",
                f"; ┌─ Begin {current_function} ─┐",
            ])
            in_function = True
            continue
        
        # Handle function end
        if '# -- End function' in line:
            if current_function:
                output_lines.extend([
                    f"; └─ End {current_function} ─┘",
                    "",
                ])
            in_function = False
            current_function = None
            continue
        
        # Process instructions within functions
        if in_function and line:
            processed_line = process_instruction(line)
            output_lines.append(processed_line)
        elif line:
            output_lines.append(line)
    
    # Write the super readable version
    with open("solve_cpp_super_readable.asm", 'w') as f:
        f.write('\n'.join(output_lines))
    
    print("Created super readable assembly: solve_cpp_super_readable.asm")

def process_instruction(line):
    """Process a single assembly instruction to make it more readable"""
    
    # Dictionary of instruction explanations
    instruction_explanations = {
        'movsd': 'Move 64-bit floating point value',
        'addsd': 'Add 64-bit floating point values',
        'subsd': 'Subtract 64-bit floating point values',
        'mulsd': 'Multiply 64-bit floating point values',
        'divsd': 'Divide 64-bit floating point values',
        'sqrtsd': 'Square root of 64-bit floating point',
        'mov': 'Move data',
        'sub': 'Subtract',
        'add': 'Add',
        'push': 'Push to stack',
        'pop': 'Pop from stack',
        'call': 'Call function',
        'ret': 'Return from function',
        'cmp': 'Compare values',
        'jmp': 'Jump unconditionally',
        'je': 'Jump if equal',
        'jne': 'Jump if not equal',
        'jl': 'Jump if less',
        'jg': 'Jump if greater',
        'test': 'Test (bitwise AND)',
    }
    
    # Register explanations
    register_explanations = {
        'xmm0': 'fp_result',
        'xmm1': 'fp_temp1',
        'xmm2': 'fp_temp2',
        'xmm3': 'fp_temp3',
        'rax': 'result',
        'rbx': 'base',
        'rcx': 'arg1',
        'rdx': 'arg2',
        'r8': 'arg3',
        'r9': 'arg4',
        'rsp': 'stack_ptr',
        'rbp': 'frame_ptr',
    }
    
    # Extract instruction
    if '\t' in line:
        instruction = line.split('\t')[0].strip()
    else:
        instruction = line.split(' ')[0].strip()
    
    # Get explanation
    explanation = instruction_explanations.get(instruction, '')
    
    # Format the line
    if explanation:
        return f"    {line:<50} ; {explanation}"
    else:
        return f"    {line}"

def create_algorithm_flowchart():
    """Create a text-based flowchart of the algorithm"""
    
    flowchart = """
# Algorithm Flowchart

```
START
  │
  ▼
┌─────────────────────────┐
│ Read number of points N │
└─────────────────────────┘
  │
  ▼
┌─────────────────────────┐
│ Initialize total = 0    │
└─────────────────────────┘
  │
  ▼
┌─────────────────────────┐
│ For i = 0 to N-1:       │
│   Read lat[i], lon[i]   │
└─────────────────────────┘
  │
  ▼
┌─────────────────────────┐
│ For i = 0 to N-2:       │
└─────────────────────────┘
  │
  ▼
┌─────────────────────────┐
│ Convert (lat[i], lon[i])│
│ to Cartesian point p1   │
└─────────────────────────┘
  │
  ▼
┌─────────────────────────┐
│ Convert (lat[i+1],      │
│ lon[i+1]) to point p2   │
└─────────────────────────┘
  │
  ▼
┌─────────────────────────┐
│ Calculate dot product   │
│ dot = p1 · p2           │
└─────────────────────────┘
  │
  ▼
┌─────────────────────────┐
│ Calculate angle         │
│ angle = acos(dot)       │
└─────────────────────────┘
  │
  ▼
┌─────────────────────────┐
│ Calculate distance      │
│ dist = RADIUS * angle   │
└─────────────────────────┘
  │
  ▼
┌─────────────────────────┐
│ total += dist           │
└─────────────────────────┘
  │
  ▼
┌─────────────────────────┐
│ Output total distance   │
└─────────────────────────┘
  │
  ▼
END
```

## Key Formulas

### Spherical to Cartesian Conversion
```
x = cos(latitude) * cos(longitude)
y = cos(latitude) * sin(longitude)
z = sin(latitude)
```

### Great Circle Distance
```
distance = R * arccos(dot_product(p1, p2))
```

Where:
- R = Earth radius (6371 km)
- p1, p2 = normalized 3D points on unit sphere
- dot_product = x1*x2 + y1*y2 + z1*z2
"""
    
    with open("algorithm_flowchart.md", 'w') as f:
        f.write(flowchart)
    
    print("Created algorithm flowchart: algorithm_flowchart.md")

if __name__ == "__main__":
    print("Creating super readable assembly version...")
    create_super_readable_assembly()
    create_algorithm_flowchart()
    print("Done!")
