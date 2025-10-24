// char *malloc();

#define SSZ 20
#define WS 32
#define MAX_CARD (SSZ * WS)

#ifndef BOOL
#define BOOL
typedef enum {
  false,
  true} boolean;
#endif

#define Stype unsigned long
typedef unsigned long SET[SSZ];
#define set unsigned long *

typedef struct STLST {
  set s;
  boolean possibly_disjoint;
  struct STLST *up;
  struct STLST *down;
} SETLIST, *setlist;

#define forallsets(sl,sp) for(sp = sl; sp; sp = sp->up)
#define forallmembers(s,x) for(x = 0; x < MAX_CARD; x++) if (isin(x,s))

void emptyset(set s);
void assign(set dest, set source);
void putinset(int x, set s);
void putoutset(int x, set s);
boolean isin(int x, set s);
set singleton(int x);
int cardinality(set s);
boolean subset(set small, set large);
boolean disjoint(set s1, set s2);
void sl_push(setlist *L, set s);
void just_push(setlist *L, set s);
void free_sets(setlist sl);
void print_set(set s);
