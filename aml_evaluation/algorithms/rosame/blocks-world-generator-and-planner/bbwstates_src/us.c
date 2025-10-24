#include "us.h"

int USlength(int i[], int g[],int N, int verbosity)
{
  USprob p;
  int res;

  p = get_USproblem(i,g,N);
  us(p);
  res = p->solution.lastmove;
  switch(verbosity) {
  case 0:
    break;
  case 1:
  case 2:
    printf("  %d\n", res);
    break;
  case 3:
    printUSplan(i,g,p);
    break;
  }    
  free_USproblem(p);
  return(res); 
}
 
USprob get_USproblem(int i[], int g[],int N)
{
  int x;
  USprob p = (USprob) malloc(sizeof(USProb));
  p->size = N+1;
  p->si = (USblock *) malloc((N+1) * sizeof(USblock));
  p->sg = (USblock *) malloc((N+1) * sizeof(USblock));
  for(x=1;x<p->size;x++) {
    p->si[x] = i[x-1]+1;
    p->sg[x] = g[x-1]+1;
  }
  p->clear = (boolean *) malloc((N+1) * sizeof(boolean));
  p->inposition = (boolean *) malloc((N+1) * sizeof(boolean));
  p->considered = (boolean *) malloc((N+1) * sizeof(boolean));
  p->solution.obj = (USblock *) malloc(N * 2 * sizeof(USblock));
  p->solution.dst = (USblock *) malloc(N * 2 * sizeof(USblock));
  return p;
}

void free_USproblem(USprob p)
{
  free(p->si);
  free(p->sg);
  free(p->clear);
  free(p->inposition);
  free(p->considered);
  free(p->solution.obj);
  free(p->solution.dst);
  free(p);
}

USplan us( USprob p )
{
  USblock b;

  if (!p) return 0;
  USinit(p);
  for (b=1; b<p->size; b++)
    if ( p->clear[b] )
      USunstack(p,b);
  for (b=1; b<p->size; b++)
  USstack(p,b); 
  return &(p->solution);
}


void USinit( USprob p )
{
  USblock b;

  p->solution.lastmove = 0;
  for (b=0; b<p->size; b++) {
    p->clear[b] = true;
    p->considered[b] = false;
  }
  p->inposition[UStable] = true;
  for (b=1; b<p->size; b++) {
    USinpos(p,b);
    if ( p->si[b] )
      p->clear[p->si[b]] = false; 
  }
}


boolean USinpos( USprob p, USblock b )
{
  if ( !b )
    return true;
  if ( !p->considered[b] ) {
    p->considered[b] = true;
    if ( p->si[b] != p->sg[b] )
      p->inposition[b] = false;
    else
      p->inposition[b] = USinpos(p,p->si[b]);
  }
  return p->inposition[b];
}


void USunstack( USprob p, USblock b )
{
  USblock c;

  if ( !p->inposition[b] && p->si[b] ) {
    c = p->si[b];
    USmove(p,b,UStable);
    USunstack(p,c);
  }
}


void USstack( USprob p, USblock b )
{
  if ( !p->inposition[b] ) {
    USstack(p,p->sg[b]);
    USmove(p,b,p->sg[b]);
  }
}


void USmove( USprob p, USblock object, USblock destination )
{
  p->solution.obj[p->solution.lastmove] = object;
  p->solution.dst[p->solution.lastmove] = destination;
  p->solution.lastmove++;

  if ( p->si[object] )
    p->clear[p->si[object]] = true;
  if ( destination )
    p->clear[destination] = false;
  p->inposition[object] = ( p->sg[object]==destination
			   && p->inposition[destination] );
  p->si[object] = destination;
}



void printUSplan(int i[], int g[], USprob p)
{
  int x;

  printf("\nProblem:\n  block  initial   goal\n");
  for (x=0; x<p->size; x++) {
    if (i[x] < 0) printf("%7d    table", x+1);
    else printf("%7d%9d", x+1, i[x]+1);
    if (g[x] < 0) printf("  table\n");
    else printf("%7d\n", g[x]+1);
  }
  printf("\nPlan:\n");
  for (x=0; x < p->solution.lastmove; x++) {
    if (p->solution.dst[x])
      printf("  %d to %d\n",
	     p->solution.obj[x],
	     p->solution.dst[x]);
    else
      printf("  %d to table\n",
	     p->solution.obj[x]);
  }
  printf("\n");
}
