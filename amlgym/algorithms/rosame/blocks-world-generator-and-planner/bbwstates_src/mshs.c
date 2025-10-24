#include "optimal.h"

boolean insertafter();
void swapcontents();


/*
* Fill rs with a hitting set (of cardinality at least x) for the sets in L.
* Pointer dd is the address of the count of backtracks, and "exverb" is a
* flag indicating "extreme verbosity". Return the cardinality of rs.
*/

int mshs(setlist L, int mincard, set sd, set rs, int size, int sdsize,
	  int *dd)
{
  SET nonH;            /* Elements not allowed in the HS */
  int maxcard;
  int x,asize;
  int alive[maxOPTblocks];
  setlist ptr;

  for (x=0; x<size+2; x++) alive[x] = 0;
  forallsets(L,ptr) if (disjoint(ptr->s,sd)) {
    for (x=0; x<=size; x++) if (isin(x,ptr->s))
      alive[x] = 1;
  }
  asize = 0;
  for (x=1; x<=size; x++) if (alive[x]) {
    alive[asize++] = x;
    alive[x] = 0;
  }

  for (maxcard = mincard;; maxcard++) {
    assign(rs,sd);
    emptyset(nonH);
    if (new_rec_mshs(L,rs,nonH,maxcard,sdsize,asize,alive,dd))
      return maxcard;
  }
}



/*
  Compute which sets in L are hit, which are units and how many each b hits.
  If already have a hitting set then return true.
  If have an unhittable deadlock, or if depthnow + number of disjoint
  deadlocks still to be hit >= maxdepth then return false.
  If have a local singleton set b to it;
  Else choose a block b (suggested heuristic: greedy (in most deadlocks)).
  Add b to rs.
  If new_rec_mshs of the result, return true.
  Delete b from rs. Add it to forbiddens.
  If new_rec_mshs of the result, return true.
  Delete b from the forbiddens.
  Return false.
*/

boolean new_rec_mshs(setlist L, set H, set nonH, int maxcard, int Hcard,
		     int asize, int alive[], int *dd)
{
  setlist ptr;        /* List of deadlocks to be hit */
  int x,y;
  int *occurs;        /* Number of unhit deadlocks involving each block */
  int b;              /* Next block to be added to H */
  boolean singleton;  /* There is a singleton deadlock */
  int disjointsets;   /* Number of deadlocks disjoint from all the rest */
  int poss_dis;       /* Upper bound on disjointsets */
  boolean isdisjoint; /* This deadlock is disjoint from the rest */

  occurs = (int*) malloc((asize+1) * sizeof(int));
  for (x=0; x<=asize; x++) occurs[x] = 0;
  b = -1;
  singleton = false;
  disjointsets = poss_dis = 0;

  forallsets(L,ptr) {
    if (subset(ptr->s,nonH)) {
      (*dd)++;
      free(occurs);
      return false;                 /* Backtrack if set unhittable */
    }
    if (disjoint(ptr->s,H) && !singleton) {
      ptr->possibly_disjoint = true;
      for (y=0,x=0; x<asize; x++)
	if (isin(alive[x],ptr->s) && !isin(alive[x],nonH)) {
	  y++;
	  occurs[x]++;
	  if (occurs[x] > 1) ptr->possibly_disjoint = false;
	  if (!singleton && (b<0 || occurs[x]>occurs[b])) b = x;
	}
      if (!singleton && y==1) {
	singleton = true;
	for (b=0; !(isin(alive[b],ptr->s) && !isin(alive[b],nonH)); b++);
      }
      else if (ptr->possibly_disjoint) poss_dis++;
    }
    else ptr->possibly_disjoint = false;
  }

  if (b<0) {
    (*dd)++;
    free(occurs);
    return true;                          /* This is a MSHS */
  }

  if (!singleton && Hcard+poss_dis >= maxcard) {
    forallsets(L,ptr) {
      if (ptr->possibly_disjoint && disjoint(ptr->s,H)) {
	isdisjoint = true;
	for (x=0; x< asize; x++)
	  if (occurs[x] > 1 &&
	      isin(alive[x],ptr->s) &&
	      !isin(alive[x],nonH)) {
	    isdisjoint = false;
	    break;
	  }
	if (isdisjoint) disjointsets++;
      }
    }
  }

  if (Hcard+disjointsets > maxcard ||
      ((singleton || occurs[b]>1) && Hcard+disjointsets == maxcard)) {
    (*dd)++;
    free(occurs);
    return false;             /* Backtrack if HS too big */
  }

  putinset(alive[b],H);
  if(new_rec_mshs(L,H,nonH,maxcard,Hcard+1,asize,alive,dd)) {
    free(occurs);
    return true;
  }
  putoutset(alive[b],H);

  if (!singleton && occurs[b] != 1) {
    putinset(alive[b],nonH);
    if(new_rec_mshs(L,H,nonH,maxcard,Hcard,asize,alive,dd)) {
      free(occurs);
      return true;
    }
    putoutset(alive[b],nonH);
  }
  free(occurs);
  return false;                 /* No HS found in any extension */
}


/*
***************************************************************************
*/


/*
* Fill rs with a hitting set of cardinality x for the sets in L
* Return true if successful, false if not.
*/

boolean mshs_dec(setlist L, int x, set rs, int size, int *dd)
{
    SET nonH;            /* Elements not allowed in the HS */

    emptyset(rs);
    emptyset(nonH);
    return rec_mshs(L,rs,nonH,x,0,size,dd);
}



/*
* Fill H with a superset of H, disjoint from nonH which hits L and
* return true, or return false if there is no solution.
* H must be of cardinality not greater than maxcard.
*/

boolean rec_mshs(setlist L, set H, set nonH, int maxcard, int Hcard, int size,
		 int *dd)
{
  setlist ptr;
  int x;
  SET forbidden;      /* The local version of nonH, for recursion */

  forallsets(L,ptr)
    if (subset(ptr->s,nonH)) {
      (*dd)++;
      return false;                 /* Backtrack if set unhittable */
    }
  assign(forbidden,nonH);
  forallsets(L,ptr)
    if (disjoint(H,ptr->s)) {         /* I.e. if set not yet hit */
      if (Hcard == maxcard) {
	(*dd)++;
	return false;             /* Backtrack if HS too big */
      }
      forallmembers(ptr->s,x)       /* Try branching all ways */
	if (!isin(x,forbidden)) {
	  putinset(x,H);
	  if(rec_mshs(ptr->up,H,forbidden,maxcard,Hcard+1,size,dd))
	    return true;
	  putoutset(x,H);
	  putinset(x,forbidden);
	}
      return false;                 /* No HS found in any extension */
    }
  (*dd)++;
  return true;                          /* This is a MSHS */
}



/*
 * Fill rs with a superset of sofar which is a hitting set of
 * cardinality n for the sets in L, and return 1. If no such set
 * exists, set rs to the null set and return 0.
 */

/*
int hsn(setlist L, int n, hss H, set sofar, set rs)
{
  int x;
  int choice;
  set inset;
  set outset;
  set try;

  choice = greedy(H);
  copyset(sofar,try);
  propagate_pos(try,choice,L,H);
  if (cardinality(try) > n) inset = 0;
  else hsn(L,n,H,try,inset);
  if (inset) {
    copyset(rs,inset);
    return;
  }
}
*/


/*
 * Choose the block which hits the largest number of sets in L
 */

/*
int greedy(hss H)
{
  int c = 0;
  int x;

  for (x=1; x<H->nblocks; x++)
    if (H->hits[x] > H->hits[c])
      c = x;
  return c;
}
*/

/****************************************************************/

