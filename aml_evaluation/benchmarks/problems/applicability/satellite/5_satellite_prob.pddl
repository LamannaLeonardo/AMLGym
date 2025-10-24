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
	image1 - mode
	infrared0 - mode
	groundstation0 - direction
	groundstation1 - direction
	groundstation2 - direction
	star3 - direction
	star4 - direction
	planet5 - direction
	planet6 - direction
	phenomenon7 - direction
)
(:init
	(supports instrument0 image1)
	(supports instrument0 infrared0)
	(calibration_target instrument0 groundstation2)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon7)
	(supports instrument1 image1)
	(supports instrument1 infrared0)
	(calibration_target instrument1 groundstation2)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation0)
	(supports instrument2 infrared0)
	(supports instrument2 image1)
	(calibration_target instrument2 groundstation1)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet6)
	(supports instrument3 infrared0)
	(supports instrument3 image1)
	(calibration_target instrument3 groundstation2)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star4)
)
(:goal (and
	(pointing satellite0 star4)
	(have_image star3 image1)
	(have_image star4 infrared0)
	(have_image planet5 infrared0)
	(have_image planet6 infrared0)
	(have_image phenomenon7 image1)
))

)
