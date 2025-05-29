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
	spectrograph0 - mode
	star1 - direction
	star0 - direction
	groundstation2 - direction
	planet3 - direction
	planet4 - direction
	phenomenon5 - direction
	planet6 - direction
	planet7 - direction
)
(:init
	(supports instrument0 image1)
	(calibration_target instrument0 star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation2)
	(supports instrument1 image1)
	(supports instrument1 spectrograph0)
	(calibration_target instrument1 star0)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star1)
	(supports instrument2 spectrograph0)
	(calibration_target instrument2 groundstation2)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet6)
	(supports instrument3 spectrograph0)
	(calibration_target instrument3 groundstation2)
	(on_board instrument3 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet6)
)
(:goal (and
	(pointing satellite0 planet6)
	(have_image planet3 image1)
	(have_image planet4 spectrograph0)
	(have_image phenomenon5 image1)
	(have_image planet6 image1)
	(have_image planet7 spectrograph0)
))

)
