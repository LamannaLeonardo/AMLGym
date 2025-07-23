(define (problem transport_l6_t1_p4---int100n150_m1---int100c100---s554---e0)
(:domain transport_strips)

(:objects
l0 l1 l2 l3 l4 l5 - location
t0 - truck
p0 p1 p2 p3 - package
level0 level1 level2 level3 level4 level5 - fuellevel
)

(:init
(sum level0 level1 level1)
(sum level1 level1 level2)
(sum level2 level1 level3)
(sum level3 level1 level4)
(sum level4 level1 level5)

(connected l0 l1)
(fuelcost level1 l0 l1)
(connected l0 l2)
(fuelcost level1 l0 l2)
(connected l0 l3)
(fuelcost level1 l0 l3)
(connected l0 l5)
(fuelcost level1 l0 l5)
(connected l1 l0)
(fuelcost level1 l1 l0)
(connected l1 l4)
(fuelcost level1 l1 l4)
(connected l1 l5)
(fuelcost level1 l1 l5)
(connected l2 l0)
(fuelcost level1 l2 l0)
(connected l2 l4)
(fuelcost level1 l2 l4)
(connected l3 l0)
(fuelcost level1 l3 l0)
(connected l3 l4)
(fuelcost level1 l3 l4)
(connected l4 l1)
(fuelcost level1 l4 l1)
(connected l4 l2)
(fuelcost level1 l4 l2)
(connected l4 l3)
(fuelcost level1 l4 l3)
(connected l4 l5)
(fuelcost level1 l4 l5)
(connected l5 l0)
(fuelcost level1 l5 l0)
(connected l5 l1)
(fuelcost level1 l5 l1)
(connected l5 l4)
(fuelcost level1 l5 l4)

(at t0 l5)
(fuel t0 level5)


(at p0 l1)
(at p1 l1)
(at p2 l5)
(at p3 l3)
)

(:goal
(and
(at p0 l2)
(at p1 l3)
(at p2 l2)
(at p3 l4)
)
)
)
