To compile:

GCC:
gcc -Wall -o test pizza.c ..\..\..\C_Code\Utilities\utils.c ..\..\..\C_Code\Files\files.c ..\..\..\C_Code\Matrix\matrix.c ..\..\..\C_Code\Vector\vector.c ..\..\..\C_Code\Math_Extended\math_extended.c

NOTE, compiling as follows assumes you have forked my C-libraries repository (and renamed it C_Code) and you have stored that repository in the same directory level as the
misc-programming-projects repository.

to run all the files: test example.in small.in medium.in big.in

output files will be generated conforming to the Submission format except for the first line not containing the number of slices (this can be manually inserted).

Score:
    example: 8
    small:   34
    medium:  47,559
    big:     893,027

    Total:   940628
    Runtime: ~19 seconds.

The solution is a relatively naive algorithm (clearly the score for example could be improved by inspection).