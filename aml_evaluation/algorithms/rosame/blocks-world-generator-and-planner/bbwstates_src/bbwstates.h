#include <stdio.h>
#include <math.h>
#include <ctype.h>
#include <getopt.h>


typedef struct {   /* A tower is distinguished by its top and bottom blocks */
  int top;
  int bottom;
} TOWER, *tower;


typedef struct {            /* A partial state of Blocks World */
  int N;                    /* The number of blocks */
  int *S;                   /* The ON relation considered as a function */
  TOWER *rooted;            /* The towers which are on the table */
  TOWER *floating;          /* The towers which are not yet on anything */
  int nrt, nft;             /* The numbers of rooted and floating towers */
} STATE, *state;


typedef struct {
  int size;
  int count;
  int seed;
  double tot;
} RES_TYPE, *res_type;


state get_state(int n);
void free_state(state sigma);
void get_options(int argc, char *argv[],
		 int *size, int *nprob, long *seed, int *alg, int *verb,
		 char *format);
double* make_ratio(int N);
void make_state(state sigma, double ratio[]);
void print_state(state sigma);
void pddlprint(state sigma_i, state sigma_g, int seed, int x);
double drand48();
void record(int len, res_type theresults);
void print_record(res_type theresults);
res_type init_results(int N, int R);

#ifdef DEBUG
void sane(state sigma);
void report(state sigma);
void bumpout(state sigma);
#endif









