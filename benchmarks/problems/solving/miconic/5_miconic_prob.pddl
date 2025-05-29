


(define (problem mixed_f6_p4_u0_v0_d0_a0_n0_a0_b0_n0_f0)
   (:domain miconic)
   (:objects p0 p1 p2 p3 - passenger
             f0 f1 f2 f3 f4 f5 - floor)


(:init
(above f0 f1)
(above f0 f2)
(above f0 f3)
(above f0 f4)
(above f0 f5)

(above f1 f2)
(above f1 f3)
(above f1 f4)
(above f1 f5)

(above f2 f3)
(above f2 f4)
(above f2 f5)

(above f3 f4)
(above f3 f5)

(above f4 f5)



(origin p0 f1)
(destin p0 f3)

(origin p1 f3)
(destin p1 f5)

(origin p2 f4)
(destin p2 f5)

(origin p3 f4)
(destin p3 f1)






(lift_at f0)
)


(:goal


(and
(served p0)
(served p1)
(served p2)
(served p3)
))
)


