

(define (problem bw_rand_11)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b8)
(on b2 b9)
(on b3 b11)
(ontable b4)
(on b5 b6)
(on b6 b3)
(on b7 b4)
(on b8 b7)
(ontable b9)
(on b10 b1)
(ontable b11)
(clear b2)
(clear b5)
(clear b10)
)
(:goal
(and
(on b2 b10)
(on b4 b6)
(on b5 b3)
(on b6 b8)
(on b7 b11)
(on b8 b9)
(on b9 b5)
(on b10 b1)
(on b11 b4))
)
)


