

(define (problem bw_rand_6)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(ontable b1)
(on b2 b4)
(ontable b3)
(on b4 b1)
(on b5 b3)
(ontable b6)
(clear b2)
(clear b5)
(clear b6)
)
(:goal
(and
(on b2 b3)
(on b3 b5)
(on b5 b1)
(on b6 b4))
)
)


