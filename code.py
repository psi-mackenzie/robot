import color_sensor
import distance_sensor
from hub import light_matrix, port, motion_sensor
import motor
import motor_pair
import runloop

# Yaw Variables
YAW_FACE = motion_sensor.TOP
DEFAULT_YAW_VALUE = 0

# Motor Variables
FIRST_MOTOR_PORT = port.D
SECOND_MOTOR_PORT = port.C

# Runtime Variables
TIME_TO_SLEEP = 100
MAX_DISTANCE_TO_CENTER = 10.1
MAX_DISTANCE_TO_POLLUTANT = 4.7

async def main():
    motion_sensor.set_yaw_face(YAW_FACE)
    motion_sensor.reset_yaw(DEFAULT_YAW_VALUE)

    motor_pair.pair(motor_pair.PAIR_1, FIRST_MOTOR_PORT, SECOND_MOTOR_PORT)

    center_color = 0

    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 920, 0, velocity=360)
    await turn(90)
    motion_sensor.reset_yaw(DEFAULT_YAW_VALUE)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 1200, 0, velocity=700)
    await runloop.sleep_ms(TIME_TO_SLEEP)

    await micro_ajuste()
    await go_to_center()
    await runloop.sleep_ms(TIME_TO_SLEEP * 2)
    center_color = color()
    print(f"A cor do centro identicada foi {center_color}")

    print("Primeiro Poluente:")
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -440, 0, velocity=360)
    await turn(90)
    motion_sensor.reset_yaw(DEFAULT_YAW_VALUE)
    await runloop.sleep_ms(TIME_TO_SLEEP)
    await go_to_pollutant()
    await do_pollutant_mission(center_color, 1)

    print("Segundo poluente:")
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -70, 0, velocity=360)
    await turn(-90)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 515, 0, velocity=360)
    await turn(90)
    await go_to_pollutant()
    await do_pollutant_mission(center_color, 1)

    print("Terceiro poluente:")
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -70, 0, velocity=360)
    await turn(-45)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 105, 0, velocity=360)
    await turn(-45)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 605, 0, velocity=360)
    await motor.run_for_degrees(port.D, 528, 360)
    await go_to_pollutant()
    await do_pollutant_mission(center_color, 1)

    print("Quarto poluente:")
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -70, 0, velocity=360)
    await turn(-90)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 525, 0, velocity=360)
    await turn(90)
    await go_to_pollutant()
    await do_pollutant_mission(center_color, 1)

    print("Quinto poluente:")
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -340, 0, velocity=360)
    await turn(180)
    motion_sensor.reset_yaw(0)
    await go_to_pollutant()
    await do_pollutant_mission(center_color, -1)

    print("Sexto poluente:")
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -70, 0, velocity=360)
    await turn(-90)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 525, 0, velocity=360)
    await turn(90)
    await go_to_pollutant()
    await do_pollutant_mission(center_color, -1)

    print("Sétimo poluente:")
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -70, 0, velocity=360)
    await turn(-45)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 105, 0, velocity=360)
    await turn(-45)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 605, 0, velocity=360)
    await motor.run_for_degrees(port.D, 528, 360)
    await go_to_pollutant()
    await do_pollutant_mission(center_color, -1)

    print("Oitavo poluente:")
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -70, 0, velocity=360)
    await turn(-90)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 525, 0, velocity=360)
    await turn(90)
    await go_to_pollutant()
    await do_pollutant_mission(center_color, -1)

async def do_pollutant_mission(center_color, k):
    await micro_ajuste()
    pollutant_color = color()
    print(f"A cor do poluente identicada foi {pollutant_color}")

    if pollutant_color == center_color:
        await turn(-25 * k)
        await runloop.sleep_ms(TIME_TO_SLEEP)
        await turn(25 * k)
    
    await micro_ajuste()

def angle():
    return motion_sensor.tilt_angles()[0] / 10

def distance():
    return distance_sensor.distance(port.F) / 10

def color():
    color = color_sensor.color(port.E)
    if color == 9:
        return "Vermelho"
    else:
        return "Preto"

async def turn(degrees):
    if degrees > 0:
        motor_pair.move(motor_pair.PAIR_1, 100, velocity=500)
        await runloop.until(lambda: angle() > degrees + 1)
    else:
        motor_pair.move(motor_pair.PAIR_1, -100, velocity=500)
        await runloop.until(lambda: angle() < degrees - 1)

    motor_pair.stop(motor_pair.PAIR_1)
    motion_sensor.reset_yaw(DEFAULT_YAW_VALUE)

async def go_to_center():
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=360)
    await runloop.until(lambda: distance() < MAX_DISTANCE_TO_CENTER)
    motor_pair.stop(motor_pair.PAIR_1)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 180, 0, velocity=360)

async def go_to_pollutant():
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=360)
    await runloop.until(lambda: distance() < MAX_DISTANCE_TO_POLLUTANT)
    motor_pair.stop(motor_pair.PAIR_1)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 55, 0, velocity=360)

async def micro_ajuste():
    error = angle()
    await turn(error)

runloop.run(main())
