

(define (problem bw_rand_8)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b6)
(on b3 b2)
(on b4 b3)
(on b5 b7)
(on b6 b5)
(ontable b7)
(on b8 b4)
(clear b1)
)
(:goal
(and
(on b1 b8)
(on b2 b7)
(on b3 b6)
(on b4 b1)
(on b6 b4)
(on b7 b5))
)
)


