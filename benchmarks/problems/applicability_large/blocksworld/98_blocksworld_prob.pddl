

(define (problem bw_rand_11)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(ontable b1)
(on b2 b3)
(on b3 b10)
(on b4 b5)
(on b5 b7)
(on b6 b1)
(ontable b7)
(ontable b8)
(on b9 b8)
(on b10 b4)
(on b11 b6)
(clear b2)
(clear b9)
(clear b11)
)
(:goal
(and
(on b1 b8)
(on b4 b5)
(on b8 b11)
(on b10 b9)
(on b11 b3))
)
)


