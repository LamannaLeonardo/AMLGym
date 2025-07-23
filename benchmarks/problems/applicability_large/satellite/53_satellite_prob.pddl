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
	image0 - mode
	spectrograph2 - mode
	groundstation0 - direction
	star2 - direction
	groundstation1 - direction
	star3 - direction
	planet4 - direction
	planet5 - direction
	star6 - direction
	star7 - direction
)
(:init
	(supports instrument0 spectrograph2)
	(supports instrument0 infrared1)
	(calibration_target instrument0 groundstation1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star7)
	(supports instrument1 spectrograph2)
	(calibration_target instrument1 groundstation0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation0)
	(supports instrument2 infrared1)
	(supports instrument2 image0)
	(calibration_target instrument2 star2)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation0)
	(supports instrument3 spectrograph2)
	(supports instrument3 image0)
	(supports instrument3 infrared1)
	(calibration_target instrument3 groundstation1)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet4)
)
(:goal (and
	(have_image star3 infrared1)
	(have_image planet4 infrared1)
	(have_image planet5 spectrograph2)
	(have_image star6 infrared1)
	(have_image star7 image0)
))

)
