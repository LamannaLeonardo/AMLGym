

(define (problem bw_rand_10)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b6)
(ontable b2)
(on b3 b9)
(on b4 b1)
(on b5 b3)
(ontable b6)
(on b7 b2)
(ontable b8)
(on b9 b8)
(on b10 b7)
(clear b4)
(clear b5)
(clear b10)
)
(:goal
(and
(on b1 b10)
(on b2 b4)
(on b3 b9)
(on b4 b3)
(on b5 b1)
(on b7 b2)
(on b9 b5)
(on b10 b8))
)
)


