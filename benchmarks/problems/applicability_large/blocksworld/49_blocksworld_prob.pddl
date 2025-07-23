

(define (problem bw_rand_12)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(ontable b1)
(on b2 b8)
(ontable b3)
(on b4 b12)
(on b5 b2)
(ontable b6)
(on b7 b6)
(ontable b8)
(on b9 b3)
(ontable b10)
(on b11 b4)
(on b12 b10)
(clear b1)
(clear b5)
(clear b7)
(clear b9)
(clear b11)
)
(:goal
(and
(on b1 b12)
(on b2 b8)
(on b3 b1)
(on b4 b5)
(on b5 b7)
(on b7 b9)
(on b10 b3)
(on b11 b4))
)
)


