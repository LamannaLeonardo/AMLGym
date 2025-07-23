

(define (problem bw_rand_11)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b4)
(on b2 b11)
(on b3 b10)
(on b4 b3)
(on b5 b8)
(ontable b6)
(on b7 b2)
(on b8 b7)
(ontable b9)
(on b10 b6)
(on b11 b1)
(clear b5)
(clear b9)
)
(:goal
(and
(on b1 b4)
(on b2 b7)
(on b4 b9)
(on b5 b3)
(on b6 b11)
(on b10 b6)
(on b11 b2))
)
)


