(define (domain elevators_sequencedstrips)
  (:requirements :typing)
  (:types 	elevator - object 
			slow_elevator fast_elevator - elevator
   			passenger - object
          	count - object
         )

(:predicates 
	(passenger_at ?person - passenger ?floor - count)
	(boarded ?person - passenger ?lift - elevator)
	(lift_at ?lift - elevator ?floor - count)
	(reachable_floor ?lift - elevator ?floor - count)
	(above ?floor1 - count ?floor2 - count)
	(passengers ?lift - elevator ?n - count)
	(can_hold ?lift - elevator ?n - count)
	(next ?n1 - count ?n2 - count)
)

(:action move_up_slow
  :parameters (?lift - slow_elevator ?f1 - count ?f2 - count )
  :precondition (and (lift_at ?lift ?f1) (above ?f1 ?f2) (reachable_floor ?lift ?f2) )
  :effect (and (lift_at ?lift ?f2) (not (lift_at ?lift ?f1)) ))

(:action move_down_slow
  :parameters (?lift - slow_elevator ?f1 - count ?f2 - count )
  :precondition (and (lift_at ?lift ?f1) (above ?f2 ?f1) (reachable_floor ?lift ?f2) )
  :effect (and (lift_at ?lift ?f2) (not (lift_at ?lift ?f1)) ))

(:action move_up_fast
  :parameters (?lift - fast_elevator ?f1 - count ?f2 - count )
  :precondition (and (lift_at ?lift ?f1) (above ?f1 ?f2) (reachable_floor ?lift ?f2) )
  :effect (and (lift_at ?lift ?f2) (not (lift_at ?lift ?f1)) ))

(:action move_down_fast
  :parameters (?lift - fast_elevator ?f1 - count ?f2 - count )
  :precondition (and (lift_at ?lift ?f1) (above ?f2 ?f1) (reachable_floor ?lift ?f2) )
  :effect (and (lift_at ?lift ?f2) (not (lift_at ?lift ?f1)) ))

(:action board
  :parameters (?p - passenger ?lift - elevator ?f - count ?n1 - count ?n2 - count)
  :precondition (and  (lift_at ?lift ?f) (passenger_at ?p ?f) (passengers ?lift ?n1) (next ?n1 ?n2) (can_hold ?lift ?n2) )
  :effect (and (not (passenger_at ?p ?f)) (boarded ?p ?lift) (not (passengers ?lift ?n1)) (passengers ?lift ?n2) ))

(:action leave 
  :parameters (?p - passenger ?lift - elevator ?f - count ?n1 - count ?n2 - count)
  :precondition (and  (lift_at ?lift ?f) (boarded ?p ?lift) (passengers ?lift ?n1) (next ?n2 ?n1) )
  :effect (and (passenger_at ?p ?f) (not (boarded ?p ?lift)) (not (passengers ?lift ?n1)) (passengers ?lift ?n2) ))
  
)

