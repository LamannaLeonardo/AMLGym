#include <stdlib.h>
#include <stdio.h>
#include "setlists.h"


/*
* The utilities here are just for handling bitvector sets and lists of sets.
*/


#define through(x) for (x=0; x<SSZ; x++)

/*
* Empty the set s
*/

void emptyset(set s)
{
    int p;
    through(p) s[p] = 0;
}


/*
* Copy the contents of source into dest
*/

void assign(set dest, set source)
{
    int p;
    through(p) dest[p] = source[p];
}


/*
* Add x as an element to s (has no effect if x already in s)
*/

void putinset(int x, set s)
{
    s[x/WS] |= ((Stype)1 << (x%WS));
}


/*
* Remove element x from s (has no effect if x not in s)
*/

void putoutset(int x, set s)
{
    s[x/WS] &= ~((Stype)1 << (x%WS));
}


/*
* x is a member of s
*/

boolean isin(int x, set s)
{
    return ((s[x/WS] & ((Stype)1 << (x%WS))) != 0);
}


/*
* Allocate memory for a new set {x} and return a pointer to it
*/

set singleton(int x)
{
    set s;
    s = (set) malloc(sizeof(SET));
    emptyset(s);
    putinset(x,s);
    return s;
}


/*
* The number of members of s
*/

int cardinality(set s)
{
    int p, q, k=0;
    through(p)
	for (q=0; q<WS; q++)
	    if (s[p] & ((Stype)1 << q))
		k++;
    return k;
}


/*
* small is a subset of large
*/

boolean subset(set small, set large)
{
    int p;
    through(p)
	if (small[p] & ~(large[p])) return false;
    return true;
}


/*
* s1 and s2 have no element in common
*/

boolean disjoint(set s1, set s2)
{
    int p;
    through(p) if (s1[p] & s2[p]) return false;
    return true;
}


/*
* Now just a few utilities for operations on lists of sets
*/



/*
* Insert a set into a list after the sets of smaller cardinality
*/

void sl_push(setlist *L, set s)
{
    int cs;
    setlist ptr;
    setlist item;

    item = (setlist) malloc(sizeof(SETLIST));
    item->s = s;

    if (!*L) {
	*L = item;
	(*L)->up = (*L)->down = 0;
    }
    else {
	cs = cardinality(s);
	if (cardinality((*L)->s) >= cs) {
	    item->up = *L;
	    (*L)->down = item;
	    (*L) = item;
	}
	else {
	    forallsets(*L,ptr)
		if (!ptr->up || cardinality(ptr->up->s) > cs) break;
	    item->up = ptr->up;
	    item->down = ptr;
	    ptr->up = item;
	    if (item->up) item->up->down = item;
	}
    }
}


void just_push(setlist *L, set s)
{
    setlist ptr;
    setlist item;

    item = (setlist) malloc(sizeof(SETLIST));
    item->s = s;

    if (!*L) {
	*L = item;
	(*L)->up = (*L)->down = 0;
    }
    else {
	forallsets(*L,ptr) if (!ptr->up) break;
	item->up = 0;
	item->down = ptr;
	ptr->up = item;
    }
}



/*
* Free the memory used to hold the deadlocks
*/

void free_sets(setlist sl)
{
    if (sl) {
	free_sets(sl->up);
	free(sl->s);
	free(sl);
    }
}


/*
* Print out a set using only the required number of words.
* Terminate each word with a space.
*/

void print_set(set s)
{
    int x,y;

    through(x) if (s[x]) y = x;
    through(x) if (x <= y) printf("%lu ",s[x]);
}
