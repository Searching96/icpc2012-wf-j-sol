# Assembly Variable Guide

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
