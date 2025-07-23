(define (problem transport_l4_t1_p2---int100n150_m1---int100c100---s126---e0)
(:domain transport_strips)

(:objects
l0 l1 l2 l3 - location
t0 - truck
p0 p1 - package
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
(connected l0 l3)
(fuelcost level1 l0 l3)
(connected l1 l0)
(fuelcost level1 l1 l0)
(connected l1 l2)
(fuelcost level1 l1 l2)
(connected l1 l3)
(fuelcost level1 l1 l3)
(connected l2 l0)
(fuelcost level1 l2 l0)
(connected l2 l1)
(fuelcost level1 l2 l1)
(connected l2 l3)
(fuelcost level1 l2 l3)
(connected l3 l0)
(fuelcost level1 l3 l0)
(connected l3 l1)
(fuelcost level1 l3 l1)
(connected l3 l2)
(fuelcost level1 l3 l2)

(at t0 l3)
(fuel t0 level3)


(at p0 l2)
(at p1 l3)
)

(:goal
(and
(at p0 l1)
(at p1 l0)
)
)
)
