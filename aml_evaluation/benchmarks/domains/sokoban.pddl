(define (domain typed_sokoban)
(:requirements :typing)
(:types loc dir box)
(:predicates 
             (at_robot ?l - loc)
             (at ?o - box ?l - loc)
             (adjacent ?l1 - loc ?l2 - loc ?d - dir) 
             (clear ?l - loc)
)


(:action move
:parameters (?from - loc ?to - loc ?dir - dir)
:precondition (and (clear ?to) (at_robot ?from) (adjacent ?from ?to ?dir))
:effect (and (at_robot ?to) (not (at_robot ?from)))
)
             

(:action push
:parameters  (?rloc - loc ?bloc - loc ?floc - loc ?dir - dir ?b - box)
:precondition (and (at_robot ?rloc) (at ?b ?bloc) (clear ?floc)
	           (adjacent ?rloc ?bloc ?dir) (adjacent ?bloc ?floc ?dir))

:effect (and (at_robot ?bloc) (at ?b ?floc) (clear ?bloc)
             (not (at_robot ?rloc)) (not (at ?b ?bloc)) (not (clear ?floc)))
)
)


