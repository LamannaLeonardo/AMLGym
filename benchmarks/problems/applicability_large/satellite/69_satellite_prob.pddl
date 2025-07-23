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
	satellite3 - satellite
	instrument6 - instrument
	satellite4 - satellite
	instrument7 - instrument
	instrument8 - instrument
	satellite5 - satellite
	instrument9 - instrument
	instrument10 - instrument
	instrument11 - instrument
	satellite6 - satellite
	instrument12 - instrument
	image2 - mode
	image4 - mode
	image3 - mode
	thermograph1 - mode
	image0 - mode
	infrared5 - mode
	star3 - direction
	groundstation2 - direction
	star5 - direction
	groundstation0 - direction
	groundstation1 - direction
	groundstation4 - direction
	planet6 - direction
	phenomenon7 - direction
	planet8 - direction
	star9 - direction
	phenomenon10 - direction
	phenomenon11 - direction
	planet12 - direction
	planet13 - direction
)
(:init
	(supports instrument0 image0)
	(supports instrument0 infrared5)
	(calibration_target instrument0 groundstation2)
	(calibration_target instrument0 groundstation0)
	(supports instrument1 image0)
	(calibration_target instrument1 star5)
	(calibration_target instrument1 groundstation0)
	(supports instrument2 image4)
	(supports instrument2 image0)
	(calibration_target instrument2 groundstation4)
	(calibration_target instrument2 groundstation2)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation0)
	(supports instrument3 image4)
	(supports instrument3 image0)
	(supports instrument3 image2)
	(calibration_target instrument3 groundstation0)
	(supports instrument4 thermograph1)
	(supports instrument4 infrared5)
	(supports instrument4 image0)
	(calibration_target instrument4 groundstation0)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet8)
	(supports instrument5 image3)
	(supports instrument5 image4)
	(supports instrument5 thermograph1)
	(calibration_target instrument5 star5)
	(on_board instrument5 satellite2)
	(power_avail satellite2)
	(pointing satellite2 star3)
	(supports instrument6 image0)
	(calibration_target instrument6 star5)
	(calibration_target instrument6 star3)
	(on_board instrument6 satellite3)
	(power_avail satellite3)
	(pointing satellite3 planet13)
	(supports instrument7 image2)
	(supports instrument7 image3)
	(supports instrument7 image4)
	(calibration_target instrument7 star5)
	(supports instrument8 image0)
	(supports instrument8 image3)
	(calibration_target instrument8 groundstation2)
	(calibration_target instrument8 groundstation0)
	(on_board instrument7 satellite4)
	(on_board instrument8 satellite4)
	(power_avail satellite4)
	(pointing satellite4 planet6)
	(supports instrument9 image2)
	(supports instrument9 thermograph1)
	(calibration_target instrument9 star5)
	(calibration_target instrument9 groundstation1)
	(supports instrument10 thermograph1)
	(supports instrument10 image2)
	(calibration_target instrument10 groundstation0)
	(supports instrument11 image0)
	(calibration_target instrument11 groundstation1)
	(on_board instrument9 satellite5)
	(on_board instrument10 satellite5)
	(on_board instrument11 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star3)
	(supports instrument12 image3)
	(calibration_target instrument12 groundstation4)
	(on_board instrument12 satellite6)
	(power_avail satellite6)
	(pointing satellite6 groundstation1)
)
(:goal (and
	(pointing satellite0 phenomenon11)
	(pointing satellite1 groundstation0)
	(pointing satellite2 groundstation4)
	(pointing satellite5 star3)
	(have_image planet6 infrared5)
	(have_image planet6 image4)
	(have_image phenomenon7 image0)
	(have_image phenomenon7 thermograph1)
	(have_image planet8 thermograph1)
	(have_image star9 image3)
	(have_image phenomenon10 thermograph1)
	(have_image phenomenon11 infrared5)
	(have_image phenomenon11 image4)
	(have_image planet12 image2)
	(have_image planet12 image0)
	(have_image planet13 infrared5)
	(have_image planet13 image4)
))

)
