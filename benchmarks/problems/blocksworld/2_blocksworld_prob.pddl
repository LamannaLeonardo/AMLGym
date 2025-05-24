

(define (problem bw_rand_4)
(:domain blocksworld_4ops)
(:objects b1 b2 b3 b4 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b1)
(ontable b4)
(clear b2)
(clear b3)
(clear b4)
)
(:goal
(and
(on b2 b4)
(on b4 b3))
)
)


