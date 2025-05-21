

(define (problem matching-bw-typed-n2)
(:domain matching-bw-typed)
(:requirements :typing)
(:objects h1 h2 - hand b1 b2  - block)
(:init
 (empty h1)
 (empty h2)
 (hand-positive h1)
 (hand-negative h2)
 (solid b1)
 (block-positive b1)
 (on-table b1)
 (solid b2)
 (block-negative b2)
 (on-table b2)
 (clear b1)
 (clear b2)
)
(:goal
(and
 (on b1 b2))
)
)


