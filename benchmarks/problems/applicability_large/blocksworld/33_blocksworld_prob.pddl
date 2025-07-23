

(define (problem bw_rand_6)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b5)
(ontable b4)
(on b5 b2)
(on b6 b4)
(clear b1)
(clear b3)
(clear b6)
)
(:goal
(and
(on b3 b4)
(on b4 b5)
(on b5 b1)
(on b6 b2))
)
)


