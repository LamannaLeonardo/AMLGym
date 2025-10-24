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
	star1 - direction
	star2 - direction
	star0 - direction
	star3 - direction
	planet4 - direction
	star5 - direction
	planet6 - direction
	star7 - direction
)
(:init
	(supports instrument0 infrared1)
	(calibration_target instrument0 star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star5)
	(supports instrument1 infrared1)
	(calibration_target instrument1 star2)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star7)
	(supports instrument2 infrared0)
	(supports instrument2 infrared1)
	(calibration_target instrument2 star2)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star3)
	(supports instrument3 infrared1)
	(supports instrument3 infrared0)
	(calibration_target instrument3 star0)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star2)
)
(:goal (and
	(pointing satellite2 planet6)
	(pointing satellite3 star0)
	(have_image star3 infrared1)
	(have_image planet4 infrared0)
	(have_image star5 infrared0)
	(have_image planet6 infrared1)
	(have_image star7 infrared1)
))

)
