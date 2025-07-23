(define (problem elevators_sequencedstrips_p4_3_1)
(:domain elevators_sequencedstrips)

(:objects 
n0 n1 n2 n3 n4  - count
p0 p1 p2  - passenger
fast0  - fast_elevator
slow0_0 slow1_0 - slow_elevator
)

(:init
(next n0 n1) (next n1 n2) (next n2 n3) (next n3 n4) 

(above n0 n1) (above n0 n2) (above n0 n3) (above n0 n4) 
(above n1 n2) (above n1 n3) (above n1 n4) 
(above n2 n3) (above n2 n4) 
(above n3 n4) 

(lift_at fast0 n0)
(passengers fast0 n0)
(can_hold fast0 n1) 
(reachable_floor fast0 n0)(reachable_floor fast0 n1)(reachable_floor fast0 n2)(reachable_floor fast0 n3)(reachable_floor fast0 n4)

(lift_at slow0_0 n2)
(passengers slow0_0 n0)
(can_hold slow0_0 n1) 
(reachable_floor slow0_0 n0)(reachable_floor slow0_0 n1)(reachable_floor slow0_0 n2)

(lift_at slow1_0 n3)
(passengers slow1_0 n0)
(can_hold slow1_0 n1) 
(reachable_floor slow1_0 n2)(reachable_floor slow1_0 n3)(reachable_floor slow1_0 n4)

(passenger_at p0 n3)
(passenger_at p1 n4)
(passenger_at p2 n0)









)

(:goal
(and
(passenger_at p0 n2)
(passenger_at p1 n3)
(passenger_at p2 n1)
))


)
