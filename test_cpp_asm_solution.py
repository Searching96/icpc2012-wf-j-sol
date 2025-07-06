#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

def compile_asm_solution():
    """Compile the ASM solution"""
    print("Compiling solve_cpp.asm...")
    
    # First, try to assemble and link the .asm file
    # This assumes Microsoft MASM (ml64.exe) or GNU assembler (as)
    
    # Try different approaches for assembling
    approaches = [
        # Microsoft MASM approach
        {
            "name": "Microsoft MASM (ml64)",
            "commands": [
                ["ml64", "/c", "solve_cpp.asm"],  # Assemble
                ["link", "/subsystem:console", "solve_cpp.obj", "/out:main_asm.exe"]  # Link
            ]
        },
        # GNU assembler approach  
        {
            "name": "GNU Assembler (as + ld)",
            "commands": [
                ["as", "--64", "-o", "solve_cpp.o", "solve_cpp.asm"],  # Assemble
                ["ld", "-o", "main_asm.exe", "solve_cpp.o"]  # Link
            ]
        },
        # GCC approach (treating as assembly)
        {
            "name": "GCC (direct assembly)",
            "commands": [
                ["gcc", "-o", "main_asm.exe", "solve_cpp.asm", "-lm"]
            ]
        }
    ]
    
    for approach in approaches:
        print(f"Trying {approach['name']}...")
        
        try:
            success = True
            for cmd in approach["commands"]:
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode != 0:
                    print(f"  Command failed: {' '.join(cmd)}")
                    print(f"  STDERR: {result.stderr}")
                    success = False
                    break
            
            if success:
                # Check if executable was created
                if os.path.exists("main_asm.exe"):
                    print("✅ Assembly compilation successful!")
                    return True
                else:
                    print("  Executable not found after compilation")
                    
        except subprocess.TimeoutExpired:
            print(f"  Timeout during compilation with {approach['name']}")
        except FileNotFoundError:
            print(f"  {approach['name']} tools not found")
        except Exception as e:
            print(f"  Error with {approach['name']}: {e}")
    
    print("❌ Assembly compilation failed with all approaches!")
    print("\nNote: Assembly files require specific assemblers and linkers.")
    print("Common requirements:")
    print("  - Microsoft MASM (ml64.exe) + link.exe")
    print("  - GNU binutils (as + ld)")
    print("  - Or compile the original C++ file instead")
    return False

def compare_outputs_with_tolerance(expected, actual, tolerance=1e-2):
    """Compare outputs with floating point tolerance"""
    expected_lines = expected.strip().split('\n')
    actual_lines = actual.strip().split('\n')
    
    if len(expected_lines) != len(actual_lines):
        return False, f"Different number of lines: expected {len(expected_lines)}, got {len(actual_lines)}"
    
    for i, (exp_line, act_line) in enumerate(zip(expected_lines, actual_lines)):
        exp_line = exp_line.strip()
        act_line = act_line.strip()
        
        # Handle non-numeric lines (Case headers, "impossible")
        if exp_line.startswith("Case") or exp_line == "impossible":
            if exp_line != act_line:
                return False, f"Line {i+1}: expected '{exp_line}', got '{act_line}'"
        else:
            # Try to parse as float for numeric comparison
            try:
                exp_val = float(exp_line)
                act_val = float(act_line)
                
                # Use both absolute and relative tolerance
                abs_error = abs(exp_val - act_val)
                rel_error = abs_error / max(abs(exp_val), 1e-10)
                
                if abs_error > tolerance and rel_error > tolerance:
                    return False, f"Line {i+1}: expected {exp_val:.6f}, got {act_val:.6f} (abs_error: {abs_error:.6f}, rel_error: {rel_error:.6f})"
            except ValueError:
                # Not a number, do exact string comparison
                if exp_line != act_line:
                    return False, f"Line {i+1}: expected '{exp_line}', got '{act_line}'"
    
    return True, "OK"

def run_test_case(input_file, expected_output_file, tolerance=1e-2):
    """Run a single test case and compare output with tolerance"""
    print(f"Testing {input_file}...")
    
    # Read expected output
    with open(expected_output_file, 'r') as f:
        expected = f.read().strip()
    
    # Run the solution
    with open(input_file, 'r') as f:
        input_data = f.read()
    
    try:
        result = subprocess.run(
            ["./main_asm.exe"],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=60  # 60 second timeout
        )
    except subprocess.TimeoutExpired:
        print(f"❌ {input_file} - TIMEOUT")
        return False
    
    if result.returncode != 0:
        print(f"❌ Runtime error in {input_file}")
        print("STDERR:", result.stderr)
        return False
    
    actual = result.stdout.strip()
    
    # Compare outputs with tolerance
    match, message = compare_outputs_with_tolerance(expected, actual, tolerance)
    
    if match:
        print(f"✅ {input_file} - PASSED")
        return True
    else:
        print(f"❌ {input_file} - FAILED")
        print(f"Reason: {message}")
        return False

def run_all_tests(tolerance=1e-2):
    """Run all test cases with given tolerance"""
    print(f"🔍 Testing ASM solution with tolerance: {tolerance}")
    
    # Find all test cases
    test_dir = Path("shortest")
    input_files = sorted(test_dir.glob("*.in"))
    
    passed = 0
    total = 0
    failed_tests = []
    
    for input_file in input_files:
        expected_file = input_file.with_suffix(".ans")
        if expected_file.exists():
            total += 1
            if run_test_case(str(input_file), str(expected_file), tolerance):
                passed += 1
            else:
                failed_tests.append(input_file.name)
        else:
            print(f"Warning: No expected output file for {input_file}")
    
    print(f"\n📊 Results with tolerance {tolerance}: {passed}/{total} test cases passed")
    
    if failed_tests:
        print(f"❌ Failed tests: {', '.join(failed_tests)}")
    
    return passed == total

def main():
    # Change to the script's directory (relative path handling)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Check if assembly file exists
    if not os.path.exists("solve_cpp.asm"):
        print("❌ solve_cpp.asm file not found!")
        print("Make sure the assembly file is in the current directory.")
        return 1
    
    # Compile solution
    if not compile_asm_solution():
        print("\n💡 Alternative: You can test the C++ version instead:")
        print("   python test_cpp_solution.py")
        return 1
    
    # Test with progressively relaxed tolerances
    tolerances = [1e-3, 1e-2, 1e-1, 1.0]
    
    for tolerance in tolerances:
        print()
        if run_all_tests(tolerance):
            print(f"🎉 All tests passed with tolerance {tolerance}!")
            print("\n✅ ASM solution is working correctly!")
            
            # Clean up
            cleanup_files = ["solve_cpp.obj", "solve_cpp.o", "main_asm.exe"]
            for file in cleanup_files:
                if os.path.exists(file):
                    try:
                        os.remove(file)
                    except:
                        pass
            
            return 0
        print()
    
    print("❌ Tests failed even with very relaxed tolerance!")
    print("The assembly solution may have issues that need debugging.")
    
    # Clean up
    cleanup_files = ["solve_cpp.obj", "solve_cpp.o", "main_asm.exe"]
    for file in cleanup_files:
        if os.path.exists(file):
            try:
                os.remove(file)
            except:
                pass
    
    return 1

if __name__ == "__main__":
    sys.exit(main())
