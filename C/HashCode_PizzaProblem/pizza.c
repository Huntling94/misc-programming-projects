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

matrix_t* read_pizza_in(char* fname, int* pizza_rows, int* pizza_columns, int* min_ingredients, int* max_slice)
{
    int lines = lines_in_file(fname);
    char** buffer = malloc(lines * sizeof(*buffer));
    read_file(fname, buffer, lines);
    
    char* token = buffer[0];

    /* Extract information from first line of file */
    token = strtok(token, " ");
    *pizza_rows = atoi(token);
    token = strtok(NULL, " ");
    *pizza_columns = atoi(token);
    token = strtok(NULL, " ");
    *min_ingredients = atoi(token);
    token = strtok(NULL, " ");
    *max_slice = atoi(token);
    printf("%d %d %d %d\n", *pizza_rows, *pizza_columns, *min_ingredients, *max_slice);
    
    matrix_t* pizza = create_matrix(*pizza_rows, *pizza_columns); // Store pizza here
    int i, j;

    /* Extract information about pizza from file */
    for(i=1; i<*pizza_rows+1; i++){
        for(j=0; j<*pizza_columns; j++){
            if (buffer[i][j] == 'T'){
                pizza->set_entry(pizza, i-1, j, TOMATO);
            }
        }
    }

    free_string_array(buffer, lines);
    return pizza;
}

int area_of_slice(int r1, int c1, int r2, int c2)
{
    return ((abs(r1 - r2) + 1) * (abs(c1 - c2) + 1));
}

int tomatos_in_slice(matrix_t* pizza, int r1, int c1, int r2, int c2)
{
    if (pizza == NULL){
        error_set_to_null_message("matrix");
    }
    
    assert(r1 >= 0 && r2 >= 0 && c1 >= 0 && c2 >= 0);
    assert(r1 <= pizza->num_rows && r2 <= pizza->num_rows
           && c1 <= pizza->num_columns && c2 <= pizza->num_columns);
    int num =0;
    int i, j;
    int higher_row;
    int lower_row;
    int higher_column;
    int lower_column;
    (r1 > r2) ? (higher_row = r1) : (higher_row = r2);
    (r1 > r2) ? (lower_row = r2) : (lower_row = r1);
    (c1 > c2) ? (higher_column = c1) : (higher_column = c2);
    (c1 > c2) ? (lower_column = c2) : (lower_column = c1);

    for(i=lower_row; i<higher_row+1; i++){
        for(j=lower_column; j<higher_column+1; j++){
            num += pizza->get_entry(pizza, i, j);
        }
    }
    return num;
}

/*
void get_all_slices(int* possible_slices, int row, int col, int min_ingredients, int max_slice)
{
    int alloc = 10;
    int num_slices = 0;

    int other_row = row; // Other end of slice
    int other_col = col; // Other end of slice
    for(;;){
        int i;
        for(i=0; i<max_slice; i++){

        }
    }
}
*/
int main(int argc, char* argv[])
{
    int pizza_rows=0, pizza_columns=0, min_ingredients=0, max_slice=0;
    matrix_t* pizza = read_pizza_in(argv[1], &pizza_rows, &pizza_columns, &min_ingredients, &max_slice);

    int num_tomato, num_mushroom;
    num_tomato = pizza->grand_sum(pizza);
    num_mushroom = pizza_rows * pizza_columns - num_tomato;

    //pizza->print(pizza);
    printf("Number of Mushrooms: %d\n", num_mushroom);
    printf("Number of Tomatos: %d\n", num_tomato);

    printf("%d\n", area_of_slice(0, 0, 999, 999));
    printf("Number of tomatos: %d\n", tomatos_in_slice(pizza, 0, 0, 999, 999));
    //int** possible_slices = malloc(pizza_rows * sizeof(*possible_slices));
    //matrix_t* eaten_pizza = pizza->copy(pizza);

}