

(define (problem bw_rand_4)
(:domain blocksworld)
(:objects b1 b2 b3 b4 - block)
(:init
(handempty)
(on b1 b2)
(ontable b2)
(ontable b3)
(ontable b4)
(clear b1)
(clear b3)
(clear b4)
)
(:goal
(and
(on b1 b2)
(on b3 b4))
)
)


