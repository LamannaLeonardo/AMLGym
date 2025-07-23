(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	instrument2 - instrument
	satellite2 - satellite
	instrument3 - instrument
	satellite3 - satellite
	instrument4 - instrument
	instrument5 - instrument
	satellite4 - satellite
	instrument6 - instrument
	instrument7 - instrument
	satellite5 - satellite
	instrument8 - instrument
	instrument9 - instrument
	satellite6 - satellite
	instrument10 - instrument
	spectrograph3 - mode
	infrared5 - mode
	thermograph4 - mode
	spectrograph0 - mode
	thermograph2 - mode
	image1 - mode
	star1 - direction
	star5 - direction
	star2 - direction
	groundstation4 - direction
	groundstation0 - direction
	star3 - direction
	planet6 - direction
	star7 - direction
	star8 - direction
	planet9 - direction
	phenomenon10 - direction
	star11 - direction
	phenomenon12 - direction
	star13 - direction
)
(:init
	(supports instrument0 thermograph4)
	(supports instrument0 thermograph2)
	(calibration_target instrument0 star5)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star5)
	(supports instrument1 spectrograph3)
	(supports instrument1 thermograph2)
	(calibration_target instrument1 star2)
	(calibration_target instrument1 star5)
	(supports instrument2 spectrograph0)
	(calibration_target instrument2 star1)
	(calibration_target instrument2 star3)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet6)
	(supports instrument3 spectrograph0)
	(supports instrument3 spectrograph3)
	(supports instrument3 thermograph4)
	(calibration_target instrument3 star5)
	(calibration_target instrument3 groundstation4)
	(on_board instrument3 satellite2)
	(power_avail satellite2)
	(pointing satellite2 phenomenon12)
	(supports instrument4 spectrograph0)
	(supports instrument4 spectrograph3)
	(calibration_target instrument4 star2)
	(calibration_target instrument4 groundstation0)
	(supports instrument5 spectrograph0)
	(supports instrument5 image1)
	(supports instrument5 infrared5)
	(calibration_target instrument5 star3)
	(calibration_target instrument5 groundstation4)
	(on_board instrument4 satellite3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet9)
	(supports instrument6 thermograph4)
	(calibration_target instrument6 star3)
	(supports instrument7 infrared5)
	(supports instrument7 spectrograph0)
	(supports instrument7 image1)
	(calibration_target instrument7 star2)
	(on_board instrument6 satellite4)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star5)
	(supports instrument8 spectrograph0)
	(supports instrument8 image1)
	(calibration_target instrument8 star3)
	(calibration_target instrument8 star2)
	(supports instrument9 image1)
	(calibration_target instrument9 groundstation4)
	(on_board instrument8 satellite5)
	(on_board instrument9 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star11)
	(supports instrument10 image1)
	(calibration_target instrument10 star3)
	(calibration_target instrument10 groundstation0)
	(on_board instrument10 satellite6)
	(power_avail satellite6)
	(pointing satellite6 star3)
)
(:goal (and
	(have_image planet6 spectrograph0)
	(have_image planet6 infrared5)
	(have_image star7 infrared5)
	(have_image star8 infrared5)
	(have_image star8 thermograph4)
	(have_image planet9 spectrograph3)
	(have_image planet9 image1)
	(have_image phenomenon10 image1)
	(have_image phenomenon10 infrared5)
	(have_image star11 image1)
	(have_image star11 thermograph2)
	(have_image phenomenon12 spectrograph3)
	(have_image star13 spectrograph0)
))

)
