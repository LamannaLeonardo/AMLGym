(define (domain blocksworld)
(:requirements :typing)
(:types
	block
)
(:predicates
	(on ?param_1 - block ?param_2 - block)
	(ontable ?param_1 - block)
	(clear ?param_1 - block)
	(handempty)
	(holding ?param_1 - block)
)


(:action pick_up
:parameters (?param_1 - block)
:precondition	(and
	(clear ?param_1)
	(handempty)
	(ontable ?param_1)
	(not (holding ?param_1))
	(not (on ?param_1 ?param_1))
)
:effect	(and
	(holding ?param_1)
	(not (clear ?param_1))
	(not (handempty))
	(not (ontable ?param_1))
)
)


(:action put_down
:parameters (?param_1 - block)
:precondition	(and
	(holding ?param_1)
	(not (clear ?param_1))
	(not (handempty))
	(not (on ?param_1 ?param_1))
	(not (ontable ?param_1))
)
:effect	(and
	(clear ?param_1)
	(handempty)
	(ontable ?param_1)
	(not (holding ?param_1))
)
)


(:action stack
:parameters (?param_1 - block ?param_2 - block)
:precondition	(and
	(holding ?param_1)
	(clear ?param_2)
	(not (on ?param_2 ?param_2))
	(not (on ?param_1 ?param_2))
	(not (on ?param_2 ?param_1))
	(not (clear ?param_1))
	(not (handempty))
	(not (ontable ?param_1))
	(not (holding ?param_2))
	(not (on ?param_1 ?param_1))
)
:effect	(and
	(clear ?param_1)
	(handempty)
	(on ?param_1 ?param_2)
	(not (holding ?param_1))
	(not (clear ?param_2))
)
)


(:action unstack
:parameters (?param_1 - block ?param_2 - block)
:precondition	(and
	(clear ?param_1)
	(handempty)
	(on ?param_1 ?param_2)
	(not (on ?param_2 ?param_2))
	(not (on ?param_2 ?param_1))
	(not (holding ?param_1))
	(not (ontable ?param_1))
	(not (holding ?param_2))
	(not (clear ?param_2))
	(not (on ?param_1 ?param_1))
)
:effect	(and
	(holding ?param_1)
	(clear ?param_2)
	(not (clear ?param_1))
	(not (handempty))
	(not (on ?param_1 ?param_2))
)
)



)