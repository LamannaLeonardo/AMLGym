(define (problem elevators-sequencedstrips-p6_6_1)
(:domain elevators-sequencedstrips)

(:objects 
n0 n1 n2 n3 n4 n5 n6  - count
p0 p1 p2 p3 p4 p5  - passenger
fast0 fast1  - fast-elevator
slow0-0 slow1-0 - slow-elevator
)

(:init
(next n0 n1) (next n1 n2) (next n2 n3) (next n3 n4) (next n4 n5) (next n5 n6) 

(above n0 n1) (above n0 n2) (above n0 n3) (above n0 n4) (above n0 n5) (above n0 n6) 
(above n1 n2) (above n1 n3) (above n1 n4) (above n1 n5) (above n1 n6) 
(above n2 n3) (above n2 n4) (above n2 n5) (above n2 n6) 
(above n3 n4) (above n3 n5) (above n3 n6) 
(above n4 n5) (above n4 n6) 
(above n5 n6) 

(lift-at fast0 n0)
(passengers fast0 n0)
(can-hold fast0 n1) 
(reachable-floor fast0 n0)(reachable-floor fast0 n1)(reachable-floor fast0 n2)(reachable-floor fast0 n3)(reachable-floor fast0 n4)(reachable-floor fast0 n5)(reachable-floor fast0 n6)

(lift-at fast1 n6)
(passengers fast1 n0)
(can-hold fast1 n1) 
(reachable-floor fast1 n0)(reachable-floor fast1 n1)(reachable-floor fast1 n2)(reachable-floor fast1 n3)(reachable-floor fast1 n4)(reachable-floor fast1 n5)(reachable-floor fast1 n6)

(lift-at slow0-0 n3)
(passengers slow0-0 n0)
(can-hold slow0-0 n1) (can-hold slow0-0 n2) 
(reachable-floor slow0-0 n0)(reachable-floor slow0-0 n1)(reachable-floor slow0-0 n2)(reachable-floor slow0-0 n3)

(lift-at slow1-0 n3)
(passengers slow1-0 n0)
(can-hold slow1-0 n1) (can-hold slow1-0 n2) 
(reachable-floor slow1-0 n3)(reachable-floor slow1-0 n4)(reachable-floor slow1-0 n5)(reachable-floor slow1-0 n6)

(passenger-at p0 n3)
(passenger-at p1 n2)
(passenger-at p2 n1)
(passenger-at p3 n4)
(passenger-at p4 n6)
(passenger-at p5 n1)











)

(:goal
(and
(passenger-at p0 n5)
(passenger-at p1 n3)
(passenger-at p2 n6)
(passenger-at p3 n1)
(passenger-at p4 n1)
(passenger-at p5 n2)
))


)
