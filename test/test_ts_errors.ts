// Test TypeScript file with intentional errors for recursive calling demonstration

// Type annotation errors
interface User {
    name: string;
    age: number;
    email?: string;
}

// Missing type annotations - should be detected by TypeScript
function processData(data) {  // Parameter 'data' implicitly has an 'any' type
    return data.map(item => item.value);  // Property 'value' does not exist
}

// Type mismatch errors
function calculateTotal(items: number[]): string {
    const sum = items.reduce((acc, item) => acc + item, 0);
    return sum;  // Type 'number' is not assignable to type 'string'
}

// Unused variables - ESLint should catch this
const unusedConstant = "Never used";
let unusedVariable: string;

// Missing return type annotation
function getUserInfo(id: number) {  // Should specify return type
    if (id > 0) {
        return {
            id: id,
            name: "User " + id,
            active: true
        };
    }
    // Missing return for else case
}

// Null/undefined issues
function processUser(user: User | null): void {
    // No null check - potential runtime error
    console.log(user.name.toUpperCase());  // Object is possibly 'null'
    console.log(user.age * 2);
}

// Generic type issues
function identity<T>(arg): T {  // Parameter 'arg' implicitly has an 'any' type
    return arg;
}

// Interface implementation issues
class UserManager implements User {  // Class incorrectly implements interface 'User'
    name: string = "";
    // Missing 'age' property
    
    constructor(name: string) {
        this.name = name;
    }
}

// Async/await issues
async function fetchData(): Promise<string> {
    const response = fetch("https://api.example.com/data");  // Missing 'await'
    return response.text();  // Type error: Property 'text' does not exist
}

// Main execution with errors
const user: User = null;  // Type 'null' is not assignable to type 'User'
const manager = new UserManager("John");
processUser(user);