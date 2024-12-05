import color_sensor
import distance_sensor
from hub import light_matrix, motion_sensor, port, power_off
import motor
import motor_pair
import runloop

# constants
YAW_FACE=motion_sensor.TOP
MOTOR_PAIR = motor_pair.PAIR_1
FIRST_MOTOR_PORT = port.F
SECOND_MOTOR_PORT = port.D
CLAW_MOTOR_PORT = port.C
CLAW_STRAIGHT_UP_ANGLE = 322
CLAW_TOTALLY_UP_ANGLE = 305
CLAW_TOTALLY_DOWN_ANGLE = 68
CLAW_POLUENTE = 1
CLAW_POLUENTE_DERRUBAR = 41
PONTO_PERFEITO = 331
PRIMARY_SENSOR_COLOR_PORT = port.E
SECONDARY_SENSOR_COLOR_PORT = port.A
DISTANCE_SENSOR_PORT = port.B
DEFAULT_VELOCITY = 540
MIN_DISTANCE_TO_POLLUTANT = 4.7
DEGREES_TO_KILL_POLLUTANT = 30
MOTOR_DEGREES_TO_TURN_90_DEGREES = 212
MICROADJUSTMENT_DEPTH = 20
DEFAULT_SENSOR_COLOR_DEPTH = 25

# main function
async def main():
    motion_sensor.set_yaw_face(YAW_FACE)
    motion_sensor.reset_yaw(0)
    motor_pair.pair(MOTOR_PAIR, FIRST_MOTOR_PORT, SECOND_MOTOR_PORT)

    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_UP_ANGLE, 180, direction=motor.SHORTEST_PATH)

    await go_to_a_certain_distance(10)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 145, 0, velocity=DEFAULT_VELOCITY)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 180, direction=motor.SHORTEST_PATH)
    await microadjustment()
    center_color = await read_color_with_depth(DEFAULT_SENSOR_COLOR_DEPTH, PRIMARY_SENSOR_COLOR_PORT)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_POLUENTE, 180, direction=motor.SHORTEST_PATH)
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, -605, 0, velocity=DEFAULT_VELOCITY)
    await turn(90)
    await microadjustment(90)
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 350, 0, velocity=DEFAULT_VELOCITY)
    await go_to_a_certain_distance(10)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 95, 0, velocity=DEFAULT_VELOCITY)
    await do_pollutant_mission(center_color)

    return
    power_off()

# pollutant mission

async def do_pollutant_mission(center_color):
    for i in range(0, 8):
        direction = 1 if i < 4 else -1
        print("{}. poluente:".format(i))
        
        if i == 7:
            await kill_pollutant_if_necessary(center_color, direction)
        elif i == 3:
            await pollutant_mission_route_going_from_one_side_to_the_other(center_color, direction)
        else:
            await pollutant_mission_standard_route(center_color, direction)

async def pollutant_mission_route_going_from_one_side_to_the_other(center_color, direction):
    await microadjustment()
    await kill_pollutant_if_necessary(center_color, direction)
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, -200, 0, velocity=DEFAULT_VELOCITY)
    await turn(90)
    await microadjustment(90)
    motion_sensor.reset_yaw(0)
    await turn(90)
    await microadjustment(90)
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 600, 0, velocity=DEFAULT_VELOCITY)
    await microadjustment()
    await go_to_a_certain_distance(10)
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, 100, 0, velocity=DEFAULT_VELOCITY)

async def pollutant_mission_standard_route(center_color, direction): #
    await microadjustment()
    await kill_pollutant_if_necessary(center_color, direction)
    await turn(-90)
    await microadjustment(-90)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 518, 0, velocity=DEFAULT_VELOCITY)
    await turn(90)
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, 70, 0, velocity=DEFAULT_VELOCITY)


# useful functions for pollutant mission

async def go_to_pollutant():
    await microadjustment()
    await go_to_a_certain_distance(MIN_DISTANCE_TO_POLLUTANT)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 50, 0, velocity=DEFAULT_VELOCITY)
    await microadjustment()

async def kill_pollutant_if_necessary(center_color, direction):
    await microadjustment()
    pollutant_color = await read_color_with_depth(10, SECONDARY_SENSOR_COLOR_PORT)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -70, 0, velocity=DEFAULT_VELOCITY)

    if pollutant_color == center_color:
        await turn(50 * direction)
        await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_POLUENTE_DERRUBAR, 180, direction=motor.SHORTEST_PATH)
        await runloop.sleep_ms(100)
        await turn(-35 * direction)
        await turn(35 * direction)
        await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_POLUENTE, 180, direction=motor.SHORTEST_PATH)
        await turn(-50 * direction)

    await microadjustment()

# useful functions

async def go_to_a_certain_distance(distance, inverse=False):
    if not inverse:
        motor_pair.move(MOTOR_PAIR, 0, velocity=180)
        await runloop.until(lambda: get_distance() < distance)
        motor_pair.stop(MOTOR_PAIR)
    else:
        motor_pair.move(MOTOR_PAIR, 0, velocity=-180)
        await runloop.until(lambda: get_distance() > distance)
        motor_pair.stop(MOTOR_PAIR)

async def turn(degrees, velocity=360):
    mov_degrees = int((MOTOR_DEGREES_TO_TURN_90_DEGREES * degrees) / 90)
    await motor_pair.move_for_degrees(MOTOR_PAIR, mov_degrees, 100, velocity=velocity)

async def microadjustment(angle = 0):
    if get_yaw_angle() == angle:
        return

    for _ in range(0, MICROADJUSTMENT_DEPTH - 1):
        await turn(angle - abs(get_yaw_angle()) if angle == 180 else angle - get_yaw_angle())

# sensor facilitating functions

def get_yaw_angle():
    return motion_sensor.tilt_angles()[0] / 10 * -1

def get_distance(depth=10):
    distance = distance_sensor.distance(DISTANCE_SENSOR_PORT) / 10

    if depth != 0 and distance == -0.1:
        return get_distance(depth - 1)

    return distance

async def read_color_with_depth(depth=DEFAULT_SENSOR_COLOR_DEPTH, sensor=PRIMARY_SENSOR_COLOR_PORT):
    color = color_sensor.color(sensor)

    if color == 9:
        light_matrix.write("V")
        return "Vermelho"
    if depth == 0:
        light_matrix.write("P")
        return "Preto"
    return await read_color_with_depth(depth - 1)

# run main function
runloop.run(main())
