

(define (problem bw_rand_3)
(:domain blocksworld)
(:objects b1 b2 b3 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b3)
(ontable b3)
(clear b1)
)
(:goal
(and
(on b3 b2))
)
)


