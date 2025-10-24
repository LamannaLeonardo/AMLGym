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
	instrument4 - instrument
	satellite3 - satellite
	instrument5 - instrument
	satellite4 - satellite
	instrument6 - instrument
	satellite5 - satellite
	instrument7 - instrument
	instrument8 - instrument
	satellite6 - satellite
	instrument9 - instrument
	instrument10 - instrument
	instrument11 - instrument
	image2 - mode
	infrared1 - mode
	infrared3 - mode
	image0 - mode
	thermograph4 - mode
	spectrograph5 - mode
	star5 - direction
	groundstation3 - direction
	star2 - direction
	star1 - direction
	groundstation0 - direction
	star4 - direction
	planet6 - direction
	phenomenon7 - direction
	star8 - direction
	star9 - direction
	planet10 - direction
	planet11 - direction
	star12 - direction
	planet13 - direction
)
(:init
	(supports instrument0 thermograph4)
	(supports instrument0 image2)
	(supports instrument0 infrared3)
	(calibration_target instrument0 star2)
	(calibration_target instrument0 groundstation0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation3)
	(supports instrument1 infrared3)
	(supports instrument1 thermograph4)
	(calibration_target instrument1 star2)
	(supports instrument2 infrared3)
	(calibration_target instrument2 star2)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star12)
	(supports instrument3 infrared3)
	(calibration_target instrument3 groundstation3)
	(calibration_target instrument3 star4)
	(supports instrument4 thermograph4)
	(calibration_target instrument4 groundstation3)
	(calibration_target instrument4 star2)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet13)
	(supports instrument5 infrared3)
	(supports instrument5 image2)
	(calibration_target instrument5 star4)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star5)
	(supports instrument6 image2)
	(supports instrument6 infrared3)
	(supports instrument6 infrared1)
	(calibration_target instrument6 star2)
	(calibration_target instrument6 groundstation0)
	(on_board instrument6 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star9)
	(supports instrument7 image2)
	(supports instrument7 infrared1)
	(calibration_target instrument7 groundstation0)
	(supports instrument8 image0)
	(supports instrument8 infrared1)
	(supports instrument8 thermograph4)
	(calibration_target instrument8 star1)
	(calibration_target instrument8 groundstation0)
	(on_board instrument7 satellite5)
	(on_board instrument8 satellite5)
	(power_avail satellite5)
	(pointing satellite5 planet6)
	(supports instrument9 infrared3)
	(supports instrument9 infrared1)
	(calibration_target instrument9 groundstation0)
	(calibration_target instrument9 star1)
	(supports instrument10 infrared1)
	(calibration_target instrument10 groundstation0)
	(calibration_target instrument10 star1)
	(supports instrument11 infrared3)
	(supports instrument11 image2)
	(supports instrument11 spectrograph5)
	(calibration_target instrument11 star4)
	(calibration_target instrument11 groundstation0)
	(on_board instrument9 satellite6)
	(on_board instrument10 satellite6)
	(on_board instrument11 satellite6)
	(power_avail satellite6)
	(pointing satellite6 phenomenon7)
)
(:goal (and
	(pointing satellite3 phenomenon7)
	(have_image planet6 thermograph4)
	(have_image planet6 infrared3)
	(have_image phenomenon7 infrared1)
	(have_image star8 infrared3)
	(have_image star8 spectrograph5)
	(have_image star9 infrared1)
	(have_image star9 image0)
	(have_image planet10 image2)
	(have_image planet11 infrared1)
	(have_image star12 infrared1)
	(have_image planet13 infrared1)
	(have_image planet13 image0)
))

)
