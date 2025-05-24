(define (domain ferry)
(:requirements :typing)
(:types car location)

(:predicates
		(noteq ?x - location ?y - location)
		(at_ferry ?l - location)
		(at ?c - car ?l - location)
		(empty_ferry)
		(on ?c - car)
)

(:action sail
		:parameters (?from - location ?to - location)
		:precondition (and (noteq ?from ?to) (at_ferry ?from))
		:effect (and  (at_ferry ?to) 		     (not (at_ferry ?from))))

(:action board
		:parameters (?car - car ?loc - location)
		:precondition (and (at ?car ?loc) (at_ferry ?loc) (empty_ferry))
		:effect (and (on ?car) 		    (not (at ?car ?loc))  		    (not (empty_ferry))))

(:action debark
		:parameters (?car - car ?loc - location)
		:precondition (and (on ?car) (at_ferry ?loc))
		:effect (and (at ?car ?loc) 		    (empty_ferry) 		    (not (on ?car))))

)

