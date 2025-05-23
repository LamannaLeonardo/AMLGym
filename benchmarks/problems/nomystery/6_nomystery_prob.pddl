(define (problem transport-l5-t1-p3---int100n150-m1---int100c100---s545---e0)
(:domain transport-strips)

(:objects
l0 l1 l2 l3 l4 - location
t0 - truck
p0 p1 p2 - package
level0 level1 level2 level3 - fuellevel
)

(:init
(sum level0 level1 level1)
(sum level1 level1 level2)
(sum level2 level1 level3)

(connected l0 l1)
(fuelcost level1 l0 l1)
(connected l0 l2)
(fuelcost level1 l0 l2)
(connected l1 l0)
(fuelcost level1 l1 l0)
(connected l1 l3)
(fuelcost level1 l1 l3)
(connected l1 l4)
(fuelcost level1 l1 l4)
(connected l2 l0)
(fuelcost level1 l2 l0)
(connected l2 l3)
(fuelcost level1 l2 l3)
(connected l2 l4)
(fuelcost level1 l2 l4)
(connected l3 l1)
(fuelcost level1 l3 l1)
(connected l3 l2)
(fuelcost level1 l3 l2)
(connected l3 l4)
(fuelcost level1 l3 l4)
(connected l4 l1)
(fuelcost level1 l4 l1)
(connected l4 l2)
(fuelcost level1 l4 l2)
(connected l4 l3)
(fuelcost level1 l4 l3)

(at t0 l1)
(fuel t0 level3)


(at p0 l4)
(at p1 l2)
(at p2 l2)
)

(:goal
(and
(at p0 l2)
(at p1 l4)
(at p2 l4)
)
)
)
