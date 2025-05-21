(define (problem elevators-sequencedstrips-p3_2_1)
(:domain elevators-sequencedstrips)

(:objects 
n0 n1 n2 n3  - count
p0 p1  - passenger
fast0  - fast-elevator
slow0-0 - slow-elevator
)

(:init
(next n0 n1) (next n1 n2) (next n2 n3) 

(above n0 n1) (above n0 n2) (above n0 n3) 
(above n1 n2) (above n1 n3) 
(above n2 n3) 

(lift-at fast0 n0)
(passengers fast0 n0)
(can-hold fast0 n1) 
(reachable-floor fast0 n0)(reachable-floor fast0 n1)(reachable-floor fast0 n2)(reachable-floor fast0 n3)

(lift-at slow0-0 n0)
(passengers slow0-0 n0)
(can-hold slow0-0 n1) 
(reachable-floor slow0-0 n0)(reachable-floor slow0-0 n1)(reachable-floor slow0-0 n2)(reachable-floor slow0-0 n3)

(passenger-at p0 n0)
(passenger-at p1 n0)







)

(:goal
(and
(passenger-at p0 n1)
(passenger-at p1 n3)
))


)
