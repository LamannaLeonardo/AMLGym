(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	infrared1 - mode
	infrared0 - mode
	groundstation1 - direction
	groundstation0 - direction
	star2 - direction
	star3 - direction
	phenomenon4 - direction
	star5 - direction
)
(:init
	(supports instrument0 infrared1)
	(supports instrument0 infrared0)
	(calibration_target instrument0 groundstation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star5)
	(supports instrument1 infrared1)
	(supports instrument1 infrared0)
	(calibration_target instrument1 groundstation1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star3)
	(supports instrument2 infrared0)
	(supports instrument2 infrared1)
	(calibration_target instrument2 groundstation0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation0)
)
(:goal (and
	(pointing satellite1 star2)
	(have_image star2 infrared0)
	(have_image star3 infrared1)
	(have_image phenomenon4 infrared0)
	(have_image star5 infrared1)
))

)
