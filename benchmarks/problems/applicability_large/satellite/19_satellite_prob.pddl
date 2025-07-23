(define (problem strips_sat_x_1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	satellite1 - satellite
	instrument2 - instrument
	instrument3 - instrument
	satellite2 - satellite
	instrument4 - instrument
	instrument5 - instrument
	instrument6 - instrument
	satellite3 - satellite
	instrument7 - instrument
	instrument8 - instrument
	instrument9 - instrument
	satellite4 - satellite
	instrument10 - instrument
	satellite5 - satellite
	instrument11 - instrument
	instrument12 - instrument
	satellite6 - satellite
	instrument13 - instrument
	image2 - mode
	image5 - mode
	infrared0 - mode
	thermograph1 - mode
	spectrograph3 - mode
	spectrograph4 - mode
	star0 - direction
	star3 - direction
	star1 - direction
	star5 - direction
	groundstation4 - direction
	groundstation2 - direction
	phenomenon6 - direction
	planet7 - direction
	phenomenon8 - direction
	phenomenon9 - direction
	phenomenon10 - direction
	phenomenon11 - direction
	phenomenon12 - direction
	planet13 - direction
)
(:init
	(supports instrument0 image5)
	(supports instrument0 thermograph1)
	(calibration_target instrument0 star5)
	(calibration_target instrument0 star3)
	(supports instrument1 image5)
	(calibration_target instrument1 groundstation4)
	(calibration_target instrument1 groundstation2)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(power_avail satellite0)
	(pointing satellite0 star5)
	(supports instrument2 image5)
	(calibration_target instrument2 groundstation4)
	(calibration_target instrument2 groundstation2)
	(supports instrument3 image2)
	(supports instrument3 thermograph1)
	(calibration_target instrument3 star0)
	(on_board instrument2 satellite1)
	(on_board instrument3 satellite1)
	(power_avail satellite1)
	(pointing satellite1 phenomenon10)
	(supports instrument4 image2)
	(supports instrument4 image5)
	(calibration_target instrument4 star0)
	(calibration_target instrument4 star3)
	(supports instrument5 thermograph1)
	(supports instrument5 image2)
	(supports instrument5 image5)
	(calibration_target instrument5 star3)
	(calibration_target instrument5 star0)
	(supports instrument6 thermograph1)
	(calibration_target instrument6 star3)
	(calibration_target instrument6 star5)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation4)
	(supports instrument7 infrared0)
	(supports instrument7 image5)
	(supports instrument7 image2)
	(calibration_target instrument7 star3)
	(calibration_target instrument7 star1)
	(supports instrument8 thermograph1)
	(supports instrument8 infrared0)
	(supports instrument8 spectrograph4)
	(calibration_target instrument8 star1)
	(supports instrument9 thermograph1)
	(supports instrument9 spectrograph4)
	(calibration_target instrument9 star3)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(on_board instrument9 satellite3)
	(power_avail satellite3)
	(pointing satellite3 phenomenon10)
	(supports instrument10 image5)
	(supports instrument10 spectrograph3)
	(supports instrument10 thermograph1)
	(calibration_target instrument10 star5)
	(calibration_target instrument10 star1)
	(on_board instrument10 satellite4)
	(power_avail satellite4)
	(pointing satellite4 groundstation2)
	(supports instrument11 thermograph1)
	(calibration_target instrument11 groundstation4)
	(supports instrument12 thermograph1)
	(supports instrument12 infrared0)
	(calibration_target instrument12 groundstation4)
	(calibration_target instrument12 groundstation2)
	(on_board instrument11 satellite5)
	(on_board instrument12 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star1)
	(supports instrument13 spectrograph4)
	(supports instrument13 thermograph1)
	(supports instrument13 image5)
	(calibration_target instrument13 groundstation2)
	(on_board instrument13 satellite6)
	(power_avail satellite6)
	(pointing satellite6 phenomenon6)
)
(:goal (and
	(pointing satellite0 planet13)
	(pointing satellite6 planet7)
	(have_image phenomenon6 spectrograph3)
	(have_image planet7 spectrograph3)
	(have_image phenomenon8 image2)
	(have_image phenomenon9 image5)
	(have_image phenomenon10 spectrograph3)
	(have_image phenomenon11 spectrograph4)
	(have_image phenomenon12 spectrograph4)
	(have_image phenomenon12 image5)
	(have_image planet13 image5)
	(have_image planet13 thermograph1)
))

)
