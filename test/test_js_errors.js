// Test JavaScript file with intentional errors for recursive calling demonstration

// Unused variable - should be detected by ESLint
const unusedVariable = "This variable is never used";

// Missing semicolon - should be detected by ESLint
let name = "John"

// Function with no return statement but should return something
function calculateArea(width, height) {
    const area = width * height;
    // Missing return statement!
}

// Function with potential null/undefined issues
function processUser(user) {
    // No null check - potential runtime error
    console.log(user.name.toUpperCase());
    return user.age * 2;
}

// Inconsistent indentation and spacing
function badFormatting(){
let x=1;
    let y = 2;
      return x+y;
}

// Unreachable code
function unreachableCode() {
    return "early return";
    console.log("This will never execute"); // Unreachable
}

// Main execution with potential errors
const user = null;
const area = calculateArea(10, 20);
console.log("Area:", area); // Will log undefined

processUser(user); // Will throw error due to null