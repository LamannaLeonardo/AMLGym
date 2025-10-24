

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
 (on_table b1)
 (solid b2)
 (block_negative b2)
 (on_table b2)
 (solid b3)
 (block_negative b3)
 (on b3 b1)
 (clear b2)
 (clear b3)
)
(:goal
(and
 (on b1 b3))
)
)


