


(define (problem mixed_f5_p3_u0_v0_d0_a0_n0_a0_b0_n0_f0)
   (:domain miconic)
   (:objects p0 p1 p2 - passenger
             f0 f1 f2 f3 f4 - floor)


(:init
(above f0 f1)
(above f0 f2)
(above f0 f3)
(above f0 f4)

(above f1 f2)
(above f1 f3)
(above f1 f4)

(above f2 f3)
(above f2 f4)

(above f3 f4)



(origin p0 f0)
(destin p0 f2)

(origin p1 f2)
(destin p1 f0)

(origin p2 f1)
(destin p2 f2)






(lift_at f0)
)


(:goal


(and
(served p0)
(served p1)
(served p2)
))
)


