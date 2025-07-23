

(define (problem bw_rand_10)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b3)
(ontable b2)
(on b3 b9)
(ontable b4)
(on b5 b1)
(on b6 b5)
(ontable b7)
(on b8 b6)
(on b9 b10)
(on b10 b4)
(clear b2)
(clear b7)
(clear b8)
)
(:goal
(and
(on b2 b8)
(on b4 b10)
(on b5 b6)
(on b6 b7)
(on b7 b1)
(on b8 b3)
(on b9 b2))
)
)


