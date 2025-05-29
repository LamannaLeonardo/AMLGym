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
	image1 - mode
	groundstation0 - direction
	groundstation1 - direction
	groundstation2 - direction
	phenomenon3 - direction
	phenomenon4 - direction
	planet5 - direction
	phenomenon6 - direction
	phenomenon7 - direction
)
(:init
	(supports instrument0 image0)
	(supports instrument0 image1)
	(calibration_target instrument0 groundstation1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon4)
	(supports instrument1 image1)
	(supports instrument1 image0)
	(calibration_target instrument1 groundstation2)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation0)
	(supports instrument2 image1)
	(calibration_target instrument2 groundstation1)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet5)
	(supports instrument3 image0)
	(supports instrument3 image1)
	(calibration_target instrument3 groundstation2)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon3)
)
(:goal (and
	(pointing satellite0 groundstation0)
	(pointing satellite1 groundstation1)
	(pointing satellite2 groundstation0)
	(have_image phenomenon3 image0)
	(have_image phenomenon4 image1)
	(have_image planet5 image1)
	(have_image phenomenon6 image0)
	(have_image phenomenon7 image0)
))

)
