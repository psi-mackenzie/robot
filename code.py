import color_sensor
import distance_sensor
from hub import light_matrix, motion_sensor, port, power_off
import motor_pair
import runloop

# constants
YAW_FACE=motion_sensor.TOP
MOTOR_PAIR = motor_pair.PAIR_1
FIRST_MOTOR_PORT = port.F
SECOND_MOTOR_PORT = port.E
DEFAULT_SENSOR_COLOR_PORT = port.D
SECONDARY_SENSOR_COLOR_PORT = port.B
DISTANCE_SENSOR_PORT = port.C
DEFAULT_VELOCITY = 540
MIN_DISTANCE_TO_POLLUTANT = 4.7
DEGREES_TO_KILL_POLLUTANT = 30
MOTOR_DEGREES_TO_TURN_90_DEGREES = 214
MICROADJUSTMENT_DEPTH = 10
DEFAULT_SENSOR_COLOR_DEPTH = 100

# main function
async def main():
    motion_sensor.set_yaw_face(YAW_FACE)
    motion_sensor.reset_yaw(0)
    motor_pair.pair(MOTOR_PAIR, FIRST_MOTOR_PORT, SECOND_MOTOR_PORT)

    center_color = 0

    await motor_pair.move_for_degrees(MOTOR_PAIR, 920, 0, velocity=DEFAULT_VELOCITY)
    await turn(91)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 1200, 0, velocity=DEFAULT_VELOCITY)
    await microadjustment(90)
    motion_sensor.reset_yaw(0)
    await microadjustment()

    distance_to_center = get_distance()
    await turn(180)
    await microadjustment(180)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -int(28 * distance_to_center) - 45, 0, velocity=DEFAULT_VELOCITY)
    await microadjustment(180)
    center_color = await read_color_with_depth(sensor=SECONDARY_SENSOR_COLOR_PORT)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 150, 0, velocity=DEFAULT_VELOCITY)
    await microadjustment(180)

    for i in range(0, 8):
        direction = 1 if i < 4 else -1
        print("{}. poluente:".format(i))

        if i == 0:
            await pollutant_mission_route_leaving_the_center(center_color, direction)
        elif i == 4:
            await pollutant_mission_route_going_from_one_side_to_the_other(center_color, direction)
        else:
            await pollutant_mission_standard_route(center_color, direction)

    return
    power_off()

# pollutant mission

async def pollutant_mission_route_leaving_the_center(center_color, direction):
    await motor_pair.move_for_degrees(MOTOR_PAIR, 504, 0, velocity=DEFAULT_VELOCITY)
    await microadjustment(180)
    await turn(-90)
    await microadjustment(90)
    motion_sensor.reset_yaw(0)
    await go_to_pollutant()
    await do_pollutant_mission(center_color, direction)

async def pollutant_mission_route_going_from_one_side_to_the_other(center_color, direction):
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, -405, 0, velocity=DEFAULT_VELOCITY)
    await turn(180)
    await microadjustment(180)
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 100, 0, velocity=DEFAULT_VELOCITY)
    await microadjustment(180)
    await go_to_pollutant()
    await do_pollutant_mission(center_color, direction)
    motion_sensor.reset_yaw(0)

async def pollutant_mission_standard_route(center_color, direction): # 
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, -55, 0, velocity=DEFAULT_VELOCITY)
    await turn(-90)
    await microadjustment(-90)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 519, 0, velocity=DEFAULT_VELOCITY)
    await turn(90)
    await microadjustment()
    await go_to_pollutant()
    await do_pollutant_mission(center_color, direction)
    motion_sensor.reset_yaw(0)

# useful functions for missions

async def go_to_pollutant():
    await microadjustment()
    await go_to_a_certain_distance(MIN_DISTANCE_TO_POLLUTANT)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 50, 0, velocity=DEFAULT_VELOCITY)
    await microadjustment()

async def do_pollutant_mission(center_color, k):
    await microadjustment()
    pollutant_color = await read_color_with_depth()

    if pollutant_color == center_color:
        await turn(-DEGREES_TO_KILL_POLLUTANT * k, DEFAULT_VELOCITY)
        await runloop.sleep_ms(100)
        await turn(DEGREES_TO_KILL_POLLUTANT * k, DEFAULT_VELOCITY)

    await microadjustment()

# useful functions

async def go_to_a_certain_distance(distance):
    motor_pair.move(MOTOR_PAIR, 0, velocity=DEFAULT_VELOCITY)
    await runloop.until(lambda: get_distance() < distance)
    motor_pair.stop(MOTOR_PAIR)

async def turn(degrees, velocity=360):
    mov_degrees = int((MOTOR_DEGREES_TO_TURN_90_DEGREES * degrees) / 90)
    await motor_pair.move_for_degrees(MOTOR_PAIR, mov_degrees, 100, velocity=velocity)

async def microadjustment(angle = 0):
    if get_yaw_angle() == angle:
        return

    for _ in range(0, 9):
        await runloop.sleep_ms(25)
        await turn(angle - abs(get_yaw_angle()) if angle == 180 else angle - get_yaw_angle())

# sensor facilitating functions

def get_yaw_angle():
    return motion_sensor.tilt_angles()[0] / 10

def get_distance():
    return distance_sensor.distance(DISTANCE_SENSOR_PORT) / 10

async def read_color_with_depth(depth=DEFAULT_SENSOR_COLOR_DEPTH, sensor=DEFAULT_SENSOR_COLOR_PORT):
    await runloop.sleep_ms(25)
    color = color_sensor.color(sensor)

    if color == 9:
        light_matrix.write("V")
        return "Vermelho"
    if depth == 0 or color == 0:
        light_matrix.write("P")
        return "Preto"
    return await read_color_with_depth(depth - 1)

# run main function
runloop.run(main())
