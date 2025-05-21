(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	satellite1 - satellite
	instrument1 - instrument
	instrument2 - instrument
	satellite2 - satellite
	instrument3 - instrument
	instrument4 - instrument
	instrument5 - instrument
	instrument6 - instrument
	satellite3 - satellite
	instrument7 - instrument
	instrument8 - instrument
	satellite4 - satellite
	instrument9 - instrument
	instrument10 - instrument
	instrument11 - instrument
	instrument12 - instrument
	satellite5 - satellite
	instrument13 - instrument
	instrument14 - instrument
	satellite6 - satellite
	instrument15 - instrument
	infrared4 - mode
	spectrograph3 - mode
	thermograph0 - mode
	image1 - mode
	image5 - mode
	image2 - mode
	groundstation2 - direction
	groundstation1 - direction
	star3 - direction
	groundstation0 - direction
	groundstation4 - direction
	groundstation5 - direction
	planet6 - direction
	star7 - direction
	phenomenon8 - direction
	phenomenon9 - direction
	planet10 - direction
	planet11 - direction
	phenomenon12 - direction
	phenomenon13 - direction
)
(:init
	(supports instrument0 spectrograph3)
	(supports instrument0 image5)
	(calibration_target instrument0 groundstation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon9)
	(supports instrument1 image5)
	(supports instrument1 thermograph0)
	(calibration_target instrument1 groundstation2)
	(calibration_target instrument1 groundstation4)
	(supports instrument2 image2)
	(supports instrument2 image1)
	(calibration_target instrument2 groundstation0)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet11)
	(supports instrument3 spectrograph3)
	(calibration_target instrument3 groundstation2)
	(calibration_target instrument3 groundstation0)
	(supports instrument4 image1)
	(supports instrument4 infrared4)
	(calibration_target instrument4 star3)
	(supports instrument5 spectrograph3)
	(supports instrument5 image5)
	(supports instrument5 image2)
	(calibration_target instrument5 groundstation2)
	(calibration_target instrument5 groundstation4)
	(supports instrument6 image1)
	(supports instrument6 thermograph0)
	(supports instrument6 image2)
	(calibration_target instrument6 groundstation5)
	(calibration_target instrument6 star3)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(on_board instrument5 satellite2)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation4)
	(supports instrument7 spectrograph3)
	(supports instrument7 image5)
	(supports instrument7 image1)
	(calibration_target instrument7 groundstation1)
	(calibration_target instrument7 groundstation5)
	(supports instrument8 image2)
	(calibration_target instrument8 star3)
	(on_board instrument7 satellite3)
	(on_board instrument8 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet6)
	(supports instrument9 infrared4)
	(supports instrument9 image2)
	(calibration_target instrument9 groundstation0)
	(supports instrument10 thermograph0)
	(supports instrument10 spectrograph3)
	(supports instrument10 image1)
	(calibration_target instrument10 groundstation0)
	(calibration_target instrument10 groundstation5)
	(supports instrument11 image1)
	(supports instrument11 spectrograph3)
	(calibration_target instrument11 star3)
	(supports instrument12 image2)
	(calibration_target instrument12 groundstation0)
	(on_board instrument9 satellite4)
	(on_board instrument10 satellite4)
	(on_board instrument11 satellite4)
	(on_board instrument12 satellite4)
	(power_avail satellite4)
	(pointing satellite4 groundstation2)
	(supports instrument13 thermograph0)
	(supports instrument13 spectrograph3)
	(supports instrument13 image1)
	(calibration_target instrument13 groundstation5)
	(supports instrument14 image2)
	(supports instrument14 infrared4)
	(calibration_target instrument14 groundstation4)
	(on_board instrument13 satellite5)
	(on_board instrument14 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star7)
	(supports instrument15 image2)
	(supports instrument15 thermograph0)
	(calibration_target instrument15 groundstation5)
	(on_board instrument15 satellite6)
	(power_avail satellite6)
	(pointing satellite6 planet11)
)
(:goal (and
	(pointing satellite0 groundstation4)
	(pointing satellite2 groundstation1)
	(pointing satellite3 groundstation2)
	(pointing satellite5 phenomenon8)
	(pointing satellite6 planet11)
	(have_image planet6 image2)
	(have_image planet6 spectrograph3)
	(have_image star7 image1)
	(have_image star7 image5)
	(have_image phenomenon8 infrared4)
	(have_image phenomenon8 image5)
	(have_image phenomenon9 infrared4)
	(have_image planet10 thermograph0)
	(have_image planet10 spectrograph3)
	(have_image planet11 image5)
	(have_image phenomenon12 thermograph0)
	(have_image phenomenon13 spectrograph3)
))

)
