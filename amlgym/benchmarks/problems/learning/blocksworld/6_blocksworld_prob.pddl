

(define (problem bw_rand_9)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(on b2 b9)
(on b3 b1)
(ontable b4)
(on b5 b6)
(on b6 b3)
(on b7 b4)
(ontable b8)
(ontable b9)
(clear b2)
(clear b5)
(clear b7)
(clear b8)
)
(:goal
(and
(on b1 b8)
(on b3 b6)
(on b4 b3)
(on b5 b1)
(on b6 b5)
(on b7 b2)
(on b8 b7))
)
)


