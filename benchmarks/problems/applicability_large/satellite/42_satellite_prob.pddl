(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	satellite2 - satellite
	instrument2 - instrument
	satellite3 - satellite
	instrument3 - instrument
	infrared1 - mode
	infrared0 - mode
	groundstation1 - direction
	star0 - direction
	star2 - direction
	planet3 - direction
	star4 - direction
	phenomenon5 - direction
	planet6 - direction
	star7 - direction
)
(:init
	(supports instrument0 infrared1)
	(supports instrument0 infrared0)
	(calibration_target instrument0 star2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star2)
	(supports instrument1 infrared1)
	(calibration_target instrument1 groundstation1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet6)
	(supports instrument2 infrared0)
	(calibration_target instrument2 star0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon5)
	(supports instrument3 infrared1)
	(supports instrument3 infrared0)
	(calibration_target instrument3 star2)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star7)
)
(:goal (and
	(pointing satellite2 star2)
	(have_image planet3 infrared0)
	(have_image star4 infrared1)
	(have_image phenomenon5 infrared1)
	(have_image planet6 infrared1)
	(have_image star7 infrared1)
))

)
