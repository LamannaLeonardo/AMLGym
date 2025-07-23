

(define (problem bw_rand_8)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(on b1 b2)
(ontable b2)
(on b3 b8)
(on b4 b1)
(ontable b5)
(on b6 b3)
(on b7 b4)
(on b8 b7)
(clear b5)
(clear b6)
)
(:goal
(and
(on b1 b8)
(on b2 b3)
(on b4 b5)
(on b5 b6)
(on b8 b4))
)
)


