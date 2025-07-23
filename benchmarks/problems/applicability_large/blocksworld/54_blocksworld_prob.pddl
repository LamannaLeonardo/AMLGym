

(define (problem bw_rand_7)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(ontable b3)
(on b4 b7)
(ontable b5)
(ontable b6)
(on b7 b5)
(clear b2)
(clear b3)
(clear b4)
(clear b6)
)
(:goal
(and
(on b2 b6)
(on b4 b3)
(on b5 b7)
(on b7 b4))
)
)


