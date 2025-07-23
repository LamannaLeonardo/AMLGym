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
	instrument5 - instrument
	satellite2 - satellite
	instrument6 - instrument
	instrument7 - instrument
	satellite3 - satellite
	instrument8 - instrument
	satellite4 - satellite
	instrument9 - instrument
	instrument10 - instrument
	instrument11 - instrument
	satellite5 - satellite
	instrument12 - instrument
	satellite6 - satellite
	instrument13 - instrument
	infrared5 - mode
	image2 - mode
	spectrograph0 - mode
	image1 - mode
	spectrograph4 - mode
	infrared3 - mode
	star4 - direction
	groundstation3 - direction
	star1 - direction
	groundstation2 - direction
	groundstation0 - direction
	star5 - direction
	planet6 - direction
	planet7 - direction
	star8 - direction
	phenomenon9 - direction
	planet10 - direction
	planet11 - direction
	planet12 - direction
	phenomenon13 - direction
)
(:init
	(supports instrument0 spectrograph4)
	(supports instrument0 image1)
	(supports instrument0 spectrograph0)
	(calibration_target instrument0 groundstation3)
	(calibration_target instrument0 groundstation0)
	(supports instrument1 infrared5)
	(supports instrument1 spectrograph4)
	(supports instrument1 image1)
	(calibration_target instrument1 groundstation2)
	(calibration_target instrument1 star4)
	(supports instrument2 infrared3)
	(supports instrument2 infrared5)
	(calibration_target instrument2 groundstation3)
	(on_board instrument0 satellite0)
	(on_board instrument1 satellite0)
	(on_board instrument2 satellite0)
	(power_avail satellite0)
	(pointing satellite0 groundstation0)
	(supports instrument3 infrared5)
	(supports instrument3 spectrograph0)
	(calibration_target instrument3 groundstation0)
	(calibration_target instrument3 star1)
	(supports instrument4 spectrograph0)
	(supports instrument4 spectrograph4)
	(calibration_target instrument4 groundstation3)
	(supports instrument5 spectrograph4)
	(supports instrument5 infrared3)
	(calibration_target instrument5 star4)
	(calibration_target instrument5 groundstation0)
	(on_board instrument3 satellite1)
	(on_board instrument4 satellite1)
	(on_board instrument5 satellite1)
	(power_avail satellite1)
	(pointing satellite1 planet10)
	(supports instrument6 image1)
	(calibration_target instrument6 star4)
	(supports instrument7 infrared5)
	(supports instrument7 spectrograph4)
	(supports instrument7 infrared3)
	(calibration_target instrument7 star5)
	(calibration_target instrument7 groundstation3)
	(on_board instrument6 satellite2)
	(on_board instrument7 satellite2)
	(power_avail satellite2)
	(pointing satellite2 groundstation3)
	(supports instrument8 image1)
	(supports instrument8 spectrograph4)
	(calibration_target instrument8 groundstation2)
	(calibration_target instrument8 star5)
	(on_board instrument8 satellite3)
	(power_avail satellite3)
	(pointing satellite3 groundstation0)
	(supports instrument9 infrared3)
	(calibration_target instrument9 star1)
	(calibration_target instrument9 groundstation0)
	(supports instrument10 infrared3)
	(calibration_target instrument10 groundstation2)
	(calibration_target instrument10 groundstation0)
	(supports instrument11 image1)
	(calibration_target instrument11 groundstation0)
	(on_board instrument9 satellite4)
	(on_board instrument10 satellite4)
	(on_board instrument11 satellite4)
	(power_avail satellite4)
	(pointing satellite4 star4)
	(supports instrument12 image1)
	(supports instrument12 spectrograph4)
	(supports instrument12 image2)
	(calibration_target instrument12 groundstation0)
	(calibration_target instrument12 groundstation2)
	(on_board instrument12 satellite5)
	(power_avail satellite5)
	(pointing satellite5 groundstation0)
	(supports instrument13 spectrograph4)
	(supports instrument13 infrared3)
	(supports instrument13 spectrograph0)
	(calibration_target instrument13 star5)
	(on_board instrument13 satellite6)
	(power_avail satellite6)
	(pointing satellite6 planet7)
)
(:goal (and
	(pointing satellite0 planet11)
	(pointing satellite2 star4)
	(pointing satellite5 groundstation0)
	(pointing satellite6 star1)
	(have_image planet6 infrared5)
	(have_image planet7 image1)
	(have_image planet7 spectrograph0)
	(have_image star8 infrared5)
	(have_image star8 infrared3)
	(have_image phenomenon9 image1)
	(have_image phenomenon9 spectrograph0)
	(have_image planet10 infrared3)
	(have_image planet11 image2)
	(have_image planet12 spectrograph4)
	(have_image planet12 infrared3)
	(have_image phenomenon13 spectrograph4)
))

)
