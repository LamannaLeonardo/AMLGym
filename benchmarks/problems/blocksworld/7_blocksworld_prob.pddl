

(define (problem bw_rand_6)
(:domain blocksworld_4ops)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b5)
(on b2 b3)
(ontable b3)
(on b4 b6)
(on b5 b4)
(on b6 b2)
(clear b1)
)
(:goal
(and
(on b1 b5)
(on b3 b1)
(on b4 b2)
(on b5 b6))
)
)


