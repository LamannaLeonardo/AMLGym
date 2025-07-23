

(define (problem bw_rand_8)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b7)
(on b4 b1)
(on b5 b3)
(on b6 b5)
(ontable b7)
(ontable b8)
(clear b2)
(clear b4)
(clear b6)
(clear b8)
)
(:goal
(and
(on b1 b3)
(on b2 b7)
(on b3 b6)
(on b4 b8)
(on b6 b4)
(on b7 b1))
)
)


