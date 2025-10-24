;;created by tomas de la rosa
;;domain for painting floor tiles with two colors

(define (domain floor_tile)
(:requirements :typing)
(:types robot tile color - object)

(:predicates 	
		(robot_at ?r - robot ?x - tile)
		(up ?x - tile ?y - tile)
		(down ?x - tile ?y - tile)
		(right ?x - tile ?y - tile)
		(left ?x - tile ?y - tile)
		
		(clear ?x - tile)
                (painted ?x - tile ?c - color)
		(robot_has ?r - robot ?c - color)
                (available_color ?c - color)
                (free_color ?r - robot))


(:action change_color
  :parameters (?r - robot ?c - color ?c2 - color)
  :precondition (and (robot_has ?r ?c) (available_color ?c2))
  :effect (and (not (robot_has ?r ?c)) (robot_has ?r ?c2))
) 


(:action paint_up
  :parameters (?r - robot ?y - tile ?x - tile ?c - color)
  :precondition (and (robot_has ?r ?c) (robot_at ?r ?x) (up ?y ?x) (clear ?y))
  :effect (and (not (clear ?y)) (painted ?y ?c))
)


(:action paint_down
  :parameters (?r - robot ?y - tile ?x - tile ?c - color)
  :precondition (and (robot_has ?r ?c) (robot_at ?r ?x) (down ?y ?x) (clear ?y))
  :effect (and (not (clear ?y)) (painted ?y ?c))
)


; robot movements
(:action move_up
  :parameters (?r - robot ?x - tile ?y - tile)
  :precondition (and (robot_at ?r ?x) (up ?y ?x) (clear ?y))
  :effect (and (robot_at ?r ?y) (not (robot_at ?r ?x))
               (clear ?x) (not (clear ?y)))
)


(:action move_down
  :parameters (?r - robot ?x - tile ?y - tile)
  :precondition (and (robot_at ?r ?x) (down ?y ?x) (clear ?y))
  :effect (and (robot_at ?r ?y) (not (robot_at ?r ?x))
               (clear ?x) (not (clear ?y)))
)

(:action move_right
  :parameters (?r - robot ?x - tile ?y - tile)
  :precondition (and (robot_at ?r ?x) (right ?y ?x) (clear ?y))
  :effect (and (robot_at ?r ?y) (not (robot_at ?r ?x))
               (clear ?x) (not (clear ?y)))
)

(:action move_left
  :parameters (?r - robot ?x - tile ?y - tile)
  :precondition (and (robot_at ?r ?x) (left ?y ?x) (clear ?y))
  :effect (and (robot_at ?r ?y) (not (robot_at ?r ?x))
               (clear ?x) (not (clear ?y)))
)

)

