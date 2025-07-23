

(define (problem bw_rand_8)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(ontable b1)
(on b2 b6)
(ontable b3)
(on b4 b1)
(on b5 b8)
(on b6 b4)
(on b7 b3)
(ontable b8)
(clear b2)
(clear b5)
(clear b7)
)
(:goal
(and
(on b1 b4)
(on b2 b5)
(on b3 b6)
(on b4 b7)
(on b6 b8)
(on b7 b2)
(on b8 b1))
)
)


