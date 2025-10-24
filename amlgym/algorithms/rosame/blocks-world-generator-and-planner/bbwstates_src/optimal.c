#include "optimal.h"


int OPTlength(int i[], int g[], int N, int verbosity)
{
  OPTinstance p;
  int res;

  p = get_OPTproblem(i,g,N);
  res = (optimal(p))->plan_length;
  switch(verbosity) {
  case 0:
    break;
  case 1:
  case 2:
    printf("  %d\n", res);
    break;
  case 3:
    printOPTplan(i,g,p);
    break;
  }    
  free_OPTproblem(p);
  return res;
}



OPTinstance get_OPTproblem (int i[], int g[], int N)
{
  int x;
  OPTlist l;
  OPTinstance I;

  I = (OPTinstance) malloc(sizeof(OPTINSTANCE));

  for (l=OPTnull; l<number_of_OPTlists; l++) {
    I->L[l].head = 0;
    I->L[l].tail = 0;
  }

  I->P.plan_length = 0;
  I->P.M = (OPTmove) malloc(N * 2 * sizeof(OPTMOVE));

  I->size = N;
  I->B = (OPTblock) malloc((N+1) * sizeof(OPTBLOCK));

  I->table = I->B;
  I->table->offset = 0;
  I->table->si = I->table->sg = I->table->initialsi = 0;
  I->table->isi = I->table->isg = 0;
  I->table->next = I->table->last = 0;
  I->table->loc = 0;
  I->table->clear = I->table->inposition = true;
  I->table->examined = true;

  for (x=1; x<=I->size; x++) {
    I->B[x].si = I->B[x].initialsi = (I->B)+(i[x-1]+1);
    I->B[x].sg = (I->B)+(g[x-1]+1);
    I->B[x].offset = x;
  }
  return I;
}

void free_OPTproblem(OPTinstance I)
{
  free(I->P.M);
  free(I->B);
  free(I);
}



/*
 * Repeatedly find a minimal size hitting set for the list of known
 * deadlocks, run gn1 governed by that set and either return the plan
 * or add a new deadlock to the list.
*/

OPTplan optimal(OPTinstance I)
{
  setlist K;          /* The known deadlocks */
  SET H;              /* The next candidate HS (set by mshs()) */
  SET SD;             /* The singleton deadlocks */
  int H_card;         /* The cardinality of H */
  int SD_card;        /* Minimum value for H_card */
  OPTplan pi;         /* The value returned by gn1 */
  set newd;           /* The new deadlock to be added to K */
  int i;

  if (!I) return 0;
  K = 0;
  SD_card = single_deadlocks(I,&K,SD);
  H_card = SD_card;
  do {
    H_card = mshs(
		  K,
		  H_card,
		  SD,
		  H,
		  I->size,
		  SD_card,
		  &(I->P.dd)
		  );
    pi = gn1_dec(I,H);
    if (!pi) {
      newd = (set) malloc(sizeof(SET));
      deadlock(I,H,newd);
      sl_push(&K,newd);
    }
  }
  while (!pi);
  free_sets(K);
  return pi;
}



/*
 * Add all singleton deadlocks to sofar. Fill H with their union.
 * Return number of them.
*/

int single_deadlocks(OPTinstance I, setlist *sofar, set H)
{
  int x;
  SET allbut;    /* All blocks but the one currently considered */
  int rc = 0;

  emptyset(H);
  for (x=1; x<=I->size; x++) putinset(x,allbut);
  for (x=1; x<=I->size; x++) {
    putoutset(x,allbut);
    if (!gn1_dec(I,allbut)) {
      sl_push(sofar,singleton(x));
      putinset(x,H);
      rc++;
    }
    putinset(x,allbut);
  }
  return rc;
}



/*
 * Fill dest with a minimal deadlock not hit by h. Note that the
 * contents of h may be altered as a side effect of this function.
*/

void deadlock(OPTinstance I, set h, set dest)
{
  int x;

  emptyset(dest);
  for (x=1; x<=I->size; x++)
    if (!isin(x,h)) {
      putinset(x,h);
      if (gn1_dec(I,h)) {
	putoutset(x,h);
	putinset(x,dest);
      }
    }
}




static struct tms TM;

clock_t timestamp()
{
  times(&TM);
  return TM.tms_utime;
}



void printOPTplan(int i[], int g[], OPTinstance I)
{
  int x;

  printf("\nProblem:\n  block  initial   goal\n");
  for (x=0; x<I->size; x++) {
    if (i[x] < 0) printf("%7d    table", x+1);
    else printf("%7d%9d", x+1, i[x]+1);
    if (g[x] < 0) printf("  table\n");
    else printf("%7d\n", g[x]+1);
  }
  printf("\nPlan:\n");
  for (x=0; x < I->P.plan_length; x++) {
    if (I->P.M[x].dst->offset)
      printf("%4d:  %d to %d\n",
	     x+1,
	     I->P.M[x].obj->offset,
	     I->P.M[x].dst->offset);
    else
      printf("%4d:  %d to table\n",
	     x+1,
	     I->P.M[x].obj->offset);
  }
  printf("\n");
}
