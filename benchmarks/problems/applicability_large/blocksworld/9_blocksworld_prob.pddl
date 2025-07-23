

(define (problem bw_rand_12)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b10)
(on b2 b5)
(ontable b3)
(on b4 b12)
(on b5 b3)
(on b6 b11)
(on b7 b8)
(ontable b8)
(ontable b9)
(on b10 b9)
(on b11 b2)
(on b12 b1)
(clear b4)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b6)
(on b2 b12)
(on b3 b7)
(on b4 b3)
(on b6 b10)
(on b7 b9)
(on b8 b5)
(on b10 b8)
(on b12 b11))
)
)


