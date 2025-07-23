

(define (problem bw_rand_5)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 - block)
(:init
(handempty)
(ontable b1)
(on b2 b1)
(ontable b3)
(ontable b4)
(ontable b5)
(clear b2)
(clear b3)
(clear b4)
(clear b5)
)
(:goal
(and
(on b1 b5)
(on b3 b1)
(on b5 b2))
)
)


