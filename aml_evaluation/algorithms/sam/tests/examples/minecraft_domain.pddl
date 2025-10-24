; PolyCraft domain

(define (domain polycraft)

(:requirements :strips :typing :negative-preconditions :fluents)

(:types
    cell - object
)

(:constants
    crafting_table - cell
)

(:predicates
    (position ?c - cell)
)

(:functions
    ; Map
    (cell_type ?c - cell) ; 0 = empty, 1 = tree, 2 = crafting table

    ; Items
    (count_log_in_inventory)
    (count_planks_in_inventory)
    (count_stick_in_inventory)
    (count_sack_polyisoprene_pellets_in_inventory)
    (count_tree_tap_in_inventory)
    (count_wooden_pogo_stick_in_inventory)
)

; Actions
(:action tp_to
    :parameters (?from - cell ?to - cell)
    :precondition (and
        (position ?from)
    )
    :effect (and
        (not (position ?from))
        (position ?to)
    )
)

(:action break
    :parameters (?pos - cell)
    :precondition (and
        (position ?pos)
        (= (cell_type ?pos) 1)
    )
    :effect (and
        (assign (cell_type ?pos) 0)
        (increase (count_log_in_inventory) 1)
    )
)

(:action craft_plank
    :parameters ()
    :precondition (and
        (> (count_log_in_inventory) 0)
    )
    :effect (and
        (decrease (count_log_in_inventory) 1)
        (increase (count_planks_in_inventory) 4)
    )
)

(:action craft_stick
    :parameters ()
    :precondition (and
        (> (count_planks_in_inventory) 1)
    )
    :effect (and
        (decrease (count_planks_in_inventory) 2)
        (increase (count_stick_in_inventory) 4)
    )
)

(:action craft_tree_tap
    :parameters (?pos - cell)
    :precondition (and
        (position ?pos)
        (> (count_planks_in_inventory) 4)
        (> (count_stick_in_inventory) 0)
    )
    :effect (and
        (not (position ?pos))
        (position crafting_table)
        (decrease (count_planks_in_inventory) 5)
        (decrease (count_stick_in_inventory) 1)
        (increase (count_tree_tap_in_inventory) 1)
    )
)

(:action craft_wooden_pogo
    :parameters (?pos - cell)
    :precondition (and
        (position ?pos)
        (> (count_planks_in_inventory) 1)
        (> (count_stick_in_inventory) 3)
        (> (count_sack_polyisoprene_pellets_in_inventory) 0)
    )
    :effect (and
        (not (position ?pos))
        (position crafting_table)
        (decrease (count_planks_in_inventory) 2)
        (decrease (count_stick_in_inventory) 4)
        (decrease (count_sack_polyisoprene_pellets_in_inventory) 1)
        (increase (count_wooden_pogo_stick_in_inventory) 1)
    )
)

(:action place_tree_tap
    :parameters (?pos - cell)
    :precondition (and
        (position ?pos)
        (= (cell_type ?pos) 1)
        (> (count_tree_tap_in_inventory) 0)
    )
    :effect (and
        (increase (count_sack_polyisoprene_pellets_in_inventory) 1)
    )
)

)