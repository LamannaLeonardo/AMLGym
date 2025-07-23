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
	instrument7 - instrument
	spectrograph1 - mode
	spectrograph2 - mode
	image0 - mode
	groundstation2 - direction
	star0 - direction
	star1 - direction
	groundstation3 - direction
	planet4 - direction
	star5 - direction
	planet6 - direction
	planet7 - direction
	star8 - direction
	phenomenon9 - direction
)
(:init
	(supports instrument0 spectrograph2)
	(supports instrument0 spectrograph1)
	(calibration_target instrument0 star0)
	(on_board instrument0 satellite0)
	(power_avail satellite0)
	(pointing satellite0 phenomenon9)
	(supports instrument1 spectrograph1)
	(supports instrument1 spectrograph2)
	(calibration_target instrument1 groundstation2)
	(supports instrument2 image0)
	(supports instrument2 spectrograph2)
	(supports instrument2 spectrograph1)
	(calibration_target instrument2 star0)
	(on_board instrument1 satellite1)
	(on_board instrument2 satellite1)
	(power_avail satellite1)
	(pointing satellite1 groundstation3)
	(supports instrument3 spectrograph1)
	(supports instrument3 image0)
	(supports instrument3 spectrograph2)
	(calibration_target instrument3 groundstation3)
	(supports instrument4 spectrograph2)
	(calibration_target instrument4 star0)
	(on_board instrument3 satellite2)
	(on_board instrument4 satellite2)
	(power_avail satellite2)
	(pointing satellite2 planet6)
	(supports instrument5 image0)
	(supports instrument5 spectrograph1)
	(calibration_target instrument5 groundstation3)
	(on_board instrument5 satellite3)
	(power_avail satellite3)
	(pointing satellite3 star5)
	(supports instrument6 spectrograph2)
	(calibration_target instrument6 star1)
	(supports instrument7 spectrograph1)
	(supports instrument7 spectrograph2)
	(supports instrument7 image0)
	(calibration_target instrument7 groundstation3)
	(on_board instrument6 satellite4)
	(on_board instrument7 satellite4)
	(power_avail satellite4)
	(pointing satellite4 planet7)
)
(:goal (and
	(pointing satellite0 star8)
	(pointing satellite3 planet4)
	(have_image planet4 spectrograph2)
	(have_image star5 spectrograph2)
	(have_image planet6 spectrograph2)
	(have_image planet7 spectrograph2)
	(have_image star8 spectrograph1)
	(have_image phenomenon9 spectrograph1)
))

)
