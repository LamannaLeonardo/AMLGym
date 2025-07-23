

(define (problem bw_rand_9)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(ontable b1)
(on b2 b8)
(on b3 b1)
(on b4 b3)
(ontable b5)
(on b6 b9)
(on b7 b6)
(on b8 b5)
(on b9 b2)
(clear b4)
(clear b7)
)
(:goal
(and
(on b1 b6)
(on b2 b5)
(on b5 b8)
(on b6 b4)
(on b7 b3)
(on b8 b7)
(on b9 b1))
)
)


