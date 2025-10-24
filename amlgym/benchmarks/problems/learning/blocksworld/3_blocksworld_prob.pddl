

(define (problem bw_rand_6)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b3)
(ontable b3)
(on b4 b6)
(ontable b5)
(on b6 b1)
(clear b2)
(clear b4)
)
(:goal
(and
(on b2 b1)
(on b3 b5)
(on b6 b3))
)
)


