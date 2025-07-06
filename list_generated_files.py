#!/usr/bin/env python3
"""
List all generated assembly files and their purposes
"""

import os

def list_generated_files():
    """List all generated files with descriptions"""
    
    # Define all generated files and their purposes
    files_info = {
        'solve_cpp_readable.asm': 'Basic readable version with function names replaced',
        'solve_cpp_human_readable.asm': 'Enhanced version with detailed comments and explanations',
        'solve_cpp_annotated.asm': 'Variable-annotated version with C++ variable mappings',
        'solve_cpp_ultimate_readable.asm': 'Most comprehensive readable version with full documentation',
        'assembly_variable_guide.md': 'Guide to register usage and memory layout',
        'assembly_understanding_guide.md': 'Detailed guide for understanding assembly code',
        'variable_mapping_guide.md': 'C++ to assembly variable correspondence guide',
        'complete_assembly_guide.md': 'Complete reference for all generated files',
        'algorithm_flowchart.md': 'Text-based flowchart of the algorithm (if generated)'
    }
    
    # Python scripts created
    scripts_info = {
        'make_readable_asm.py': 'Original script to create readable assembly',
        'make_human_readable_asm.py': 'Enhanced readability script',
        'create_annotated_asm.py': 'Script to create variable-annotated assembly',
        'create_ultimate_readable_asm.py': 'Ultimate readability script with full documentation',
        'make_super_readable_asm.py': 'Advanced script (may have encoding issues)',
        'list_generated_files.py': 'This script - lists all generated files'
    }
    
    print("=" * 80)
    print("GENERATED ASSEMBLY FILES AND GUIDES")
    print("=" * 80)
    
    print("\n📄 ASSEMBLY FILES:")
    print("-" * 40)
    for filename, description in files_info.items():
        if filename.endswith('.asm'):
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                print(f"✅ {filename:<35} - {description}")
                print(f"   Size: {size:,} bytes")
            else:
                print(f"❌ {filename:<35} - {description} (NOT FOUND)")
    
    print("\n📚 DOCUMENTATION FILES:")
    print("-" * 40)
    for filename, description in files_info.items():
        if filename.endswith('.md'):
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                print(f"✅ {filename:<35} - {description}")
                print(f"   Size: {size:,} bytes")
            else:
                print(f"❌ {filename:<35} - {description} (NOT FOUND)")
    
    print("\n🐍 PYTHON SCRIPTS:")
    print("-" * 40)
    for filename, description in scripts_info.items():
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename:<35} - {description}")
            print(f"   Size: {size:,} bytes")
        else:
            print(f"❌ {filename:<35} - {description} (NOT FOUND)")
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS:")
    print("=" * 80)
    print("1. 🌟 START WITH: solve_cpp_ultimate_readable.asm")
    print("   - Most comprehensive and well-documented")
    print("   - Includes detailed function explanations")
    print("   - Complete algorithm overview")
    print("")
    print("2. 📖 READ: complete_assembly_guide.md")
    print("   - Overview of all generated files")
    print("   - Tips for understanding assembly")
    print("   - Debugging recommendations")
    print("")
    print("3. 🔍 REFERENCE: assembly_understanding_guide.md")
    print("   - Detailed technical explanations")
    print("   - Register usage patterns")
    print("   - Memory layout information")
    print("")
    print("4. 🎯 FOR LEARNING: variable_mapping_guide.md")
    print("   - C++ to assembly correspondence")
    print("   - Examples of common patterns")
    print("   - Debugging techniques")
    
    print("\n" + "=" * 80)
    print("USAGE TIPS:")
    print("=" * 80)
    print("• Open assembly files in a text editor with syntax highlighting")
    print("• Use 'grep' to search for specific functions or instructions")
    print("• Compare different versions to see various levels of detail")
    print("• Use the guides as reference while reading assembly code")
    print("• Set up debugger with the assembly files for step-by-step analysis")
    
    # Show file sizes summary
    print("\n" + "=" * 80)
    print("FILE SIZE SUMMARY:")
    print("=" * 80)
    
    total_size = 0
    file_count = 0
    
    all_files = {**files_info, **scripts_info}
    for filename in all_files.keys():
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            total_size += size
            file_count += 1
    
    print(f"Total files generated: {file_count}")
    print(f"Total size: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")

if __name__ == "__main__":
    list_generated_files()
