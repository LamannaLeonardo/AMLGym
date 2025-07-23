(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	instrument2 - instrument
	satellite1 - satellite
	instrument3 - instrument
	instrument4 - instrument
	satellite2 - satellite
	instrument5 - instrument
	instrument6 - instrument
	satellite3 - satellite
	instrument7 - instrument
	instrument8 - instrument
	satellite4 - satellite
	instrument9 - instrument
	instrument10 - instrument
	instrument11 - instrument
	satellite5 - satellite
	instrument12 - instrument
	instrument13 - instrument
	satellite6 - satellite
	instrument14 - instrument
	instrument15 - instrument
	instrument16 - instrument
	image0 - mode
	thermograph1 - mode
	spectrograph3 - mode
	spectrograph2 - mode
	thermograph4 - mode
	infrared5 - mode
	star5 - direction
	star2 - direction
	star1 - direction
	star0 - direction
	star3 - direction
	star4 - direction
	planet6 - direction
	phenomenon7 - direction
	planet8 - direction
	phenomenon9 - direction
	planet10 - direction
	phenomenon11 - direction
	star12 - direction
	star13 - direction
)
(:init
	(supports instrument0 spectrograph3)
	(supports instrument0 infrared5)
	(calibration_target instrument0 star2)
	(supports instrument1 infrared5)
	(supports instrument1 spectrograph3)
	(supports instrument1 spectrograph2)
	(calibration_target instrument1 star1)
	(calibration_target instrument1 star4)
	(supports instrument2 thermograph4)
	(supports instrument2 infrared5)
	(calibration_target instrument2 star4)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star4)
	(supports instrument3 spectrograph2)
	(supports instrument3 image0)
	(calibration_target instrument3 star2)
	(supports instrument4 thermograph1)
	(calibration_target instrument4 star0)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star12)
	(supports instrument5 thermograph4)
	(calibration_target instrument5 star2)
	(calibration_target instrument5 star3)
	(supports instrument6 spectrograph2)
	(supports instrument6 thermograph4)
	(supports instrument6 infrared5)
	(calibration_target instrument6 star4)
	(on_board instrument5 satellite2)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star3)
	(supports instrument7 thermograph1)
	(supports instrument7 spectrograph3)
	(supports instrument7 spectrograph2)
	(calibration_target instrument7 star4)
	(calibration_target instrument7 star1)
	(supports instrument8 spectrograph2)
	(supports instrument8 spectrograph3)
	(supports instrument8 infrared5)
	(calibration_target instrument8 star1)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon11)
	(supports instrument9 thermograph4)
	(calibration_target instrument9 star0)
	(calibration_target instrument9 star2)
	(supports instrument10 thermograph1)
	(supports instrument10 image0)
	(supports instrument10 infrared5)
	(calibration_target instrument10 star2)
	(supports instrument11 spectrograph3)
	(supports instrument11 infrared5)
	(calibration_target instrument11 star0)
	(on_board instrument9 satellite4)
	(on_board instrument10 satellite4)
	(on_board instrument11 satellite4)
	(power_avail satellite4)
	(pointing satellite4 phenomenon11)
	(supports instrument12 thermograph1)
	(supports instrument12 thermograph4)
	(supports instrument12 infrared5)
	(calibration_target instrument12 star1)
	(calibration_target instrument12 star3)
	(supports instrument13 thermograph4)
	(supports instrument13 spectrograph2)
	(calibration_target instrument13 star1)
	(calibration_target instrument13 star4)
	(on_board instrument12 satellite5)
	(on_board instrument13 satellite5)
	(power_avail satellite5)
	(pointing satellite5 planet6)
	(supports instrument14 spectrograph2)
	(supports instrument14 thermograph4)
	(supports instrument14 image0)
	(calibration_target instrument14 star0)
	(supports instrument15 spectrograph2)
	(calibration_target instrument15 star0)
	(calibration_target instrument15 star4)
	(supports instrument16 image0)
	(supports instrument16 spectrograph2)
	(supports instrument16 thermograph1)
	(calibration_target instrument16 star4)
	(calibration_target instrument16 star3)
	(on_board instrument14 satellite6)
	(on_board instrument15 satellite6)
	(on_board instrument16 satellite6)
	(power_avail satellite6)
	(pointing satellite6 star4)
)
(:goal (and
	(pointing satellite0 star3)
	(pointing satellite4 star3)
	(pointing satellite6 star12)
	(have_image planet6 spectrograph2)
	(have_image planet6 thermograph4)
	(have_image phenomenon7 thermograph1)
	(have_image phenomenon7 spectrograph3)
	(have_image planet8 thermograph1)
	(have_image planet8 spectrograph3)
	(have_image phenomenon9 thermograph4)
	(have_image phenomenon9 infrared5)
	(have_image planet10 thermograph4)
	(have_image phenomenon11 image0)
	(have_image star12 thermograph1)
	(have_image star12 infrared5)
	(have_image star13 image0)
	(have_image star13 infrared5)
))

)
