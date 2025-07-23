

(define (problem bw_rand_12)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(on b1 b9)
(on b2 b4)
(on b3 b5)
(ontable b4)
(on b5 b2)
(on b6 b12)
(on b7 b11)
(ontable b8)
(ontable b9)
(on b10 b1)
(on b11 b3)
(on b12 b8)
(clear b6)
(clear b7)
(clear b10)
)
(:goal
(and
(on b1 b2)
(on b2 b3)
(on b3 b6)
(on b4 b12)
(on b5 b9)
(on b6 b7)
(on b8 b11)
(on b10 b1)
(on b11 b10)
(on b12 b5))
)
)


