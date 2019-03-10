To compile:

GCC:
gcc -Wall -o test pizza.c ..\..\..\C_Code\Utilities\utils.c ..\..\..\C_Code\Files\files.c ..\..\..\C_Code\Matrix\matrix.c ..\..\..\C_Code\Vector\vector.c ..\..\..\C_Code\Math_Extended\math_extended.c

to run, make sure to pass in the filename of the data in as an argument, eg: test example.in