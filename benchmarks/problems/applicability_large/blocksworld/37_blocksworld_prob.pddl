

(define (problem bw_rand_10)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(ontable b1)
(on b2 b4)
(on b3 b7)
(on b4 b10)
(on b5 b1)
(on b6 b3)
(on b7 b5)
(ontable b8)
(ontable b9)
(on b10 b6)
(clear b2)
(clear b8)
(clear b9)
)
(:goal
(and
(on b2 b10)
(on b3 b8)
(on b4 b2)
(on b7 b6)
(on b8 b7)
(on b9 b1)
(on b10 b3))
)
)


