

(define (problem bw_rand_7)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 - block)
(:init
(handempty)
(ontable b1)
(on b2 b5)
(ontable b3)
(ontable b4)
(on b5 b4)
(on b6 b2)
(on b7 b1)
(clear b3)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b3)
(on b2 b5)
(on b3 b4)
(on b4 b2)
(on b5 b6)
(on b6 b7))
)
)


