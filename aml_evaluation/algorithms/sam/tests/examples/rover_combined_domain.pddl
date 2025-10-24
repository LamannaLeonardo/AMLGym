(define (domain rover)
(:requirements :typing)
(:types 	rover waypoint store camera mode lander objective - object
)

(:predicates (at ?x - rover ?y - waypoint)
	(at_lander ?x - lander ?y - waypoint)
	(can_traverse ?r - rover ?x - waypoint ?y - waypoint)
	(equipped_for_soil_analysis ?r - rover)
	(equipped_for_rock_analysis ?r - rover)
	(equipped_for_imaging ?r - rover)
	(empty ?s - store)
	(have_rock_analysis ?r - rover ?w - waypoint)
	(have_soil_analysis ?r - rover ?w - waypoint)
	(full ?s - store)
	(calibrated ?c - camera ?r - rover)
	(supports ?c - camera ?m - mode)
	(available ?r - rover)
	(visible ?w - waypoint ?p - waypoint)
	(have_image ?r - rover ?o - objective ?m - mode)
	(communicated_soil_data ?w - waypoint)
	(communicated_rock_data ?w - waypoint)
	(communicated_image_data ?o - objective ?m - mode)
	(at_soil_sample ?w - waypoint)
	(at_rock_sample ?w - waypoint)
	(visible_from ?o - objective ?w - waypoint)
	(store_of ?s - store ?r - rover)
	(calibration_target ?i - camera ?o - objective)
	(on_board ?i - camera ?r - rover)
	(channel_free ?l - lander)
)

(:action navigate
	:parameters   (?x - rover ?y - waypoint ?z - waypoint)
	:precondition (and (visible ?y ?z) (at ?x ?y) (available ?x) (can_traverse ?x ?y ?z))
	:effect       (and (at ?x ?z) (not (at ?x ?y))
))

(:action sample_soil
	:parameters   (?x - rover ?s - store ?p - waypoint)
	:precondition (and (store_of ?s ?x) (empty ?s) (at ?x ?p) (equipped_for_soil_analysis ?x) (at_soil_sample ?p))
	:effect       (and (full ?s) (have_soil_analysis ?x ?p) (not (empty ?s)) (not (at_soil_sample ?p))
))

(:action sample_rock
	:parameters   (?x - rover ?s - store ?p - waypoint)
	:precondition (and (store_of ?s ?x) (empty ?s) (at ?x ?p) (at_rock_sample ?p) (equipped_for_rock_analysis ?x))
	:effect       (and (full ?s) (have_rock_analysis ?x ?p) (not (empty ?s)) (not (at_rock_sample ?p))
))

(:action drop
	:parameters   (?x - rover ?y - store)
	:precondition (and (full ?y) (store_of ?y ?x))
	:effect       (and (empty ?y) (not (full ?y))
))

(:action calibrate
	:parameters   (?r - rover ?i - camera ?t - objective ?w - waypoint)
	:precondition (and (at ?r ?w) (calibration_target ?i ?t) (equipped_for_imaging ?r) (on_board ?i ?r) (visible_from ?t ?w))
	:effect       (and (calibrated ?i ?r)
))

(:action take_image
	:parameters   (?r - rover ?p - waypoint ?o - objective ?i - camera ?m - mode)
	:precondition (and (calibrated ?i ?r) (supports ?i ?m) (at ?r ?p) (visible_from ?o ?p) (equipped_for_imaging ?r) (on_board ?i ?r))
	:effect       (and (have_image ?r ?o ?m) (not (calibrated ?i ?r))
))

(:action communicate_soil_data
	:parameters   (?r - rover ?l - lander ?p - waypoint ?x - waypoint ?y - waypoint)
	:precondition (and (at ?r ?x) (have_soil_analysis ?r ?p) (at_lander ?l ?y) (channel_free ?l) (visible ?x ?y) (available ?r))
	:effect       (and (communicated_soil_data ?p)
))

(:action communicate_rock_data
	:parameters   (?r - rover ?l - lander ?p - waypoint ?x - waypoint ?y - waypoint)
	:precondition (and (at ?r ?x) (at_lander ?l ?y) (channel_free ?l) (visible ?x ?y) (available ?r) (have_rock_analysis ?r ?p))
	:effect       (and (communicated_rock_data ?p)
))

(:action communicate_image_data
	:parameters   (?r - rover ?l - lander ?o - objective ?m - mode ?x - waypoint ?y - waypoint)
	:precondition (and (at ?r ?x) (have_image ?r ?o ?m) (at_lander ?l ?y) (channel_free ?l) (visible ?x ?y) (available ?r))
	:effect       (and (communicated_image_data ?o ?m)
))

)