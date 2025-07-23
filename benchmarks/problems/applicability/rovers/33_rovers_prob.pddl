(define (problem roverprob319) (:domain rover)
(:objects
	general - lander
	colour high_res low_res - mode
	rover0 - rover
	rover0store - store
	waypoint0 waypoint1 waypoint2 - waypoint
	camera0 - camera
	objective0 - objective
	)
(:init
	(visible waypoint0 waypoint1)
	(visible waypoint1 waypoint0)
	(visible waypoint1 waypoint2)
	(visible waypoint2 waypoint1)
	(visible waypoint2 waypoint0)
	(visible waypoint0 waypoint2)
	(at_soil_sample waypoint0)
	(at_rock_sample waypoint0)
	(at_rock_sample waypoint1)
	(at_soil_sample waypoint2)
	(at_rock_sample waypoint2)
	(at_lander general waypoint2)
	(channel_free general)
	(at rover0 waypoint0)
	(available rover0)
	(store_of rover0store rover0)
	(empty rover0store)
	(equipped_for_soil_analysis rover0)
	(equipped_for_imaging rover0)
	(can_traverse rover0 waypoint0 waypoint1)
	(can_traverse rover0 waypoint1 waypoint0)
	(can_traverse rover0 waypoint0 waypoint2)
	(can_traverse rover0 waypoint2 waypoint0)
	(on_board camera0 rover0)
	(calibration_target camera0 objective0)
	(supports camera0 low_res)
	(visible_from objective0 waypoint1)
	(visible_from objective0 waypoint2)
)

(:goal (and
(communicated_soil_data waypoint2)
(communicated_soil_data waypoint0)
(communicated_image_data objective0 low_res)
	)
)
)
