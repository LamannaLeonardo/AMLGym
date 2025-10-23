(define (domain grid)
(:requirements :typing)
(:types place key shape)

(:predicates
		(conn ?x - place ?y - place)
		(key_shape ?k - key ?s - shape)
		(lock_shape ?x - place ?s - shape)
		(at ?r - key ?x - place)
		(at_robot ?x - place)
		(locked ?x - place)
		(holding ?k - key)
		(open ?x - place)
		(arm_empty))

(:action unlock
		:parameters (?curpos - place ?lockpos - place ?key - key ?shape - shape)
		:precondition (and (conn ?curpos ?lockpos) (key_shape ?key ?shape) (lock_shape ?lockpos ?shape) (at_robot ?curpos) (locked ?lockpos) (holding ?key))
		:effect (and  (open ?lockpos) (not (locked ?lockpos))))

(:action move
		:parameters (?curpos - place ?nextpos - place)
		:precondition (and (at_robot ?curpos) (conn ?curpos ?nextpos) (open ?nextpos))
		:effect (and (at_robot ?nextpos) (not (at_robot ?curpos))))

(:action pickup
		:parameters (?curpos - place ?key - key)
		:precondition (and (at_robot ?curpos) (at ?key ?curpos) (arm_empty))
		:effect (and (holding ?key)    (not (at ?key ?curpos)) (not (arm_empty))))

(:action pickup_and_loose
		:parameters (?curpos - place ?newkey - key ?oldkey - key)
		:precondition (and (at_robot ?curpos) (holding ?oldkey) (at ?newkey ?curpos))
		:effect (and (holding ?newkey) (at ?oldkey ?curpos)         (not (holding ?oldkey)) (not (at ?newkey ?curpos))))

(:action putdown
		:parameters (?curpos - place ?key - key)
		:precondition (and (at_robot ?curpos) (holding ?key))
		:effect (and (arm_empty) (at ?key ?curpos) (not (holding ?key))))

)

