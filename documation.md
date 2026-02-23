# Fluxus Programming Language
## Complete Documentation – Version 2.2

Fluxus is a lightweight interpreted programming language designed to be simple, readable, and powerful enough for console applications.  
It combines ideas from C, C++, Java, Python and Lua, while maintaining its own unique syntax (such as `<-` assignment).

Use FluxIDE or FluxIDE Java edition (coming soon!) to code comfortably like in VS Code or other editors.

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
11. Using More Files (Use file.flx;)
12. Arrays
13. Pointers
14. Structs
15. Built-in Functions
16. Modules
17. Type Conversion Rules
18. Truth Rules
19. Execution Model
20. Complete Example
21. Feature Summary

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

## 4.1 int

```fluxus
int x <- 5;
```

## 4.2 double

```fluxus
double pi <- 3.14;
```

## 4.3 String

```fluxus
String name <- "Fluxus";
```

Escape sequences:

```
\n   newline
\"   quote
\\   backslash
```

## 4.4 bool

```fluxus
bool active <- true;
```

Values:

```
true
false
```

## 4.5 null

Represents no value.

```
null
```

---

# 5. Variables

Declaration:

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

Fluxus uses `<-`.

```fluxus
int x <- 10;
x <- 20;
```

---

# 7. Operators

## Arithmetic

```
+  -  *  /
```

## Comparison

```
==  !=  <  >
```

## Logical

```
and
or
not
```

---

# 8. Conditions

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

## while

```fluxus
int i <- 0;

while (i < 5) {
    println(i);
    i <- i + 1;
}
```

`break` stops the loop.  
`continue` skips current iteration.

---

# 10. Functions

Declaration:

```fluxus
fun add(int a, int b) {
    return a + b;
}
```

Calling:

```fluxus
int result <- add(5, 3);
```

If no return is provided, function returns `null`.

---

# 11. Using More Files

Fluxus supports splitting programs into multiple `.flx` files.

## Basic Usage

```fluxus
Use utils.flx;
```

When encountered:

```
Use file.flx;
```

Fluxus:

1. Loads the file  
2. Parses it  
3. Executes top-level code  
4. Makes its functions and variables available  

## Example

### mathutils.flx

```fluxus
fun add(int a, int b) {
    return a + b;
}
```

### main.flx

```fluxus
Use mathutils.flx;

int result <- add(5, 3);
println(result);
```

## Rules

- File must end with `.flx`
- `Use` is case-sensitive
- Files load in order
- Multiple `Use` allowed
- Circular imports not recommended

## Built-in Modules vs Files

```fluxus
Use fluxus.start;
Use myfile.flx;
```

---

# 12. Arrays

```fluxus
int numbers <- [1, 2, 3];

println(numbers[0]);
numbers[1] <- 10;
```

Arrays are dynamic.

---

# 13. Pointers

```fluxus
int x <- 5;
int* p <- &x;

*p <- 20;
```

Now `x` equals `20`.

---

# 14. Structs

```fluxus
struct Person {
    name: "Simon",
    age: 12
}
```

Access:

```fluxus
println(person.name);
```

---

# 15. Built-in Functions

- `println(value)`
- `toStr(value)`
- `toInt(value)`
- `len(value)`
- `randInt(a, b)`

---

# 16. Modules

Activate with:

```fluxus
Use module.name;
```

## fluxus.start

```
clear()
sleep(ms)
key()
getln()
gotoXY(x,y)
hideCursor()
showCursor()
```

## fluxus.colrs

```
setColor("colorName")
```

Colors:

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

## fluxus.math

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

## fluxus.filesys

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

# 17. Type Conversion Rules

- String → int uses numeric parsing  
- int → double allowed  
- double → int truncates decimals  
- Any value → bool uses truth rules  
- Non-string → String uses text conversion  

---

# 18. Truth Rules

Value is true if:

- int ≠ 0  
- double ≠ 0.0  
- String not empty  
- Array not empty  
- bool is true  

Otherwise false.

---

# 19. Execution Model

Fluxus:

- Executes top to bottom  
- Uses block scope  
- Functions create new scope  
- Arrays are dynamic  
- Struct fields stored at runtime  
- Pointers reference actual variable bindings  

---

# 20. Complete Example

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

# 21. Feature Summary

Fluxus v2 supports:

- Variables
- Functions
- While loops
- Conditions
- Multi-file system
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
