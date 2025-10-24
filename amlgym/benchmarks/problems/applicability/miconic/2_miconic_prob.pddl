


(define (problem mixed_f4_p6_u0_v0_d0_a0_n0_a0_b0_n0_f0)
   (:domain miconic)
   (:objects p0 p1 p2 p3 p4 p5 - passenger
             f0 f1 f2 f3 - floor)


(:init
(above f0 f1)
(above f0 f2)
(above f0 f3)

(above f1 f2)
(above f1 f3)

(above f2 f3)



(origin p0 f3)
(destin p0 f1)

(origin p1 f2)
(destin p1 f1)

(origin p2 f0)
(destin p2 f3)

(origin p3 f1)
(destin p3 f3)

(origin p4 f0)
(destin p4 f3)

(origin p5 f1)
(destin p5 f3)






(lift_at f0)
)


(:goal


(and
(served p0)
(served p1)
(served p2)
(served p3)
(served p4)
(served p5)
))
)


