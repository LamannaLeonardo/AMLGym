(define (problem elevators_sequencedstrips_p5_5_1)
(:domain elevators_sequencedstrips)

(:objects 
n0 n1 n2 n3 n4 n5  - count
p0 p1 p2 p3 p4  - passenger
fast0 fast1  - fast_elevator
slow0_0 - slow_elevator
)

(:init
(next n0 n1) (next n1 n2) (next n2 n3) (next n3 n4) (next n4 n5) 

(above n0 n1) (above n0 n2) (above n0 n3) (above n0 n4) (above n0 n5) 
(above n1 n2) (above n1 n3) (above n1 n4) (above n1 n5) 
(above n2 n3) (above n2 n4) (above n2 n5) 
(above n3 n4) (above n3 n5) 
(above n4 n5) 

(lift_at fast0 n0)
(passengers fast0 n0)
(can_hold fast0 n1) 
(reachable_floor fast0 n0)(reachable_floor fast0 n2)(reachable_floor fast0 n4)

(lift_at fast1 n0)
(passengers fast1 n0)
(can_hold fast1 n1) 
(reachable_floor fast1 n0)(reachable_floor fast1 n2)(reachable_floor fast1 n4)

(lift_at slow0_0 n3)
(passengers slow0_0 n0)
(can_hold slow0_0 n1) 
(reachable_floor slow0_0 n0)(reachable_floor slow0_0 n1)(reachable_floor slow0_0 n2)(reachable_floor slow0_0 n3)(reachable_floor slow0_0 n4)(reachable_floor slow0_0 n5)

(passenger_at p0 n5)
(passenger_at p1 n3)
(passenger_at p2 n3)
(passenger_at p3 n2)
(passenger_at p4 n0)








)

(:goal
(and
(passenger_at p0 n2)
(passenger_at p1 n1)
(passenger_at p2 n0)
(passenger_at p3 n1)
(passenger_at p4 n4)
))


)
