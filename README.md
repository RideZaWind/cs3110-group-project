# CS3110 Group Project: Python Numerical Literal Checker

## Specification
Construct an NFA to recognize the Python nuymerical literals
* Python decimal integer
* Python octal integer
* Python hexadecimal integer
* Python floating point literals

## Contributors
* Huy Pham (GHPHAM) - Program, Integrate, QA
* Adrian Alcoreza (RideZaWind) - NFA design
* Daniel Castillo (DanielCastillo7) - NFA extra credit design

## Functionality
* Able to read strings from a file and determine if they are recognized or not
* Able to input your own string to test the pre-defined NFA
* BONUS: Able to construct your own NFA

## Example
```
Welcome to the NFA program. Type y if you're reading from a file: y
Type the input file name: input.txt
Type the output file name: output.txt

...

Welcome to the NFA program. Type y if you're reading from a file: n
Type y if you want to use the defined NFA, otherwise build your own: y
Input a test string, 'end' to stop: 123456
String 123456: Accepted
Input a test string, 'end' to stop: end
Testing complete.

Welcome to the NFA program. Type y if you're reading from a file: n
Type y if you want to use the defined NFA, otherwise build your own: n
Start state is set to 'start'
Input an NFA node separated by space, ie "0 x hex", otherwise 'end' to stop building: ...
...
```
