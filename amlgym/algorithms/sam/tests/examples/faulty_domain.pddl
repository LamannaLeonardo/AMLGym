(define (domain depot)
(:requirements :typing :fluents :disjunctive-preconditions)
(:types 	place locatable - object
	depot distributor - place
	truck hoist surface - locatable
	pallet crate - surface
)

(:predicates (at ?x - locatable ?y - place)
	(on ?x - crate ?y - surface)
	(in ?x - crate ?y - truck)
	(lifting ?x - hoist ?y - crate)
	(available ?x - hoist)
	(clear ?x - surface)
)

(:functions (load_limit ?t - truck)
	(current_load ?t - truck)
	(weight ?c - crate)
	(fuel-cost )
)

(:action drive
	:parameters (?x - truck ?y - place ?z - place)
	:precondition (and (at ?x ?y)
				)
	:effect (and (at ?x ?z) (not (at ?x ?y))
		(increase (fuel-cost ) 10.0)
))

(:action lift
	:parameters (?x - hoist ?y - crate ?z - surface ?p - place)
	:precondition (and (at ?x ?p) (available ?x) (on ?y ?z) (clear ?y) (at ?y ?p)
				)
	:effect (and (clear ?z) (lifting ?x ?y) (not (available ?x)) (not (on ?y ?z)) (not (at ?y ?p)) (not (clear ?y))
		(increase (fuel-cost ) 4.0)
))

(:action drop
	:parameters (?x - hoist ?y - crate ?z - surface ?p - place)
	:precondition (and (clear ?z) (at ?z ?p) (lifting ?x ?y) (at ?x ?p)
				)
	:effect (and (available ?x) (on ?y ?z) (at ?y ?p) (clear ?y) (not (clear ?z)) (not (lifting ?x ?y))))

(:action load
	:parameters (?x - hoist ?y - crate ?z - truck ?p - place)
	:precondition (and (at ?z ?p) (lifting ?x ?y) (at ?x ?p)
				(<= (+ (current_load ?z) (weight ?y)) (load_limit ?z)))
	:effect (and (in ?y ?z) (available ?x) (not (lifting ?x ?y))
		(increase (current_load ?z) (weight ?y))
))

(:action unload
	:parameters (?x - hoist ?y - crate ?z - truck ?p - place)
	:precondition (and (in ?y ?z) (at ?z ?p) (available ?x) (at ?x ?p)
				)
	:effect (and (lifting ?x ?y) (not (in ?y ?z)) (not (available ?x))
		(decrease (current_load ?z) (weight ?y))
))

)