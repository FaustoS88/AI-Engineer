#!/usr/bin/env python3

"""
Test script to demonstrate the recursive function calling improvements.

This script contains intentional errors that should trigger the AI to:
1. Read the file and detect issues
2. Automatically fix the issues with additional function calls
3. Complete the task fully
"""

def calculate_sum(numbers):
    # Missing return statement - this should be detected and fixed
    total = 0
    for num in numbers:
        total += num
    # return total  # This line is missing!

def divide_numbers(a, b):
    # No error handling - this should be improved
    result = a / b
    return result

# Unused import - this should be cleaned up
import os
import sys

# Main execution
if __name__ == "__main__":
    numbers = [1, 2, 3, 4, 5]
    result = calculate_sum(numbers)
    print(f"Sum: {result}")
    
    # This will cause a division by zero error
    division_result = divide_numbers(10, 0)
    print(f"Division: {division_result}")
