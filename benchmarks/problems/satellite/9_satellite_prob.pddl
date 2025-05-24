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
	satellite5 - satellite
	instrument6 - instrument
	instrument7 - instrument
	satellite6 - satellite
	instrument8 - instrument
	instrument9 - instrument
	instrument10 - instrument
	spectrograph2 - mode
	image4 - mode
	thermograph0 - mode
	infrared5 - mode
	image1 - mode
	spectrograph3 - mode
	star0 - direction
	star2 - direction
	star3 - direction
	star5 - direction
	groundstation4 - direction
	groundstation1 - direction
	planet6 - direction
	planet7 - direction
	phenomenon8 - direction
	phenomenon9 - direction
	planet10 - direction
	star11 - direction
	phenomenon12 - direction
	star13 - direction
)
(:init
	(supports instrument0 spectrograph2)
	(calibration_target instrument0 star3)
	(calibration_target instrument0 groundstation1)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation1)
	(supports instrument1 thermograph0)
	(supports instrument1 image1)
	(supports instrument1 infrared5)
	(calibration_target instrument1 star0)
	(calibration_target instrument1 star5)
	(on_board instrument1 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star3)
	(supports instrument2 spectrograph3)
	(calibration_target instrument2 star0)
	(on_board instrument2 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon12)
	(supports instrument3 infrared5)
	(calibration_target instrument3 star2)
	(calibration_target instrument3 groundstation1)
	(supports instrument4 infrared5)
	(supports instrument4 spectrograph3)
	(supports instrument4 image1)
	(calibration_target instrument4 star0)
	(calibration_target instrument4 star3)
	(on_board instrument3 satellite3)
	(on_board instrument4 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star13)
	(supports instrument5 spectrograph3)
	(supports instrument5 image4)
	(calibration_target instrument5 star2)
	(on_board instrument5 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star2)
	(supports instrument6 infrared5)
	(calibration_target instrument6 groundstation4)
	(supports instrument7 infrared5)
	(supports instrument7 spectrograph2)
	(supports instrument7 image1)
	(calibration_target instrument7 groundstation4)
	(calibration_target instrument7 star3)
	(on_board instrument6 satellite5)
	(on_board instrument7 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star13)
	(supports instrument8 infrared5)
	(supports instrument8 image1)
	(supports instrument8 spectrograph3)
	(calibration_target instrument8 star3)
	(calibration_target instrument8 groundstation4)
	(supports instrument9 spectrograph3)
	(supports instrument9 spectrograph2)
	(calibration_target instrument9 groundstation4)
	(calibration_target instrument9 star5)
	(supports instrument10 thermograph0)
	(calibration_target instrument10 groundstation1)
	(on_board instrument8 satellite6)
	(on_board instrument9 satellite6)
	(on_board instrument10 satellite6)
	(power_avail satellite6)
	(pointing satellite6 planet6)
)
(:goal (and
	(have_image planet6 image4)
	(have_image planet6 spectrograph3)
	(have_image planet7 spectrograph3)
	(have_image phenomenon8 image1)
	(have_image phenomenon8 thermograph0)
	(have_image phenomenon9 image1)
	(have_image planet10 thermograph0)
	(have_image planet10 infrared5)
	(have_image star11 spectrograph2)
	(have_image star11 thermograph0)
	(have_image phenomenon12 thermograph0)
	(have_image phenomenon12 image4)
	(have_image star13 spectrograph2)
))

)
