

(define (problem bw_rand_6)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(ontable b1)
(on b2 b5)
(ontable b3)
(ontable b4)
(ontable b5)
(on b6 b4)
(clear b1)
(clear b2)
(clear b3)
(clear b6)
)
(:goal
(and
(on b2 b3)
(on b3 b4)
(on b4 b1)
(on b5 b6)
(on b6 b2))
)
)


