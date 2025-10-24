#include "gn1.h"

int GN1length(int i[], int g[], int N, int verbosity)
{
  GN1instance p;
  int res;

  p = get_GN1problem(i,g,N);
  res = (gn1(p))->plan_length;
  switch(verbosity) {
  case 0:
    break;
  case 1:
  case 2:
    printf("  %d\n", res);
    break;
  case 3:
    printGN1plan(i,g,p);
    break;
  }    
  free_GN1problem(p);
  return res;
}


GN1instance get_GN1problem (int i[], int g[], int N)
{
  int x;
  GN1list l;

  GN1instance I = (GN1instance) malloc(sizeof(GN1INSTANCE));

  for (l=null; l<number_of_GN1lists; l++) {
    I->L[l].head = 0;
    I->L[l].tail = 0;
  }

  I->P.plan_length = 0;
  I->P.M = (GN1move) malloc(N * 2 * sizeof(GN1MOVE));

  I->size = N;
  I->B = (GN1block) malloc((N+1) * sizeof(GN1BLOCK));
  I->table = I->B;
  I->table->offset = 0;
  I->table->si = I->table->sg = 0;
  I->table->isi = I->table->isg = 0;
  I->table->next = I->table->last = 0;
  I->table->loc = 0;
  I->table->clear = I->table->inposition = true;
  I->table->examined = true;
  for (x=1; x<=I->size; x++) {
    I->B[x].si = (I->B)+(i[x-1]+1);
    I->B[x].sg = (I->B)+(g[x-1]+1);
    I->B[x].offset = x;
  }
  return I;
}

void free_GN1problem(GN1instance I)
{
  free(I->P.M);
  free(I->B);
  free(I);
}

GN1plan gn1 (GN1instance I)
{
  if (!I) return 0;
  GN1initialise(I);
  GN1solve(I);
  return &(I->P);
}

void GN1initialise(GN1instance I)
{
  int x;

  for (x=1; x<=I->size; x++) {
    I->B[x].clear = true;
    I->B[x].isi = I->B[x].isg = 0;
    I->B[x].examined = false;
    I->B[x].loc = 0;
    I->B[x].inposition = false;
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
    GN1inpos((I->B)+x);
  for (x=1; x<=I->size; x++)
    GN1relocate(I,(I->B)+x);
}



boolean GN1inpos(GN1block b)
{
  if (!b->examined) {
    b->examined = true;
    if (b->sg != b->si)
      b->inposition = false;
    else
      b->inposition = GN1inpos(b->si);
  }
  return b->inposition;
}



void GN1putin(GN1instance I, GN1block b, GN1list to)
{
  if (b->loc == to) return;

  if (b->loc) GN1putout(b,&(I->L[b->loc]));

  if (I->L[to].head)
    I->L[to].head->last = b;
  else
    I->L[to].tail = b;
  b->next = I->L[to].head;
  b->last = 0;
  I->L[to].head = b;

  b->loc = to;
}



void GN1putout(GN1block b, GN1blocklist from)
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



void GN1solve(GN1instance I)
{
  for(;;) {
    if (I->L[GN1ready].head)
      make_GN1move(I,I->L[GN1ready].head,I->L[GN1ready].head->sg);
    else if (I->L[stuck].head)
      make_GN1move(I,I->L[stuck].head,I->table);
    else return;
  }
}



void make_GN1move(GN1instance I, GN1block object, GN1block destination)
{
  GN1block change1, change2, change3;

  change1 = object->si;
  change2 = object->isg;
  if (change1)
    change3 = change1->isg;
  else change3 = 0;
  add_GN1move(I,object,destination);
  GN1relocate(I,object);
  GN1relocate(I,change1);
  GN1relocate(I,change2);
  GN1relocate(I,change3);
}



void GN1relocate(GN1instance I, GN1block b)
{
  if (!b) return;
  if (b->clear && !b->inposition) {
    if (b->sg->inposition && b->sg->clear)
      GN1putin(I,b,GN1ready);
    else if (b->si != I->table)
      GN1putin(I,b,stuck);
    else GN1putin(I,b,0);
  }
  else GN1putin(I,b,0);
}



void add_GN1move(GN1instance I, GN1block object, GN1block destination)
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




void printGN1plan(int i[], int g[], GN1instance I)
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
