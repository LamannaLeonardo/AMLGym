

(define (problem bw_rand_9)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b3)
(ontable b2)
(ontable b3)
(on b4 b9)
(on b5 b4)
(on b6 b7)
(on b7 b5)
(on b8 b1)
(ontable b9)
(clear b2)
(clear b6)
(clear b8)
)
(:goal
(and
(on b1 b6)
(on b2 b7)
(on b4 b2)
(on b5 b1)
(on b7 b9)
(on b8 b4))
)
)


