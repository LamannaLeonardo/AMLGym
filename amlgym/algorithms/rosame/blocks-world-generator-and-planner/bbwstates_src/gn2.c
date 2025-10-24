#include "gn2.h"

int GN2length(int i[], int g[], int N, int verbosity)
{
  GN2instance p;
  int res;

  p = get_GN2problem(i,g,N);
  res = (gn2(p))->plan_length;
  switch(verbosity) {
  case 0:
    break;
  case 1:
  case 2:
    printf("  %d\n", res);
    break;
  case 3:
    printGN2plan(i,g,p);
    break;
  }    
  free_GN2problem(p);
  return res;
}

GN2instance get_GN2problem (int i[], int g[], int N)
{
  int x;
  GN2list l;

  GN2instance I = (GN2instance) malloc(sizeof(GN2INSTANCE));

  for (l=finished; l<number_of_GN2lists; l++) {
    I->L[l].head = 0;
    I->L[l].tail = 0;
  }
  I->P.plan_length = 0;
  I->P.M = (GN2move) malloc(N * 2 * sizeof(GN2MOVE));

  I->size = N;
  I->B = (GN2block) malloc((N+1) * sizeof(GN2BLOCK));
  I->table = I->B;
  I->table->offset = 0;
  I->table->si = I->table->sg = 0;
  I->table->isi = I->table->isg = 0;
  I->table->next = I->table->last = 0;
  I->table->loc = finished;
  I->table->clear = I->table->inposition = true;
  I->table->examined = true;
  I->table->concierge = I->table->g_concierge = 0;
  I->table->deltapoint = I->table->top = 0;

  I->deadlock.head = 0;

  for (x=1; x<=I->size; x++) {
    I->B[x].si = (I->B)+(i[x-1]+1);
    I->B[x].sg = (I->B)+(g[x-1]+1);
    I->B[x].offset = x;
    I->B[x].concierge = I->B[x].g_concierge = 0;
    I->B->deltapoint = I->B[x].top = 0;
  }
  return I;
}

void free_GN2problem(GN2instance I)
{
  free(I->P.M);
  free(I->B);
  free(I);
}



GN2plan gn2 (GN2instance I)
{
  if (!I) return 0;
  GN2initialise_2(I);
  GN2solve_2(I);
  return &(I->P);
}

void GN2initialise_2(GN2instance I)
{
  int x;
  GN2block b;

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
    GN2inpos((I->B)+x);
  for (x=1; x<=I->size; x++)
    I->B[x].examined = false;
  for (x=1; x<=I->size; x++)
    GN2relocate(I,(I->B)+x);
  for (x=1; x<=I->size; x++) {
    if ( I->B[x].si == I->table ) {
      for (b=(I->B)+x; b; b = b->isi) {
	b->concierge = (I->B)+x;
	I->B[x].top = b;
      }
    }
    if ( I->B[x].sg == I->table ) {
      I->B[x].deltapoint = I->table;
      for (b=(I->B)+x; b; b = b->isg) {
	b->g_concierge = (I->B)+x;
	if (b->inposition)
	  I->B[x].deltapoint = b;
      }
    }
  }
}



boolean GN2inpos(GN2block b)
{
  if (!b->examined) {
    b->examined = true;
    if (b->sg != b->si)
      b->inposition = false;
    else
      b->inposition = GN2inpos(b->si);
  }
  return b->inposition;
}



void GN2putin(GN2instance I, GN2block b, GN2list to)
{
  if (to && b->loc == to) return;

  if (b->loc) {
    if (b->last)
      b->last->next = b->next;
    else
      I->L[b->loc].head = b->next;
    if (b->next)
      b->next->last = b->last;
    else
      I->L[b->loc].tail = b->last;
  }

  if (I->L[to].head)
    I->L[to].head->last = b;
  else
    I->L[to].tail = b;
  b->next = I->L[to].head;
  b->last = 0;
  I->L[to].head = b;

  b->loc = to;
}



void GN2solve_2(GN2instance I)
{
  for(;;) {
    if (I->L[GN2ready].head)
      make_GN2move(I,I->L[GN2ready].head,I->L[GN2ready].head->sg);
    else if (I->L[stuck_on_tower].head)
      make_GN2move(I,GN2deadlock_breaker(I),I->table);
    else return;
  }
}



GN2block GN2deadlock_breaker(GN2instance I)
{
  GN2block d;

  while (I->deadlock.head && I->deadlock.head->loc != stuck_on_tower) {
    I->deadlock.head = I->deadlock.head->idelta;
    if (I->deadlock.head)
      I->deadlock.head->delta = 0;
  }
  if (!I->deadlock.head) {
    I->deadlock.head = I->L[stuck_on_tower].head;
    I->deadlock.head->delta = I->deadlock.head->idelta = 0;
    I->deadlock.head->examined = true;
  }
  for(;;) {
    d = GN2delta_of(I->deadlock.head);
    if (d->examined) return I->deadlock.head;
    I->deadlock.head->delta = d;
    d->idelta = I->deadlock.head;
    I->deadlock.head = d;
    d->examined = true;
  }
}



void make_GN2move(GN2instance I, GN2block object, GN2block destination)
{
  GN2block change1, change2, change3;

  change1 = object->si;
  change2 = object->isg;
  if (change1)
    change3 = change1->isg;
  else change3 = 0;
  add_GN2move(I,object,destination);
  GN2relocate(I,object);
  GN2relocate(I,change1);
  GN2relocate(I,change2);
  GN2relocate(I,change3);
}



void GN2relocate(GN2instance I, GN2block b)
{
  if (!b) return;
  if (b->inposition)
    GN2putin(I,b,finished);
  else if (b->clear && b->sg->inposition && b->sg->clear)
    GN2putin(I,b,GN2ready);
  else if (b->clear) {
    if (b->si==I->table)
      GN2putin(I,b,stuck_on_table);
    else
      GN2putin(I,b,stuck_on_tower);
  }
  else if (b->sg->inposition && b->sg->clear)
    GN2putin(I,b,unclear);
  else
    GN2putin(I,b,hopeless);
}


#define top_now(b) (b->concierge->top)
#define alpha(b) (b->g_concierge->deltapoint)


GN2block GN2delta_of(GN2block b)
{
  if (b->loc != stuck_on_tower) return 0;
  if (alpha(b)->sg) {
    if (alpha(b)->clear) return top_now(alpha(b)->isg);
    return top_now(alpha(b));
  }
  return top_now(b->g_concierge);
}


void add_GN2move(GN2instance I, GN2block object, GN2block destination)
{
  if (object->si != I->table) {
    object->si->isi = 0;
    object->si->clear = true;
    object->concierge->top = object->si;
  }
  if (destination != I->table) {
    destination->isi = object;
    destination->clear = false;
    object->concierge = destination->concierge;
    object->concierge->top = object;
  }
  else {
    object->concierge = object;
    object->top = object;
  }
  object->si = destination;
  if (object->sg == destination && destination->inposition) {
    object->inposition = true;
    object->g_concierge->deltapoint = object;
  }
  I->P.M[I->P.plan_length].obj = object;
  I->P.M[I->P.plan_length].dst = destination;
  I->P.plan_length++;
}



void printGN2plan(int i[], int g[], GN2instance I)
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
