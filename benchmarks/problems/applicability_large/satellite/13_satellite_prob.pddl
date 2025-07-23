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
	image0 - mode
	image2 - mode
	image1 - mode
	groundstation2 - direction
	groundstation0 - direction
	star1 - direction
	planet3 - direction
	planet4 - direction
	phenomenon5 - direction
	planet6 - direction
	star7 - direction
)
(:init
	(supports instrument0 image0)
	(supports instrument0 image1)
	(calibration_target instrument0 star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon5)
	(supports instrument1 image0)
	(supports instrument1 image1)
	(supports instrument1 image2)
	(calibration_target instrument1 groundstation2)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star1)
	(supports instrument2 image0)
	(supports instrument2 image1)
	(calibration_target instrument2 groundstation0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet6)
	(supports instrument3 image1)
	(supports instrument3 image2)
	(supports instrument3 image0)
	(calibration_target instrument3 star1)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet4)
)
(:goal (and
	(pointing satellite0 groundstation2)
	(have_image planet3 image0)
	(have_image planet4 image2)
	(have_image phenomenon5 image1)
	(have_image planet6 image0)
	(have_image star7 image0)
))

)
