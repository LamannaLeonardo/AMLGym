/*
* This program generates random states of Blocks World (BW) suitable for
* giving a supply of random BW planning problems. Note that the states
* generated are complete (that is, complete specifications of which block
* is on which) and are pseudo-random within the class of such states of
* the same number of blocks. The number of blocks (not including the table)
* is supplied as the argument to this program, along with the number of
* pairs of states required.
*
* The output is in the form of a list of intgers. The blocks are to be
* thought of as numbered from 1 to N, with the table as number 0. Each
* state is specified by giving first N and then for each block in sequence
* the number of the block it is on. A notional size of zero terminates the
* output. For example, the state of 6 blocks
*
*     2
*     5    3
*     4    1    6
*    -------------
*
* is represented by the integers
*    6
*    0 5 1 0 4 0
* meaning there are 6 blocks; 1 is on the table, 2 on 5, 3 on 1, 4 on the
* table, 5 on 4 and 6 on the table.
*
* Optionally the program outputs a solution to the problem instead of the
* pair of states. The algorithm used to generate the solution may be US,
* GN1, GN2 or OPTIMAL (see Slaney and Thiebaux, "Blocks World Revisited",
* AI Journal, 2001).
*
* Parameters are given to this program on the command line. The options are:
* 
*    -n <integer>     number of blocks in each state (default 0)
*    -p <integer>     number of problems (pairs of states) (default 1)
*    -r <integer>     seed for the random number generator (default 3088)
*    -a <integer>     algorithm used to solve problem
*                     0 = US, 1 = GN1, 2 = GN2, 3 = OPTIMAL.
*    -v <integer>     verbosity
*                     -1 = states, 0 = average, 1 = plan lengths,
*                     2 = states and plan lengths, 3 = plans.
*
* The "random" numbers are supplied by the C library function drand48().
*/


#include "bbwstates.h"
#include "us.h"
#include "gn1.h"
#include "gn2.h"
#include "optimal.h"

static double debugger;

int main(argc,argv)
int argc;
char *argv[];
{
  int P;                /* Number of problems required */
  int N;                /* Size of states required */
  state sigma_i, sigma_g; /* Structure holding the initial and goal states */
  double *ratio;        /* Array of ratios. */
  long seed;            /* Seed for drand48() */
  int alg;              /* Code of the algorithm to be called to solve
			   the problem */
  res_type theresults;  /* The results (of course) */
  int x;
  int verb;             /* How much of results to print */
  int (*solver)();      /* Function called according to alg */
  char format[10];      /* PDDL or PLAIN output */

  P = 1;                                          /* Default */
  N = 0;                                          /* Default */
  seed = (long)3088;                              /* Default */
  alg = -1;                                       /* Default */
  verb = -1;                                      /* Default */
  strcpy(format,"PLAIN");                         /* Default */
  get_options(argc,argv,
	      &N,&P,&seed,&alg,&verb,format);     /* Read command line */
  srand48(seed);                                  /* Initialise drand48() */
  ratio = make_ratio(N);                          /* Get probabilities */
  sigma_i = get_state(N);                         /* Mallocs */
  sigma_g = get_state(N);
  theresults = init_results(N,seed);              /* Zero the results */
  switch(alg) {
  case 0:
    solver = USlength;
    break;
  case 1:
    solver = GN1length;
    break;
  case 2:
    solver = GN2length;
    break;
  case 3:
    solver = OPTlength;
    break;
  default:
    solver = 0;
  }

  for (x=0; x<P; x++) {                                   /* Loop S times */
    make_state(sigma_i,ratio);
    make_state(sigma_g,ratio);
    if (!solver || verb==2) {
      if (strcmp(format,"PDDL")) {
	print_state(sigma_i);
	print_state(sigma_g);
      }
      else pddlprint(sigma_i,sigma_g,seed,x+1);
    }
    if (solver)
      record(
	     (*solver)(sigma_i->S,
		       sigma_g->S,
		       N,
		       verb
		       ),
	     theresults
	     );
  }

  if (solver)
    print_record(theresults);
  else if (!strcmp(format,"PLAIN"))
    printf("0\n");                               /* EOF marker */

  free(ratio);
  free_state(sigma_i);
  free_state(sigma_g);
  free(theresults);

  return 0;
}

/*
* Read the command line and check that it is sensible
*/

void get_options(int argc, char *argv[],
		 int *size, int *nprob, long *seed, int *alg, int *verb,
		 char *format)
{
  int option;
  extern char *optarg;
  int i;

  while ((option = getopt (argc, argv, "n:r:o:p:a:v:")) != -1)
    switch( option ) {
    case 'n':
      sscanf(optarg,"%d",size);
      break;
    case 'r':
      sscanf(optarg,"%ld",seed);
      break;
    case 'o':
      strncpy(format,optarg,6);
      break;
    case 'p':
      sscanf(optarg,"%d",nprob);
      break;
    case 'a':
      sscanf(optarg,"%d",alg);
      break;
    case 'v':
      sscanf(optarg,"%d",verb);
      break;
    }
  if (*size<0) {
    printf("Error:\nBad -n option: size %d out of range\n\n", *size);
    fflush(stdout);
    exit(2);
  }
  if (*nprob<0) {
    printf("Error:\nBad -s option: negative number of problems\n\n");
    fflush(stdout);
    exit(3);
  }
  if (*verb < 0 && *alg >= 0) {
    printf("Solutions requested, so ");
    printf("verbosity option 0 (\"Average plan lengths\") assumed.\n\n");
    fflush(stdout);
    *verb = 0;
  }
  if (*verb >= 0 && *alg < 0) {
    printf("No solutions requested, so ");
    printf("verbosity option -1 (\"Just the states\") assumed\n\n");
    fflush(stdout);
    *verb = -1;
  }
  for (i=0; format[i]; i++)
    if (islower(format[i])) format[i] = 'A'+(format[i]-'a');
  if (strcmp(format,"PDDL") && strcmp(format,"PLAIN")) {
    printf("Error:\nBad -o option %s (PLAIN or PDDL expected)\n\n",format);
    exit(4);
  }
}


res_type init_results(int N, int R)
{
  res_type temp;

  temp = (res_type) malloc(sizeof(RES_TYPE));
  temp->size = N;
  temp->count = 0;
  temp->seed = R;
  temp->tot = 0.0;
  return temp;
}


state get_state(int n)
{
  state temp;

  temp = (state) malloc(sizeof(STATE));
  temp->S = (int*) malloc((n+1) * sizeof(int));
  temp->rooted = (tower) malloc((n+1) * sizeof(TOWER));
  temp->floating = (tower) malloc((n+1) * sizeof(TOWER));
  temp->nft = temp->nrt = 0;
  temp->N = n;
  return temp;
}


void free_state(state sigma)
{
  free(sigma->S);
  free(sigma->rooted);
  free(sigma->floating);
  free(sigma);
}



/*
* Let b[n] be the number of BW states of n blocks and let c[n] be the
* number of those in which a given block (say the n-th) is clear. Let
* ratio[n] be defined as c[n]/b[n]. Then clearly ratio[1] = 1, and for
* any n > 1 we have ratio[n+1] = (n*ratio[n] + 1) / (n*(ratio[n]+1) + 1).
*
* The ratios are calculated once, during initialisation, and used many
* times to determine the probabilities with which blocks should be clear
* or with which they should be on the table.
*/

double* make_ratio(int N)
{
  int n,k;
  double *temp;

  temp = (double*) malloc((N+1)*sizeof(double));
  temp[0] = 1;
  for (n=0; n<N; n++)
    temp[n+1] = (n*temp[n] + 1) / (n*(temp[n]+1) + 1);
  return temp;
}



/*
* To make the state, begin by regarding the blocks as short floating towers,
* and repeatedly take the last one and decide whether it is to be clear or
* not. If not, put another floating tower on it and decrement n. If it is to
* be clear, repeatedly decide whether it is to go on the table or not. If so,
* ground it and decrement n. If not, put it on another floating tower and
* decrement n.
*/

void make_state(state sigma, double ratio[])
{
  int x;
  int n;         /* Abbreviation for sigma->nft */
  double r;      /* The randomly generated number */
  double pc;     /* The probability that the block is clear */
  double pt;     /* The probability that it goes on TABLE given it's clear */
  int b;         /* The destination block */

  /* Initially, each block is a floating tower */

  for (x=0; x<sigma->N; x++) {
    sigma->rooted[x].top = sigma->rooted[x].bottom = -1;
    sigma->floating[x].top = sigma->floating[x].bottom = x;
    sigma->S[x] = -1;
  }
  sigma->nrt = 0;
  n = sigma->nft = sigma->N;

#ifdef DEBUG
  sane(sigma);
#endif

  while (n) {
    r = drand48();
    pc = ratio[n];
    pt = 1 / ((n-1)*ratio[n-1] + 1);
    if (r > pc) {                 /* Put the next block under something */
      sigma->nft = --n;
                                  /* Choose a floating tower < n */
      b = (int) floor(((r-pc)/(1.0-pc)) * n);
      sigma->S[sigma->floating[b].bottom] = sigma->floating[n].top;
      sigma->floating[b].bottom = sigma->floating[n].bottom;

#ifdef DEBUG
      printf("Putting %d under %d\n",n,b);
      sane(sigma);
#endif
    }
    else {                        /* The next block is to be clear */
      r /= pc;
      while (r > pt) {            /* Extend the tower downward */ 
	sigma->nft = --n;
	b = (int) floor(drand48()*n);
	if (n > b+1) {            /* Move b up to position n-1 */
#ifdef DEBUG
	  printf("Exchanging %d and %d\n",b,n-1);
#endif
	  x = sigma->floating[b].top;
	  sigma->floating[b].top = sigma->floating[n-1].top;
	  sigma->floating[n-1].top = x;
	  x = sigma->floating[b].bottom;
	  sigma->floating[b].bottom = sigma->floating[n-1].bottom;
	  sigma->floating[n-1].bottom = x;
	  b = n-1;
	}
	sigma->S[sigma->floating[n].bottom] = sigma->floating[b].top;
	sigma->floating[b].top = sigma->floating[n].top;
#ifdef DEBUG
	printf("Putting %d on %d\n",n,b);
	sane(sigma);
#endif
	r = drand48();
	pc = ratio[n];
	pt = 1 / ((n-1)*ratio[n-1] + 1);
      }
      /* Put tower on the table */
      sigma->nft = --n;
      sigma->rooted[sigma->nrt].top = sigma->floating[n].top;
      sigma->rooted[sigma->nrt].bottom = sigma->floating[n].bottom;
      sigma->nrt++;
#ifdef DEBUG
      printf("Putting %d on table\n",n);
      sane(sigma);
#endif
    }
  }
}


/*
* Print the size (number of blocks) and list the S function. Note that for
* output purposes, the first block will be #1 although the array actually
* starts at 0, so we have to add one to everything.
*/

void print_state(state sigma)
{
  int x;

  printf(" %d\n",sigma->N);
  for (x=0; x<sigma->N; x++)
    printf(" %d", sigma->S[x]+1);
  printf("\n");
}


void pddlprint(state sigma_i, state sigma_g, int seed, int x)
{
  boolean b;
  int i, j;

  printf("\n\n(define (problem BW-%d-%d-%d)\n", sigma_i->N, seed, x);
  printf("    (:domain blocksworld)\n");
  printf("    (:objects");
  for ( i = 0; i < sigma_i->N; i++ ) printf(" b%d", i+1);
  printf(")\n");
  printf("    (:init\n");
  for ( i = 0; i < sigma_i->N; i++ ) {
    if ( sigma_i->S[i] == -1 )
      printf("        (on-table b%d)\n", i+1);
    else
      printf("        (on b%d b%d)\n", i+1, sigma_i->S[i]+1);
  }
  for ( i = 0; i < sigma_i->N; i++ ) {
    b = true;
    for ( j = 0; j < sigma_i->N; j++ )
      if (sigma_i->S[j] == i) {
	b = false;
	break;
      }
    if (b) 
      printf("        (clear b%d)\n", i+1);
  }
  printf("    )\n");
  printf("    (:goal\n        (and\n");
  for ( i = 0; i < sigma_g->N; i++ )
    if ( sigma_g->S[i] == -1 )
      printf("            (on-table b%d)\n", i+1);
    else
      printf("            (on b%d b%d)\n", i+1, sigma_g->S[i]+1);
  printf("        )\n    )\n)\n");
}


void record(int len, res_type theresults)
{
  theresults->count++;
  theresults->tot += len;
}


void print_record(res_type theresults)
{
  printf("%d %d %d  %0.4f\n",
	 theresults->size,
	 theresults->count,
	 theresults->seed,
	 theresults->tot/theresults->count);
}



#ifdef DEBUG

void sane(state sigma)
{
  int x,y;

  for (x=0; x<sigma->nft; x++) {
    if (sigma->S[sigma->floating[x].bottom] != -1) bumpout(sigma);
    for (y=sigma->floating[x].top; sigma->S[y]>=0; y = sigma->S[y]);
    if (y != sigma->floating[x].bottom) bumpout(sigma);
  }
  for (x=0; x<sigma->nrt; x++) {
    if (sigma->S[sigma->rooted[x].bottom] != -1) bumpout(sigma);
    for (y=sigma->rooted[x].top; sigma->S[y]>=0; y = sigma->S[y]);
    if (y != sigma->rooted[x].bottom) bumpout(sigma);
  }
  report(sigma);
}

void report(state sigma)
{
  int x,y;

  printf("\nFT: ");
  for (x=0; x<sigma->nft; x++)
    printf("[%d,%d] ",sigma->floating[x].top,sigma->floating[x].bottom);
  printf("\nRT: ");
  for (x=0; x<sigma->nrt; x++)
    printf("[%d,%d] ",sigma->rooted[x].top,sigma->rooted[x].bottom);
  printf("\nS:  ");
  for (x=0; x<sigma->N; x++) printf("%d ",sigma->S[x]);
  printf("\n");
}


void bumpout(state sigma)
{
  report(sigma);
  printf("Aborting on detection of insane sigma (see above)\n");
  exit(1);
}

#endif







