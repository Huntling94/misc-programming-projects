#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <time.h>

#include "..\..\..\C_Code\Utilities\utils.h"
#include "..\..\..\C_Code\Files\files.h"
#include "..\..\..\C_Code\Matrix\matrix.h"
#include "..\..\..\C_Code\Vector\vector.h"
#include "..\..\..\C_Code\Math_Extended\math_extended.h"

#define TOMATO 1
#define MUSHROOM 0
#define SOLUTION "_solution"

#define MAX_SEARCH_SLICES 20
typedef struct pizza pizza_t;
typedef struct slice slice_t;

struct pizza{
    matrix_t* pizza;
    char* fname;
    int rows;
    int cols;
    int min_ingredients;
    int max_slice;
    int num_tomato;
    int num_mushroom;
};

struct slice{
    int r1;
    int r2;
    int c1;
    int c2;
};

matrix_t* read_pizza_in(char* fname, int* rows, int* cols, int* min_ingredients, int* max_slice);
int area_of_slice(int r1, int c1, int r2, int c2);
int tomatos_in_slice(pizza_t* pizza, int r1, int c1, int r2, int c2);
int is_valid_slice(pizza_t* pizza, int r1, int c1, int r2, int c2);

pizza_t* create_pizza(char* fname)
{
    pizza_t* pizza = malloc(sizeof*pizza);
    assert(unwanted_null(pizza));
    pizza->pizza = read_pizza_in(fname, &pizza->rows, &pizza->cols, &pizza->min_ingredients, &pizza->max_slice);
    pizza->fname = fname;
    pizza->num_tomato = pizza->pizza->grand_sum(pizza->pizza);
    pizza->num_mushroom = pizza->rows * pizza->cols - pizza->num_tomato;
    return pizza;
}

pizza_t* copy_pizza(pizza_t* pizza)
{
    pizza_t* ret = malloc(sizeof*ret);
    assert(unwanted_null(ret));
    ret->fname = pizza->fname;
    ret->rows = pizza->rows;
    ret->cols = pizza->cols;
    ret->min_ingredients = pizza->min_ingredients;
    ret->max_slice = pizza->max_slice;
    ret->num_tomato = ret->num_tomato;
    ret->num_mushroom = ret->num_mushroom;
    ret->pizza = create_matrix(ret->rows, ret->cols);
    return ret;
}

matrix_t* read_pizza_in(char* fname, int* rows, int* cols, int* min_ingredients, int* max_slice)
{
    int lines = lines_in_file(fname);
    char** buffer = malloc(lines * sizeof(*buffer));
    read_file(fname, buffer, lines);
    
    char* token = buffer[0];

    /* Extract information from first line of file */
    token = strtok(token, " ");
    *rows = atoi(token);
    token = strtok(NULL, " ");
    *cols = atoi(token);
    token = strtok(NULL, " ");
    *min_ingredients = atoi(token);
    token = strtok(NULL, " ");
    *max_slice = atoi(token);
    
    matrix_t* pizza = create_matrix(*rows, *cols); // Store pizza here
    int i, j;

    /* Extract information about pizza from file */
    for(i=1; i<*rows+1; i++){
        for(j=0; j<*cols; j++){
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
    return ((abs(r1 - r2)+1) * (abs(c1 - c2)+1));
}

int tomatos_in_slice(pizza_t* pizza, int r1, int c1, int r2, int c2)
{
    if (pizza == NULL){
        error_set_to_null_message("matrix");
    }
    
    assert(r1 >= 0 && r2 >= 0 && c1 >= 0 && c2 >= 0);
    assert(r1 <= pizza->pizza->num_rows && r2 <= pizza->pizza->num_rows
           && c1 <= pizza->pizza->num_columns && c2 <= pizza->pizza->num_columns);
    int num =0;
    int i, j;
    int higher_row;
    int lower_row;
    int higher_column;
    int lower_column;
    (r1 > r2) ? (higher_row = r1+1) : (higher_row = r2+1);
    (r1 > r2) ? (lower_row = r2) : (lower_row = r1);
    (c1 > c2) ? (higher_column = c1+1) : (higher_column = c2+1);
    (c1 > c2) ? (lower_column = c2) : (lower_column = c1);
    for(i=lower_row; i<higher_row; i++){
        for(j=lower_column; j<higher_column; j++){
            num += pizza->pizza->get_entry(pizza->pizza, i, j);
        }
    }
    return num;
}

int is_valid_slice(pizza_t* pizza, int r1, int c1, int r2, int c2)
{
    if(r1 < 0 || r2 < 0 || c1 < 0 || c2 < 0){
        return 0;
    }
    if(r1 >= pizza->pizza->num_rows || r2 >= pizza->pizza->num_rows
           || c1 >= pizza->pizza->num_columns || c2 >= pizza->pizza->num_columns){
        return 0;
   }
    int area = area_of_slice(r1, c1, r2, c2);
    if (area > pizza->max_slice){
        return 0;
    }
    int num_tomato = tomatos_in_slice(pizza, r1, c1, r2, c2);
    int num_mushroom = area - num_tomato;
    if (num_tomato < pizza->min_ingredients || num_mushroom < pizza->min_ingredients){
        return 0;
    }
    return 1;
}



slice_t* create_slice(int r1, int c1, int r2, int c2)
{
    slice_t* slice = malloc(sizeof(*slice));
    assert(unwanted_null(slice));
    slice->r1 = r1;
    slice->r2 = r2;
    slice->c1 = c1;
    slice->c2 = c2;
    return slice;
}

void print_slice(slice_t* slice)
{
    printf("(%d, %d) to (%d, %d)\n", slice->r1, slice->c1, slice->r2, slice->c2);
}

int get_all_slices(pizza_t* pizza, slice_t** slices, int row, int col, int write_to_file)
{
    int other_row = row; // Other end of slice
    int other_col = col; // Other end of slice

    int row_count = 1;
    int col_count = 1;
    int count = 1;
    int invalid_repetitions = 0;
    int slices_found = 0;
    for(;;){
        int i;
        for(i=0; i<count; i++){
            (count%2 == 0) ? (other_col--) : (other_col++);
            int valid = is_valid_slice(pizza, row, col, other_row, other_col);
            if(valid){
                slice_t* slice = create_slice(row, col, other_row, other_col);
                slices[slices_found++] = slice;
                if(slices_found == MAX_SEARCH_SLICES){
                    return slices_found;
                }
            }
            else{
                invalid_repetitions++;
            }
        }
        col_count++;
        for(i=0; i<count; i++){
            (count%2 == 0) ? (other_row--) : (other_row++);
            int valid = is_valid_slice(pizza, row, col, other_row, other_col);
            if(valid){
                slice_t* slice = create_slice(row, col, other_row, other_col);
                slices[slices_found++] = slice;
                if(slices_found == MAX_SEARCH_SLICES){
                    return slices_found;
                }
            }
            else{
                invalid_repetitions++;
            }
        }
        if(invalid_repetitions > pizza->min_ingredients*((pizza->max_slice*pizza->max_slice))){
            break;
        }
        row_count++;
        assert(row_count == col_count && row_count == count+1);
        count++;
    }
    return slices_found;
}


int eat_slice(pizza_t* eaten_pizza, slice_t* slice)
{
    int higher_row;
    int lower_row;
    int higher_column;
    int lower_column;
    (slice->r1 > slice->r2) ? (higher_row = slice->r1+1) : (higher_row = slice->r2+1);
    (slice->r1 > slice->r2) ? (lower_row = slice->r2) : (lower_row = slice->r1);
    (slice->c1 > slice->c2) ? (higher_column = slice->c1+1) : (higher_column = slice->c2+1);
    (slice->c1 > slice->c2) ? (lower_column = slice->c2) : (lower_column = slice->c1);
    int i, j;
    for(i=lower_row; i<higher_row; i++){
        for(j=lower_column; j<higher_column; j++){
            if (eaten_pizza->pizza->get_entry(eaten_pizza->pizza, i, j)){
                return 0;
            }
        }
    }
    for(i=lower_row; i<higher_row; i++){
        for(j=lower_column; j<higher_column; j++){
            eaten_pizza->pizza->set_entry(eaten_pizza->pizza, i, j, 1);
        }
    }
    return 1;
}
int main(int argc, char* argv[])
{
    clock_t t;
    t = clock();

    int file;
    int total_score = 0;
    for(file=1; file<argc; file++){

        pizza_t* pizza = create_pizza(argv[file]);
        printf("Solving: %s, %d x %d\n", argv[file], pizza->rows, pizza->cols);
        int i, j, k;

        slice_t** temp_slices = malloc(MAX_SEARCH_SLICES * sizeof(*temp_slices));
        assert(unwanted_null(temp_slices));

        pizza_t* eaten_pizza = copy_pizza(pizza);
        char* solution_file = malloc(strlen(argv[file])+2+strlen(SOLUTION));
        for(i=0; i<strlen(argv[file])-3; i++){
            solution_file[i] = argv[file][i];
        }
        for(j=0; j<strlen(SOLUTION); j++){
            solution_file[i++] = SOLUTION[j];
        }
        solution_file[i++] = '.';
        solution_file[i++] = 't';
        solution_file[i++] = 'x';
        solution_file[i++] = 't';
        solution_file[i] = '\0';

        FILE *fp = fopen(solution_file, "w");
        int num_slices = 0;
        int slices_eaten = 0;
        int eaten = 0;
        for(i=0; i<pizza->rows; i++){
            for(j=0; j<pizza->cols; j++){
                num_slices = get_all_slices(pizza, temp_slices, i, j, 0);
                if(num_slices){
                    for(k=0; k<num_slices; k++){
                        eaten = eat_slice(eaten_pizza, temp_slices[k]);
                        if(eaten){
                            slices_eaten++;
                            fprintf(fp, "%d %d %d %d\n", temp_slices[k]->r1, temp_slices[k]->c1, temp_slices[k]->r2, temp_slices[k]->c2);
                            break;
                        }
                    }
                }
                for(k=0; k<num_slices; k++){
                    free(temp_slices[k]);
                }
            }
        }
        printf("\tSlices eaten: %d, Score: %lf\n", slices_eaten, eaten_pizza->pizza->grand_sum(eaten_pizza->pizza));
        total_score += eaten_pizza->pizza->grand_sum(eaten_pizza->pizza);
    }
    printf("Total Score across "); printf("%s", argv[1]);
    int i;
    for(i=2; i<argc; i++){
        printf(", %s", argv[i]);
    }
    printf(": %d\n", total_score);
    t = clock() - t;
    double time_taken = ((double)t)/CLOCKS_PER_SEC; // in seconds 
    printf("Solution took %f seconds to execute \n", time_taken); 
}
