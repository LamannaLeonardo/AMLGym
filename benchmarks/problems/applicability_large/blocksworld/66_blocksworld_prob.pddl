

(define (problem bw_rand_9)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b5)
(ontable b3)
(ontable b4)
(on b5 b9)
(on b6 b3)
(on b7 b1)
(on b8 b7)
(ontable b9)
(clear b2)
(clear b4)
(clear b8)
)
(:goal
(and
(on b3 b4)
(on b4 b6)
(on b5 b3)
(on b6 b8)
(on b8 b7)
(on b9 b1))
)
)


