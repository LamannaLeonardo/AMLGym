#ifndef GN1
#define GN1

#include <stdio.h>
#include <stdlib.h>
#include "definitions.h"

typedef enum {
  null,
  GN1ready,		/* Blocks with which constructive move possible */
  stuck,		/* Blocks clear but not able to move constructively */
  number_of_GN1lists
} GN1list;

typedef struct GN1BLK {
  int offset;		/* Number identifying this block */
  struct GN1BLK* si;	/* Block below this one currently */
  struct GN1BLK* sg;	/* Block below this one in goal */
  struct GN1BLK* isi;	/* Block above this one currently */
  struct GN1BLK* isg;	/* Block above this one in goal */
  boolean clear;	/* This block is clear */
  boolean inposition;	/* This block does not need to move */
  GN1list loc;		/* Which list this one is in */
  struct GN1BLK* next;	/* Next block in list */
  struct GN1BLK* last;	/* Previous block in list */
  boolean examined;	/* Already visited to determine inposition */
} GN1BLOCK, *GN1block;

typedef struct GN1BLKLST {
  GN1block head;
  GN1block tail;
} GN1BLOCKLIST, *GN1blocklist;

typedef struct {
  GN1block obj;		/* The block which is moved */
  GN1block dst;		/* Its destination */
} GN1MOVE, *GN1move;

typedef struct {
  int plan_length;
  GN1MOVE * M;
} GN1PLAN, *GN1plan;

typedef struct {
  int size;		/* Number of blocks in instance (excluding table) */
  GN1block B;  	        /* The blocks (of course) */
  GN1block table;
  GN1BLOCKLIST L[number_of_GN1lists]; /* Categories of block */
  GN1PLAN P;		/* The solution */
} GN1INSTANCE, *GN1instance;



/* Function prototypes */

int GN1length(int i[], int g[], int N, int verbosity);
GN1instance get_GN1problem (int i[], int g[], int N);
void free_GN1problem(GN1instance I);
GN1plan gn1 (GN1instance I);
void GN1initialise (GN1instance I);
boolean GN1inpos (GN1block b);
void GN1putin (GN1instance I, GN1block b, GN1list to);
void GN1putout(GN1block b, GN1blocklist from);
void GN1solve (GN1instance I);
void make_GN1move (GN1instance I, GN1block object, GN1block destination);
void GN1relocate (GN1instance I, GN1block b);
void add_GN1move(GN1instance I, GN1block object, GN1block destination);
void printGN1plan(int i[], int g[], GN1instance I);

#endif




