

(define (problem bw_rand_11)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b11)
(on b3 b1)
(ontable b4)
(on b5 b9)
(on b6 b8)
(on b7 b2)
(ontable b8)
(on b9 b3)
(ontable b10)
(ontable b11)
(clear b4)
(clear b5)
(clear b7)
(clear b10)
)
(:goal
(and
(on b1 b3)
(on b3 b2)
(on b4 b7)
(on b5 b6)
(on b6 b10)
(on b8 b1)
(on b9 b4)
(on b10 b9)
(on b11 b8))
)
)


