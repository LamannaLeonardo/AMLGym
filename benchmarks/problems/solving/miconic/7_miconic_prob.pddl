


(define (problem mixed_f7_p5_u0_v0_d0_a0_n0_a0_b0_n0_f0)
   (:domain miconic)
   (:objects p0 p1 p2 p3 p4 - passenger
             f0 f1 f2 f3 f4 f5 f6 - floor)


(:init
(above f0 f1)
(above f0 f2)
(above f0 f3)
(above f0 f4)
(above f0 f5)
(above f0 f6)

(above f1 f2)
(above f1 f3)
(above f1 f4)
(above f1 f5)
(above f1 f6)

(above f2 f3)
(above f2 f4)
(above f2 f5)
(above f2 f6)

(above f3 f4)
(above f3 f5)
(above f3 f6)

(above f4 f5)
(above f4 f6)

(above f5 f6)



(origin p0 f2)
(destin p0 f0)

(origin p1 f6)
(destin p1 f5)

(origin p2 f1)
(destin p2 f6)

(origin p3 f4)
(destin p3 f1)

(origin p4 f0)
(destin p4 f2)






(lift_at f0)
)


(:goal


(and
(served p0)
(served p1)
(served p2)
(served p3)
(served p4)
))
)


