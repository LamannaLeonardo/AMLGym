

(define (problem bw_rand_3)
(:domain blocksworld)
(:objects b1 b2 b3 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b1)
(clear b2)
(clear b3)
)
(:goal
(and
(on b1 b2)
(on b2 b3))
)
)


