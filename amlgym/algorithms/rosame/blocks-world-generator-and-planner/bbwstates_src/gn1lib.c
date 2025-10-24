#include "optimal.h"


/*
 * Seek a near-optimal BW plan for I using the GN1 algorithm
 * with the constraint that only blocks in X may be used for
 * deadlock-breaking moves to the table. If a plan is found,
 * return it; otherwise return null.
*/

OPTplan gn1_dec (OPTinstance I, set X)
{
  if (!I) return 0;
  GN1DECinitialise(I,X);
  if (GN1DECsolve(I,X)) return &(I->P);
  else return 0;
}



/*
 * Get the instance ready to search for a new plan. Note that
 * GN1 may be called many times with the same I and different X.
*/

void GN1DECinitialise(OPTinstance I, set X)
{
  int x;
  OPTlist l;

  for (l=OPTnull; l<number_of_OPTlists; l++) {
    I->L[l].head = 0;
    I->L[l].tail = 0;
  }
  I->P.plan_length = 0;

  I->table = I->B;
  I->table->offset = 0;
  I->table->initialsi = I->table->si = I->table->sg = 0;
  I->table->isi = I->table->isg = 0;
  I->table->next = I->table->last = 0;
  I->table->loc = 0;
  I->table->clear = I->table->inposition = true;
  I->table->examined = true;

  for (x=1; x<=I->size; x++) {
    I->B[x].clear = true;
    I->B[x].isi = I->B[x].isg = 0;
    I->B[x].examined = false;
    I->B[x].loc = 0;
    I->B[x].inposition = false;
    I->B[x].si = I->B[x].initialsi;
  }
  for (x=1; x<=I->size; x++) {
    if (I->B[x].si != I->table) {
      I->B[x].si->isi = (I->B)+x;
      I->B[x].si->clear = false;
    }
    if (I->B[x].sg != I->table)
      I->B[x].sg->isg = (I->B)+x;
  }
  for (x=1; x<=I->size; x++)
    GN1DECinpos((I->B)+x);
  for (x=1; x<=I->size; x++)
    GN1DECrelocate(I,X,(I->B)+x);

  I->mustmove = 0;
  for (x=1; x<=I->size; x++)
    if (!I->B[x].inposition)
      I->mustmove++;
}



/*
 * The sequence of blocks at or below b is the same in si as in sg
*/

boolean GN1DECinpos(OPTblock b)
{
  if (!b->examined) {
    b->examined = true;
    if (b->sg != b->si)
      b->inposition = false;
    else
      b->inposition = GN1DECinpos(b->si);
  }
  return b->inposition;
}


/*
 * Insert b in to
*/

void GN1DECputin(OPTinstance I, OPTblock b, OPTlist to)
{
  if (b->loc == to) return;

  if (b->loc) GN1DECputout(b,&(I->L[b->loc]));

  if (I->L[to].head)
    I->L[to].head->last = b;
  else
    I->L[to].tail = b;
  b->next = I->L[to].head;
  b->last = 0;
  I->L[to].head = b;

  b->loc = to;
}



/*
 * Delete b from from
*/

void GN1DECputout(OPTblock b, OPTblocklist from)
{
  if (b->last)
    b->last->next = b->next;
  else
    from->head = b->next;
  if (b->next)
    b->next->last = b->last;
  else
    from->tail = b->last;
}



/*
 * Move blocks until the goal is reached or until really stuck
*/

boolean GN1DECsolve(OPTinstance I, set X)
{
  for(;;) {
    if (I->L[OPTready].head)
      make_GN1DECmove(I,X,I->L[OPTready].head,I->L[OPTready].head->sg);
    else if (I->L[OPTstuck].head)
      make_GN1DECmove(I,X,I->L[OPTstuck].head,I->table);
    else {
      return !(I->L[OPTnogood].head);
    }
  }
}



/*
 * Update the state description when object is put on destination
*/

void make_GN1DECmove(OPTinstance I, set X,
		     OPTblock object, OPTblock destination)
{
  OPTblock change1;
  OPTblock change2;
  OPTblock change3;   /* These may change status as a result of the move */

  change1 = object->si;
  change2 = object->isg;
  if (change1) change3 = change1->isg;
  else change3 = 0;
  add_GN1DECmove(I,object,destination);
  GN1DECrelocate(I,X,object);
  GN1DECrelocate(I,X,change1);
  GN1DECrelocate(I,X,change2);
  GN1DECrelocate(I,X,change3);
}



/*
 * The main subroutine of make_move. This updates the state.
*/

void add_GN1DECmove(OPTinstance I, OPTblock object, OPTblock destination)
{
  if (object->si != I->table) {
    object->si->isi = 0;
    object->si->clear = true;
  }
  if (destination != I->table) {
    destination->isi = object;
    destination->clear = false;
  }
  object->si = destination;
  if (object->sg == destination && destination->inposition)
    object->inposition = true;
  I->P.M[I->P.plan_length].obj = object;
  I->P.M[I->P.plan_length].dst = destination;
  I->P.plan_length++;
}



/*
 * Put b in the correct list (ready, stuck, nogood or none)
*/

void GN1DECrelocate(OPTinstance I, set X, OPTblock b)
{
  if (!b) return;
  if (b->clear && !b->inposition) {
    if (b->sg->inposition && b->sg->clear)
      GN1DECputin(I,b,OPTready);
    else if (b->si != I->table) {
      if (!X || isin(b->offset,X))
	GN1DECputin(I,b,OPTstuck);
      else
	GN1DECputin(I,b,OPTnogood);
    }
    else GN1DECputin(I,b,0);
  }
  else GN1DECputin(I,b,0);
}
