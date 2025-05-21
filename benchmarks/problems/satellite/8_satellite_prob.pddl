(define (problem strips-sat-x-1)
(:domain satellite)
(:objects
	satellite0 - satellite
	instrument0 - instrument
	instrument1 - instrument
	instrument2 - instrument
	instrument3 - instrument
	instrument4 - instrument
	satellite1 - satellite
	instrument5 - instrument
	satellite2 - satellite
	instrument6 - instrument
	satellite3 - satellite
	instrument7 - instrument
	satellite4 - satellite
	instrument8 - instrument
	instrument9 - instrument
	satellite5 - satellite
	instrument10 - instrument
	instrument11 - instrument
	instrument12 - instrument
	instrument13 - instrument
	satellite6 - satellite
	instrument14 - instrument
	instrument15 - instrument
	instrument16 - instrument
	image0 - mode
	spectrograph4 - mode
	image1 - mode
	image3 - mode
	spectrograph2 - mode
	star0 - direction
	star2 - direction
	star5 - direction
	groundstation3 - direction
	groundstation4 - direction
	groundstation1 - direction
	star6 - direction
	star7 - direction
	planet8 - direction
	star9 - direction
	phenomenon10 - direction
	planet11 - direction
	planet12 - direction
	phenomenon13 - direction
)
(:init
	(supports instrument0 image0)
	(calibration_target instrument0 groundstation4)
	(calibration_target instrument0 star0)
	(supports instrument1 image0)
	(calibration_target instrument1 star5)
	(supports instrument2 image1)
	(supports instrument2 image3)
	(supports instrument2 spectrograph4)
	(calibration_target instrument2 star0)
	(supports instrument3 spectrograph4)
	(calibration_target instrument3 groundstation3)
	(supports instrument4 spectrograph2)
	(supports instrument4 image3)
	(calibration_target instrument4 groundstation3)
	(calibration_target instrument4 groundstation4)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(on_board instrument3 satellite0)
	(on_board instrument4 satellite0)
	(power_avail satellite0)
	(pointing satellite0 planet11)
	(supports instrument5 image1)
	(calibration_target instrument5 groundstation4)
	(calibration_target instrument5 star2)
	(on_board instrument5 satellite1)
	(power_avail satellite1)
	(pointing satellite1 star9)
	(supports instrument6 spectrograph4)
	(supports instrument6 spectrograph2)
	(calibration_target instrument6 groundstation3)
	(on_board instrument6 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet11)
	(supports instrument7 spectrograph4)
	(supports instrument7 image3)
	(calibration_target instrument7 groundstation1)
	(calibration_target instrument7 groundstation3)
	(on_board instrument7 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star6)
	(supports instrument8 image0)
	(calibration_target instrument8 groundstation4)
	(supports instrument9 image1)
	(supports instrument9 spectrograph2)
	(supports instrument9 image3)
	(calibration_target instrument9 star5)
	(calibration_target instrument9 star2)
	(on_board instrument8 satellite4)
	(on_board instrument9 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star2)
	(supports instrument10 image0)
	(supports instrument10 image3)
	(calibration_target instrument10 star2)
	(calibration_target instrument10 star0)
	(supports instrument11 spectrograph4)
	(calibration_target instrument11 groundstation1)
	(supports instrument12 image0)
	(supports instrument12 image1)
	(supports instrument12 spectrograph4)
	(calibration_target instrument12 star0)
	(calibration_target instrument12 groundstation4)
	(supports instrument13 image0)
	(calibration_target instrument13 star2)
	(calibration_target instrument13 star5)
	(on_board instrument10 satellite5)
	(on_board instrument11 satellite5)
	(on_board instrument12 satellite5)
	(on_board instrument13 satellite5)
	(power_avail satellite5)
	(pointing satellite5 star7)
	(supports instrument14 spectrograph2)
	(supports instrument14 spectrograph4)
	(calibration_target instrument14 groundstation3)
	(calibration_target instrument14 star5)
	(supports instrument15 spectrograph4)
	(supports instrument15 spectrograph2)
	(calibration_target instrument15 groundstation4)
	(supports instrument16 image1)
	(supports instrument16 image0)
	(calibration_target instrument16 groundstation1)
	(calibration_target instrument16 groundstation4)
	(on_board instrument14 satellite6)
	(on_board instrument15 satellite6)
	(on_board instrument16 satellite6)
	(power_avail satellite6)
	(pointing satellite6 phenomenon13)
)
(:goal (and
	(pointing satellite1 planet12)
	(pointing satellite4 planet12)
	(have_image star6 image1)
	(have_image star7 image0)
	(have_image planet8 spectrograph4)
	(have_image star9 spectrograph4)
	(have_image phenomenon10 spectrograph4)
	(have_image planet11 spectrograph2)
	(have_image planet12 image1)
	(have_image phenomenon13 image1)
))

)
