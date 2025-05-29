

(define (problem matching_bw_typed_n3)
(:domain matching_bw_typed)
(:requirements :typing)
(:objects h1 h2 - hand b1 b2 b3  - block)
(:init
 (empty h1)
 (empty h2)
 (hand_positive h1)
 (hand_negative h2)
 (solid b1)
 (block_positive b1)
 (on b1 b2)
 (solid b2)
 (block_negative b2)
 (on b2 b3)
 (solid b3)
 (block_negative b3)
 (on_table b3)
 (clear b1)
)
(:goal
(and
 (on b1 b3))
)
)


