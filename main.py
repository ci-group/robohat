
from __future__ import absolute_import, division, print_function, unicode_literals

import time
import main_config

try:
    from robohatlib.Robohat import Robohat
    from robohatlib.hal.assemblyboard.ServoAssemblyConfig import ServoAssemblyConfig
    from robohatlib.hal.assemblyboard.servo.ServoData import ServoData
    from robohatlib.hal.datastructure.Color import Color
except ImportError:
    print("Failed to import Robohat, or failed to import all dependencies")
    raise

#--------------------

def main():
    print("################################################")

    robohat = Robohat(main_config.servoassembly_1_config, main_config.servoassembly_2_config, main_config.TOPBOARD_IOEXANDER_SW)
    robohat.init(main_config.SERVOBOARD_1_DATAS_ARRAY, main_config.SERVOBOARD_2_DATAS_ARRAY)

    #robohat.set_direction_ioexpander(0, EXPANDERDIR.OUTPUT)
    #robohat.set_direction_ioexpander(1, EXPANDERDIR.OUTPUT)

    while True:
        adccodesarry = robohat.get_servos_adc_readout_multiple_channels()
        #print(adccodesarry)
        # for i in range(1,17):
        #     #print("-->" + str(i) + " " + str(adccodesarry[i]) + " V")
        #
        #
        #     print(str(i) + "-->" + str(robohat.get_servo_adc_readout_single_channel(i)) + " V, " + str(robohat.get_servo_angle(i)) + " °")
        #





        #angledarray = robohat.get_servos_angles()
        #print(angledarray)
        # for i in range(1,17):
        #     print("-->" + str(i) + " " + str(angledarray[i]) + " °")
        #voltage_adc_hat = robohat.get_readout_hatadc_mutiplechannels()
        #print("-->" + str(voltage_adc_hat) + " V")
        # robohat.set_servoassembly_1_servo_angle(1, 180)
        # time.sleep(1)
        #robohat.set_servoassembly_1_servo_angle(1, 0)
        # time.sleep(1)
        #robohat.set_ouput_ioexpander(0, EXPANDERSTATUS.LOW)
        #robohat.set_ouput_ioexpander(1, EXPANDERSTATUS.LOW)

        robohat.set_led_color(Color.GREEN)
        # for i in range(1,1800, 1):
        #     angle:float = i / 10.0
        #     robohat.set_servos_angles([angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle])
        # #print("-->" + str(robohat.get_servo_adc_readout_single_channels(1)) + " V," + str(robohat.get_servo_adc_readout_single_channels(16)) + " V")
        #     print("-->" + str(robohat.get_servo_angle(1)) + " °," + str(robohat.get_servo_angle(16)) + " °")
        time.sleep(1)
        #
        # robohat.set_led_color(Color.RED)
        # for i in range(1800,1, -1):
        #     angle:float = i / 10.0
        #     robohat.set_servos_angles([angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle, angle])
        #     print("-->" + str(robohat.get_servo_angle(1)) + " °" + str(robohat.get_servo_angle(16)) + " °")
        # time.sleep(1)

        #robohat.do_shutdown()

        #print("connected: " + str(robohat.get_is_servo_connected(1)) )

        # robohat.set_servoassembly_1_allservos_angle([  70, 0,   0, 0,   0, 180,   0, 180,   0, 180,   0, 180,   0, 180,   0, 180])
        # time.sleep(2)
        # #print("Stat " + str(robohat.get_input_ioexpander(2)))
        # #robohat.set_ouput_ioexpander(0,EXPANDERSTATUS.HIGH)
        # #robohat.set_ouput_ioexpander(1, EXPANDERSTATUS.HIGH)
        # #
        # #
        # # adccodesarry = robohat.get_servoassembly_1_readout_adc_mutiplechannels()
        # # for i in range(0,16):
        # #     print("-->" + str(i) + " " + str(adccodesarry[i]) + " V")
        # #
        # # robohat.set_color_led(Color.GREEN)
        # robohat.set_servoassembly_1_allservos_angle([120,   180, 180,   180, 180,   0, 180,   0, 180,   0, 180,   0, 180,   0, 180,   0])
        #

        #print("Stat " + str(robohat.get_input_ioexpander(2)) )

        #robohat.slowwoop_buzzer()
        #robohat.beep_buzzer()

        #robohat.do_imu_test()

        #print("------------------------------------------------------------")


if __name__ == "__main__":
    main()
