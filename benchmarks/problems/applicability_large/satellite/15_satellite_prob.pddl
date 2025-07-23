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
	instrument4 - instrument
	satellite4 - satellite
	instrument5 - instrument
	spectrograph3 - mode
	thermograph2 - mode
	image1 - mode
	infrared0 - mode
	star1 - direction
	star2 - direction
	groundstation0 - direction
	star3 - direction
	phenomenon4 - direction
	star5 - direction
	star6 - direction
	star7 - direction
	star8 - direction
	star9 - direction
)
(:init
	(supports instrument0 thermograph2)
	(supports instrument0 image1)
	(calibration_target instrument0 star3)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star6)
	(supports instrument1 image1)
	(supports instrument1 spectrograph3)
	(supports instrument1 infrared0)
	(calibration_target instrument1 star2)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star2)
	(supports instrument2 infrared0)
	(supports instrument2 spectrograph3)
	(calibration_target instrument2 star2)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star3)
	(supports instrument3 thermograph2)
	(supports instrument3 spectrograph3)
	(calibration_target instrument3 groundstation0)
	(supports instrument4 infrared0)
	(supports instrument4 image1)
	(calibration_target instrument4 star3)
	(on_board instrument3 satellite3)
	(on_board instrument4 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation0)
	(supports instrument5 spectrograph3)
	(supports instrument5 infrared0)
	(calibration_target instrument5 star3)
	(on_board instrument5 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star6)
)
(:goal (and
	(pointing satellite1 star3)
	(pointing satellite2 star3)
	(pointing satellite4 star3)
	(have_image phenomenon4 thermograph2)
	(have_image star5 spectrograph3)
	(have_image star6 image1)
	(have_image star7 image1)
	(have_image star8 infrared0)
	(have_image star9 infrared0)
))

)
