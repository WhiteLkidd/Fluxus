# Fluxus Programming Language
## Complete Documentation – Version 2

Fluxus is a lightweight interpreted programming language designed to be simple, readable, and powerful enough for console applications.
It combines ideas from C, C++, Java, Python and Lua, while maintaining its own unique syntax (such as `<-` assignment).

Use simonpad to code comfortably like in for example VS code or another editors

This document explains everything available in Fluxus v2 in a clear and beginner-friendly way.

---

# Table of Contents

1. Introduction
2. Program Structure
3. Basic Syntax Rules
4. Data Types
5. Variables
6. Assignment
7. Operators
8. Conditions (if / else)
9. Loops (while)
10. Functions
11. Arrays
12. Pointers
13. Structs
14. Built-in Functions
15. Modules
16. Type Conversion Rules
17. Truth Rules
18. Execution Model
19. Complete Example
20. Feature Summary

---

# 1. Introduction

Fluxus programs are stored in `.flx` files.

To run a program:

```
./fluxus program.flx
```

Programs are executed from top to bottom.

---

# 2. Program Structure

A program is made of statements.

Each statement ends with:

```
;
```

Code blocks use curly braces:

```
{
    statements
}
```

Example:

```fluxus
int x <- 10;
println(x);
```

---

# 3. Basic Syntax Rules

- Statements end with `;`
- Assignment uses `<-`
- Blocks use `{ }`
- Parentheses are used for conditions and function calls
- Case-sensitive keywords (`Use`, `int`, `fun`, etc.)

---

# 4. Data Types

Fluxus supports the following primitive types:

## 4.1 int

Whole numbers.

```fluxus
int x <- 5;
```

## 4.2 double

Decimal numbers.

```fluxus
double pi <- 3.14;
```

## 4.3 String

Text values inside double quotes.

```fluxus
String name <- "Fluxus";
```

Escape sequences supported:

```
\n   newline
\"   quote
\\   backslash
```

## 4.4 bool

Boolean values.

```fluxus
bool active <- true;
```

Values:

```
true
false
```

## 4.5 null

Represents "no value".

```
null
```

---

# 5. Variables

Declaration syntax:

```
type name <- expression;
```

Example:

```fluxus
int age <- 12;
String user <- "Simon";
```

Reassignment:

```fluxus
age <- 13;
```

---

# 6. Assignment

Fluxus uses:

```
<-
```

Example:

```fluxus
int x <- 10;
x <- 20;
```

---

# 7. Operators

## 7.1 Arithmetic

```
+   addition
-   subtraction
*   multiplication
/   division
```

Example:

```fluxus
int result <- 5 + 3;
```

---

## 7.2 Comparison

```
==   equal
!=   not equal
<    less than
>    greater than
```

Example:

```fluxus
if (x == 10) {
    println("Ten");
}
```

---

## 7.3 Logical

```
and
or
not
```

Example:

```fluxus
if (x > 0 and x < 100) {
    println("In range");
}
```

---

# 8. Conditions

## 8.1 if

```fluxus
if (condition) {
    statements
}
```

## 8.2 if / else

```fluxus
if (x > 10) {
    println("Big");
} else {
    println("Small");
}
```

## 8.3 else if

```fluxus
if (x > 10) {
    println("Big");
} else if (x > 5) {
    println("Medium");
} else {
    println("Small");
}
```

---

# 9. Loops

## 9.1 while

Repeats while condition is true.

```fluxus
int i <- 0;

while (i < 5) {
    println(i);
    i <- i + 1;
}
```

## 9.2 break

Stops loop immediately.

## 9.3 continue

Skips current iteration.

---

# 10. Functions

Functions allow reusable blocks of code.

## 10.1 Declaration

```fluxus
fun add(int a, int b) {
    return a + b;
}
```

## 10.2 Calling

```fluxus
int result <- add(5, 3);
```

## 10.3 Return

```fluxus
return value;
```

If no return is provided, function returns `null`.

---

# 11. Arrays

Arrays store multiple values.

## 11.1 Creating

```fluxus
int numbers <- [1, 2, 3];
```

## 11.2 Access

```fluxus
println(numbers[0]);
```

## 11.3 Modify

```fluxus
numbers[1] <- 10;
```

Arrays are dynamic in size.

---

# 12. Pointers

Pointers store references to variables.

## 12.1 Getting Address

```fluxus
int x <- 5;
int* p <- &x;
```

## 12.2 Dereferencing

```fluxus
*p <- 20;
```

Now `x` equals `20`.

---

# 13. Structs

Structs store named fields.

## 13.1 Creating

```fluxus
struct Person {
    name: "Simon",
    age: 12
}
```

## 13.2 Access

```fluxus
println(person.name);
```

Fields can contain any value type.

---

# 14. Built-in Functions

## 14.1 Output

### println(value)
Prints value with newline.

### toStr(value)
Converts value to String.

### toInt(value)
Converts value to integer.

### len(value)
Returns length of String or Array.

### randInt(a, b)
Returns random integer between a and b.

---

# 15. Modules

Modules enable additional features.

Activate with:

```fluxus
Use module.name;
```

---

## 15.1 fluxus.start

Console control functions:

```
clear()
sleep(ms)
key()
getln()
gotoXY(x,y)
hideCursor()
showCursor()
```

---

## 15.2 fluxus.colrs

```
setColor("colorName")
```

Available colors:

black  
red  
green  
blue  
yellow  
magenta  
cyan  
white  
bright_red  
bright_green  
bright_blue  
reset  

---

## 15.3 fluxus.math

```
sin(x)
cos(x)
tan(x)
sqrt(x)
floor(x)
ceil(x)
pow(a,b)
min(a,b)
max(a,b)
```

---

## 15.4 fluxus.filesys

```
readFile(path)
writeFile(path,text)
appendFile(path,text)
exists(path)
deleteFile(path)
mkdir(path)
listDir(path)
```

---

# 16. Type Conversion Rules

When assigning values:

- String → int uses numeric parsing
- int → double allowed
- double → int truncates decimals
- Any value → bool uses truth rules
- Non-string → String uses text conversion

---

# 17. Truth Rules

Value is true if:

- int ≠ 0
- double ≠ 0.0
- String not empty
- Array not empty
- bool is true

Otherwise false.

---

# 18. Execution Model

Fluxus:

- Executes top to bottom
- Uses block scope
- Functions create new scope
- Variables are dynamically stored
- Arrays are dynamic
- Struct fields stored at runtime
- Pointers reference actual variable bindings

---

# 19. Complete Example

```fluxus
Use fluxus.start;
Use fluxus.colrs;

int x <- 5;
int* p <- &x;

*p <- 20;

setColor("green");
println("Value:");
println(x);
setColor("reset");
```

---

# 20. Feature Summary

Fluxus v2 supports:

- Variables
- Functions
- While loops
- Conditions
- Arrays
- Pointers
- Structs
- Console control
- File system access
- Math library
- Module system
- Type conversion
- Dynamic memory handling

---

Fluxus v2  
Created by Lord Simon  
2026
