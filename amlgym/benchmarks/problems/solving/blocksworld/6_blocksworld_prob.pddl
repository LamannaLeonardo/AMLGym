

(define (problem bw_rand_9)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b3)
(ontable b2)
(on b3 b9)
(ontable b4)
(on b5 b4)
(ontable b6)
(on b7 b2)
(on b8 b1)
(on b9 b5)
(clear b6)
(clear b7)
(clear b8)
)
(:goal
(and
(on b1 b2)
(on b2 b4)
(on b3 b8)
(on b5 b7)
(on b6 b5)
(on b7 b9)
(on b8 b6)
(on b9 b1))
)
)


