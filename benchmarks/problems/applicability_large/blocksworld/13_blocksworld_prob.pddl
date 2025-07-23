

(define (problem bw_rand_6)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b4)
(ontable b2)
(on b3 b6)
(ontable b4)
(ontable b5)
(ontable b6)
(clear b1)
(clear b2)
(clear b3)
(clear b5)
)
(:goal
(and
(on b1 b5)
(on b5 b4)
(on b6 b1))
)
)


