


(define (problem mixed-f5-p3-u0-v0-d0-a0-n0-a0-b0-n0-f0)
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



(origin p0 f1)
(destin p0 f0)

(origin p1 f3)
(destin p1 f1)

(origin p2 f4)
(destin p2 f0)






(lift-at f0)
)


(:goal


(and
(served p0)
(served p1)
(served p2)
))
)


