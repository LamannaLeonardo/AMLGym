#ifndef GN2
#define GN2

#include <stdio.h>
#include <stdlib.h>
#include "definitions.h"

typedef enum {
  finished,		/* Blocks in goal position */
  GN2ready,		/* Blocks with which constructive move possible */
  stuck_on_tower,	/* Blocks clear but not able to move constructively */
  stuck_on_table,	/* Blocks clear but not able to move constructively */
  unclear,		/* Blocks not clear but whose goal position OK */
  hopeless,		/* None of the above */
  number_of_GN2lists
} GN2list;

typedef struct GN2BLK {
  int offset;		/* Number identifying this block */
  struct GN2BLK* si;	/* Block below this one currently */
  struct GN2BLK* sg;	/* Block below this one in goal */
  struct GN2BLK* isi;	/* Block above this one currently */
  struct GN2BLK* isg;	/* Block above this one in goal */
  boolean clear;	/* This block is clear */
  boolean inposition;	/* This block does not need to move */
  GN2list loc;		/* Which list this one is in */
  struct GN2BLK* next;	/* Next block in list */
  struct GN2BLK* last;	/* Previous block in list */
  struct GN2BLK* delta;    /* Link for making deadlock */
  struct GN2BLK* idelta;   /* Inverse of delta */
  boolean examined;	/* Already visited to determine inposition */
  struct GN2BLK* concierge;   /* Block at bottom of the tower */
  struct GN2BLK* g_concierge; /* Block at bottom of the goal tower */
  struct GN2BLK* top;      /* Block at top of the current tower */
  struct GN2BLK* deltapoint;  /* Highest block in position in goal tower */
} GN2BLOCK, *GN2block;

typedef struct GN2BLKLST {
  GN2block head;
  GN2block tail;
} GN2BLOCKLIST, *GN2blocklist;

typedef struct {
  GN2block obj;		/* The block which is moved */
  GN2block dst;		/* Its destination */
} GN2MOVE, *GN2move;

typedef struct {
  int plan_length;
  GN2move M;
} GN2PLAN, *GN2plan;

typedef struct {
  int size;		/* Number of blocks in instance (excluding table) */
  GN2block B;           /* The blocks of course */
  GN2block table;
  GN2BLOCKLIST L[number_of_GN2lists];		/* Categories of block */
  GN2PLAN P;		/* The solution */
  GN2BLOCKLIST deadlock;
} GN2INSTANCE, *GN2instance;



/* Function prototypes */

int GN2length(int i[], int g[], int N, int verbosity);
GN2instance get_GN2problem (int i[], int g[], int N);
void free_GN2problem(GN2instance I);
GN2plan gn2 (GN2instance I);
void GN2initialise_2 (GN2instance I);
boolean GN2inpos (GN2block b);
void GN2putin (GN2instance I, GN2block b, GN2list to);
void GN2solve_2 (GN2instance I);
void make_GN2move (GN2instance I, GN2block object, GN2block destination);
void GN2relocate (GN2instance I, GN2block b);
void add_GN2move(GN2instance I, GN2block object, GN2block destination);
GN2block GN2deadlock_breaker (GN2instance I);
GN2block GN2delta_of (GN2block b);
void printGN2plan(int i[], int g[], GN2instance I);

#endif


