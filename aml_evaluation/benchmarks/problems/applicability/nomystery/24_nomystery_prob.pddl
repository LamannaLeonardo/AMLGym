(define (problem transport_l2_t1_p1---int100n150_m1---int100c100---s273---e0)
(:domain transport_strips)

(:objects
l0 l1 - location
t0 - truck
p0 - package
level0 level1 level2 - fuellevel
)

(:init
(sum level0 level1 level1)
(sum level1 level1 level2)

(connected l0 l1)
(fuelcost level1 l0 l1)
(connected l1 l0)
(fuelcost level1 l1 l0)

(at t0 l0)
(fuel t0 level2)


(at p0 l1)
)

(:goal
(and
(at p0 l0)
)
)
)
