# Variable Mapping Guide

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
