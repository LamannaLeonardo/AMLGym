

(define (problem bw_rand_8)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b7)
(ontable b2)
(on b3 b6)
(on b4 b5)
(on b5 b8)
(ontable b6)
(on b7 b2)
(on b8 b3)
(clear b1)
(clear b4)
)
(:goal
(and
(on b2 b7)
(on b3 b2)
(on b5 b4)
(on b6 b1)
(on b8 b3))
)
)


