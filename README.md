
<div align="center">
  <img src="felix_logo.png" alt="Felix Programming Language" width="150" height="150">
</div>

# Felix Programming Language Guide

Hey there! 👋 Let's learn how to write programs in Felix, our friendly programming language. It's easy and fun!

## Writing Your First Program

### Variables - Like Boxes for Your Data
Think of variables like labeled boxes where you can store things:
```
x = 42          # Stores the number 42 in a box labeled 'x'
name = "Felix"  # Stores the name "Felix" in a box labeled 'name'
```

### Printing - Showing Things on Screen
When you want to see what's in your variable or show a message:
```
print "Hello!"  # Shows "Hello!" on screen
print x        # Shows what's in the 'x' box
```

### Math Operations - Calculator Stuff
You can do math just like with a calculator:
```
x = 5
y = 3
print x + y  # Adds numbers: 5 + 3 = 8
print x - y  # Subtracts: 5 - 3 = 2
print x * y  # Multiplies: 5 * 3 = 15
print x / y  # Divides: 5 ÷ 3 = 1.666...
```

### Making Decisions with IF, ELIF, and ELSE
You can make your program choose between different options:
```
x = 5
if x > 10
    print "x is bigger than 10!"
elif x > 5
    print "x is bigger than 5!"
elif x > 3
    print "x is bigger than 3!"
else
    print "x is small!"
```

The program will check each condition in order and run the first one that's true. If none are true, it will run the else part!

### Using AND and OR
You can check multiple things at once:
```
age = 12
height = 150

if age > 10 and height > 140
    print "You can ride the big roller coaster!"

if age < 8 or height < 120
    print "Please try the kiddie rides"
```

### Using NOT
You can check if something is NOT true:
```
is_raining = 0
if not is_raining
    print "Let's play outside!"
```

### Repeating Things with WHILE
Want to do something over and over? Use while:
```
count = 1
while count < 5
    print count    # This will print: 1, 2, 3, 4
    count = count + 1
```

## Fun Examples to Try

### Counter Program
```
count = 1
while count < 5
    print count
    count = count + 1
```
This counts from 1 to 4!

### Temperature Check
```
temperature = 25
if temperature > 30
    print "It's hot today!"
if temperature < 15
    print "It's cold today!"
```

### Functions - Making Reusable Code
You can create functions that do specific tasks:
```
fun greet(name)
    print "Hello, " + name

fun add(x, y)
    return x + y

# Using the functions
greet("Felix")        # Prints: Hello, Felix
result = add(5, 3)    # result will be 8
print result
```

### Simple Game Score with Functions
```
fun check_score(score)
    if score > 90
        return "You're a superstar!"
    if score > 80
        return "Great job!"
    return "Keep practicing!"

score = 85
print check_score(score)
```

Remember:
- Each instruction goes on its own line
- After if or while, put the things you want to do on the next lines
- No need for special symbols like ; or ()

Now go ahead and try writing your own programs! 🚀
