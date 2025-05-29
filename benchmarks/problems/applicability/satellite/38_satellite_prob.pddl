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
	groundstation2 - direction
	groundstation0 - direction
	star1 - direction
	planet3 - direction
	phenomenon4 - direction
	phenomenon5 - direction
	phenomenon6 - direction
	planet7 - direction
)
(:init
	(supports instrument0 infrared1)
	(calibration_target instrument0 star1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon5)
	(supports instrument1 infrared1)
	(supports instrument1 infrared0)
	(calibration_target instrument1 groundstation0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon5)
	(supports instrument2 infrared1)
	(calibration_target instrument2 groundstation0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet3)
	(supports instrument3 infrared1)
	(supports instrument3 infrared0)
	(calibration_target instrument3 star1)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon6)
)
(:goal (and
	(pointing satellite3 planet7)
	(have_image planet3 infrared1)
	(have_image phenomenon4 infrared0)
	(have_image phenomenon5 infrared0)
	(have_image phenomenon6 infrared0)
	(have_image planet7 infrared0)
))

)
