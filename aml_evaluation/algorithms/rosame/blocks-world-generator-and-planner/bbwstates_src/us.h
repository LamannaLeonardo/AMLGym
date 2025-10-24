#ifndef US
#define US

#include<stdio.h>
#include <stdlib.h>
#include "definitions.h"

#define UStable 0
#define USblock int

typedef struct {
  int lastmove;
  USblock * obj;
  USblock * dst;
} USPlan, *USplan;


typedef struct {
  USPlan solution;
  int size;
  USblock * si;
  USblock * sg;
  boolean * clear;
  boolean * inposition;
  boolean * considered;
} USProb, * USprob;
 
/* Functions */

int USlength(int i[], int g[], int N, int verbosity);
USprob get_USproblem(int i[], int g[], int N);
void free_USproblem(USprob p);
USplan us( USprob p );
void USinit( USprob p );
boolean USinpos( USprob p, USblock b );
void USunstack( USprob p, USblock b );
void USstack( USprob p, USblock b );
void USmove( USprob p, USblock object, USblock destination );
void printUSplan(int i[], int g[], USprob p);

#endif
