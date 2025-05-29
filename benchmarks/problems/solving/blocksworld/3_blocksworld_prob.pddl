

(define (problem bw_rand_6)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b5)
(on b3 b2)
(ontable b4)
(on b5 b1)
(ontable b6)
(clear b3)
(clear b6)
)
(:goal
(and
(on b1 b3)
(on b3 b4)
(on b5 b6)
(on b6 b2))
)
)


