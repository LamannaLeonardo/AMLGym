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
	infrared2 - mode
	image1 - mode
	image0 - mode
	star2 - direction
	groundstation0 - direction
	star1 - direction
	star3 - direction
	star4 - direction
	phenomenon5 - direction
	planet6 - direction
	star7 - direction
)
(:init
	(supports instrument0 infrared2)
	(supports instrument0 image0)
	(calibration_target instrument0 groundstation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation0)
	(supports instrument1 infrared2)
	(supports instrument1 image0)
	(supports instrument1 image1)
	(calibration_target instrument1 star1)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star4)
	(supports instrument2 image1)
	(calibration_target instrument2 star1)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star3)
	(supports instrument3 infrared2)
	(supports instrument3 image1)
	(supports instrument3 image0)
	(calibration_target instrument3 star1)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star3)
)
(:goal (and
	(pointing satellite2 star4)
	(pointing satellite3 star2)
	(have_image star3 image1)
	(have_image star4 infrared2)
	(have_image phenomenon5 infrared2)
	(have_image planet6 infrared2)
	(have_image star7 infrared2)
))

)
