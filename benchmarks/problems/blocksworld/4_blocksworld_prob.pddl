

(define (problem bw_rand_5)
(:domain blocksworld_4ops)
(:objects b1 b2 b3 b4 b5 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b3)
(ontable b3)
(ontable b4)
(ontable b5)
(clear b1)
(clear b2)
(clear b4)
)
(:goal
(and
(on b2 b1)
(on b3 b5)
(on b4 b2)
(on b5 b4))
)
)


