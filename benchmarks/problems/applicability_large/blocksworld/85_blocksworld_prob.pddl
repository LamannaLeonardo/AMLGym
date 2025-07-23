

(define (problem bw_rand_8)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b8)
(on b3 b4)
(ontable b4)
(on b5 b3)
(on b6 b7)
(on b7 b2)
(on b8 b1)
(clear b6)
)
(:goal
(and
(on b1 b5)
(on b2 b7)
(on b3 b1)
(on b4 b6)
(on b6 b2)
(on b7 b8)
(on b8 b3))
)
)


