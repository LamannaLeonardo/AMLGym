

(define (problem bw_rand_10)
(:domain blocksworld)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b6)
(on b2 b5)
(on b3 b2)
(on b4 b3)
(on b5 b9)
(on b6 b7)
(ontable b7)
(ontable b8)
(on b9 b10)
(ontable b10)
(clear b1)
(clear b4)
(clear b8)
)
(:goal
(and
(on b1 b2)
(on b2 b3)
(on b3 b8)
(on b4 b6)
(on b5 b10)
(on b6 b1)
(on b7 b5)
(on b8 b9))
)
)


