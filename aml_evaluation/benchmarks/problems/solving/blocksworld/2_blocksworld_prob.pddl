

(define (problem bw_rand_5)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b2)
(ontable b4)
(on b5 b4)
(clear b1)
(clear b3)
(clear b5)
)
(:goal
(and
(on b1 b3)
(on b2 b1)
(on b3 b4))
)
)


