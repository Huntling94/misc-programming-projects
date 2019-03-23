#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <unistd.h>
#include <time.h>
#include <math.h>

#define NUM_NEIGHBOURS 8
#define ALIVE 1
#define DEAD 0

typedef struct system system_t;

struct system{
    int** grid;
    int dim;
    int generation; 
};

int get_point(system_t* system, int i, int j)
{
    if (i >= system->dim || j >= system->dim){
        return 0;
    }
    if (i< 0 || j<0){
        return 0;
    }
    return system->grid[i][j];
}
int* neighbours_of_point(system_t* system, int i, int j)
{
    int* neighbours = malloc(NUM_NEIGHBOURS * sizeof(*neighbours));
    assert(neighbours != NULL);
    memset(neighbours, 0, NUM_NEIGHBOURS*sizeof*neighbours);

    int k=0;
    neighbours[k++] = get_point(system, i, j+1);
    neighbours[k++] = get_point(system, i, j-1);
    neighbours[k++] = get_point(system, i+1, j+1);
    neighbours[k++] = get_point(system, i+1, j);
    neighbours[k++] = get_point(system, i+1, j-1);
    neighbours[k++] = get_point(system, i-1, j+1);
    neighbours[k++] = get_point(system, i-1, j);
    neighbours[k++] = get_point(system, i-1, j-1);

    return neighbours;
}

int alive_neighbours(system_t* system, int i, int j)
{
    int* neighbours = neighbours_of_point(system, i, j);
    int k=NUM_NEIGHBOURS, sum=0;
    while(k--){
        sum+= neighbours[k];
    }
    return sum;
}

int update_cell_value(system_t* system, int i, int j)
{
    int alive = alive_neighbours(system, i, j);
    /* Death by Underpopulation or Overpopulation */
    if(alive < 2 || alive > 3){
        return DEAD;
    }
    /* Survives to next generation if alive, or reproduction */
    else if (alive == 3){
        return ALIVE;
    }
    /* If dead, stays dead, if alive, stays alive */
    else{
        return get_point(system, i, j);
    }
}

void print_system(system_t* system)
{
    int i, j;
    printf("Generation: %d\n", system->generation);
    for(i=0; i<system->dim; i++){
        for(j=0; j<system->dim; j++){
            printf("%d ", system->grid[i][j]);
        }
        printf("\n");
    }
}
void evolve(system_t* system)
{
    int new_gen[system->dim][system->dim];
    int i, j;
    for(i=0; i<system->dim; i++){
        for(j=0; j<system->dim; j++){
            new_gen[i][j] = update_cell_value(system, i, j);
        }
    }
    for(i=0; i<system->dim; i++){
        memcpy(system->grid[i], new_gen[i], sizeof(new_gen[i]));
    }
    system->generation++;
}

int system_dead(system_t* system)
{
    assert(system != NULL);
    int i, j;
    for(i=0; i<system->dim; i++){
        for(j=0; j<system->dim; j++){
            if (system->grid[i][j]){
                return 0;
            }
        }
    }
    return 1;
}

system_t* create_system(int dim)
{
    system_t* system = malloc(sizeof*system);
    assert(system != NULL);
    system->grid = malloc(dim * sizeof*system->grid);
    assert(system->grid != NULL);
    system->dim = dim;
    system->generation = 0;

    int i;
    for(i=0; i<dim; i++){
        system->grid[i] = calloc(dim, sizeof(*system->grid[i]));
        assert(system->grid[i] != NULL);
    }
    return system;
}

void seed_random_percent(system_t* system, double percent)
{
    srand(getpid() ^ time(0));
    while(percent > 1){
        percent/=100;
    }
    int i;
    for(i=0; i<floor(percent*100); i++){
        int num = rand()%(system->dim*system->dim);
        system->grid[num/system->dim][num%system->dim] = 1;
    }

}

int main(int argc, char* argv[])
{
    
    int n = atoi(argv[1]);
    if(n < 5){
        assert(0 && "Please enter a grid size of greater than 5");
    }

    system_t* system = create_system(n);
    
    seed_random_percent(system, 0.2);
    

    print_system(system);
    while(!system_dead(system)){
        sleep(1);
        evolve(system);
        print_system(system);
        
    }
    printf("\n--System died out in: %d generations\n", system->generation);
}

