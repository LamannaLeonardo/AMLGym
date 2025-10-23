(define (domain gripper_strips)
 (:requirements :strips :typing)
 (:types room ball robot gripper)
 (:predicates (at_robby ?r - robot ?x - room)
 	      (at ?o - ball ?x - room)
	      (free ?r - robot ?g - gripper)
	      (carry ?r - robot ?o - ball ?g - gripper))

   (:action move
       :parameters  (?r - robot ?from ?to - room)
       :precondition (and  (at_robby ?r ?from))
       :effect (and  (at_robby ?r ?to)
		     (not (at_robby ?r ?from))))

   (:action pick
       :parameters (?r - robot ?obj - ball ?room - room ?g - gripper)
       :precondition  (and  (at ?obj ?room) (at_robby ?r ?room) (free ?r ?g))
       :effect (and (carry ?r ?obj ?g)
		    (not (at ?obj ?room))
		    (not (free ?r ?g))))

   (:action drop
       :parameters (?r - robot ?obj - ball ?room - room ?g - gripper)
       :precondition  (and  (carry ?r ?obj ?g) (at_robby ?r ?room))
       :effect (and (at ?obj ?room)
		    (free ?r ?g)
		    (not (carry ?r ?obj ?g)))))