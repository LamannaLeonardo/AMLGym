

(define (problem bw_rand_12)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b2)
(on b2 b4)
(ontable b3)
(on b4 b8)
(ontable b5)
(on b6 b1)
(ontable b7)
(on b8 b11)
(on b9 b3)
(ontable b10)
(on b11 b7)
(on b12 b10)
(clear b5)
(clear b6)
(clear b9)
(clear b12)
)
(:goal
(and
(on b1 b3)
(on b3 b12)
(on b6 b4)
(on b7 b10)
(on b8 b9)
(on b9 b11)
(on b11 b1)
(on b12 b2))
)
)


