;; gold miner domain

(define (domain gold_miner_typed)
(:requirements :typing)
(:types loc)

(:predicates 	
		(robot_at ?x - loc)
		(bomb_at ?x - loc )
		(laser_at ?x - loc)
		(soft_rock_at ?x - loc)
		(hard_rock_at ?x - loc)
		(gold_at ?x - loc)
		(arm_empty)
		(holds_bomb)
        (holds_laser)
		(holds_gold)
		(clear ?x - loc)		
		(connected ?x - loc ?y - loc)
)
 

; move to an adjacent empty grid location
(:action move
  :parameters (?x - loc ?y - loc)
  :precondition (and (robot_at ?x) (connected ?x ?y) (clear ?y))
  :effect (and (robot_at ?y) (not (robot_at ?x)))
)

(:action pickup_laser
  :parameters (?x - loc)
  :precondition (and (robot_at ?x) (laser_at ?x) (arm_empty))
  :effect (and (not (arm_empty)) (holds_laser) (not (laser_at ?x)) )
)

;have to be over the bomb location to pick the bomb 
(:action pickup_bomb
  :parameters (?x - loc)
  :precondition (and (robot_at ?x) (bomb_at ?x) (arm_empty))
  :effect (and (not (arm_empty)) (holds_bomb))
)

(:action putdown_laser
  :parameters (?x - loc)
  :precondition (and (robot_at ?x) (holds_laser))
  :effect (and (arm_empty) (not (holds_laser)) (laser_at ?x))
)

;bomb an adjacent location that has soft_rock
(:action detonate_bomb 
  :parameters (?x - loc ?y - loc)
  :precondition (and (robot_at ?x) (holds_bomb) 
                     (connected ?x ?y) (soft_rock_at ?y))
  :effect (and (not (holds_bomb)) (arm_empty) (clear ?y) (not (soft_rock_at ?y)))
)

(:action fire_laser
  :parameters (?x - loc ?y - loc)
  :precondition (and (robot_at ?x) (holds_laser) 
                     (connected ?x ?y)) 
  :effect (and (clear ?y) (not (soft_rock_at ?y)) (not (gold_at ?y))
               (not (hard_rock_at ?y)))
)        
					   
;mine gold !
;the robot has to be over the gold location to pick it up
(:action pick_gold
  :parameters (?x - loc)
  :precondition (and (robot_at ?x) (arm_empty) (gold_at ?x))
  :effect (and (not (arm_empty)) (holds_gold))
)
)
