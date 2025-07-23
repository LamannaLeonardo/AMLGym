

(define (problem bw_rand_11)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b11)
(on b2 b4)
(on b3 b5)
(on b4 b8)
(ontable b5)
(ontable b6)
(on b7 b9)
(on b8 b7)
(ontable b9)
(on b10 b1)
(on b11 b2)
(clear b3)
(clear b6)
(clear b10)
)
(:goal
(and
(on b1 b10)
(on b3 b8)
(on b4 b9)
(on b6 b7)
(on b7 b3)
(on b8 b2)
(on b9 b1)
(on b10 b11)
(on b11 b6))
)
)


