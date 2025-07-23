

(define (problem bw_rand_6)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b5)
(ontable b3)
(on b4 b1)
(ontable b5)
(ontable b6)
(clear b2)
(clear b4)
(clear b6)
)
(:goal
(and
(on b1 b3)
(on b3 b4)
(on b4 b6)
(on b5 b1))
)
)


