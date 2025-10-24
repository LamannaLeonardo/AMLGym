

(define (problem bw_rand_4)
(:domain blocksworld)
(:objects b1 b2 b3 b4 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(ontable b3)
(on b4 b2)
(clear b1)
(clear b3)
)
(:goal
(and
(on b1 b2)
(on b2 b4))
)
)


