#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>

#include "..\..\..\C_Code\Utilities\utils.h"
#include "..\..\..\C_Code\Files\files.h"
#include "..\..\..\C_Code\Matrix\matrix.h"
#include "..\..\..\C_Code\Vector\vector.h"
#include "..\..\..\C_Code\Math_Extended\math_extended.h"

#define TOMATO 1
#define MUSHROOM 0
int main(int argc, char* argv[])
{

    int pizza_rows, pizza_columns, min_ingredients, max_slice;
    int lines = lines_in_file(argv[1]);
    char** buffer = malloc(lines * sizeof(*buffer));
    read_file(argv[1], buffer, lines);
    
    char* token = buffer[0];

    token = strtok(token, " ");
    pizza_rows = atoi(token);
    token = strtok(NULL, " ");
    pizza_columns = atoi(token);
    token = strtok(NULL, " ");
    min_ingredients = atoi(token);
    token = strtok(NULL, " ");
    max_slice = atoi(token);
    printf("%d %d %d %d\n", pizza_rows, pizza_columns, min_ingredients, max_slice);
    
    matrix_t* pizza = create_matrix(pizza_rows, pizza_columns);
    int i, j;
    for(i=1; i<pizza_rows+1; i++){
        for(j=0; j<pizza_columns; j++){
            if (buffer[i][j] == 'T'){
                pizza->set_entry(pizza, i-1, j, TOMATO);
            }
        }
    }
    free_string_array(buffer, lines);
    
    pizza->print(pizza);


}