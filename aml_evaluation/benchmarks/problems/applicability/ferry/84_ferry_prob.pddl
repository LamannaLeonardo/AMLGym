(define (problem ferry_l3_c2)
(:domain ferry)
(:objects l0 l1 l2  - location
          c0 c1  - car
)
(:init
(noteq l0 l1)
(noteq l1 l0)
(noteq l0 l2)
(noteq l2 l0)
(noteq l1 l2)
(noteq l2 l1)
(empty_ferry)
(at c0 l0)
(at c1 l0)
(at_ferry l1)
)
(:goal
(and
(at c0 l1)
(at c1 l2)
)
)
)
