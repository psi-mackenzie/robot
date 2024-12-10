
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
CLAW_TOTALLY_UP_ANGLE = 348
CLAW_TOTALLY_DOWN_ANGLE = 68
CLAW_ARVORE_GRANDE_PEGAR = 61
CLAW_POLUENTE = 1
CLAW_POLUENTE_DERRUBAR = 41
PONTO_PERFEITO = 359
PONTO_PERFEITO_PEQUENO = 354
CLAW_LINHA = 69

PRIMARY_SENSOR_COLOR_PORT = port.E
SECONDARY_SENSOR_COLOR_PORT = port.A
DISTANCE_SENSOR_PORT = port.B

DEFAULT_VELOCITY = 540

MIN_DISTANCE_TO_POLLUTANT = 4.7
DEGREES_TO_KILL_POLLUTANT = 30
MOTOR_DEGREES_TO_TURN_90_DEGREES = 219
MICROADJUSTMENT_DEPTH = 20
SENSOR_COLOR_DEPTH = 25

# main function
async def main():
    motion_sensor.set_yaw_face(YAW_FACE)
    motion_sensor.reset_yaw(0)
    motor_pair.pair(MOTOR_PAIR, FIRST_MOTOR_PORT, SECOND_MOTOR_PORT)

    is_primary_route = await prepare_for_first_tree()
    await do_first_tree(is_primary_route)

    center_color = await prepare_for_pollutant_mission()
    await do_pollutant_mission(center_color)

    is_primary_route = await prepare_for_second_tree()
    await do_second_tree(is_primary_route)

    return
    power_off()

# first tree mission

async def prepare_for_first_tree():
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_UP_ANGLE, 180, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 1165, 0, velocity=DEFAULT_VELOCITY)
    await microadjustment()
    await turn(-93)
    await microadjustment(-93)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -45, 0, velocity=DEFAULT_VELOCITY)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, 15, 180, direction=motor.SHORTEST_PATH)
    await runloop.sleep_ms(500)
    is_primary_route = await read_color_with_depth(75, PRIMARY_SENSOR_COLOR_PORT) == "Verde"
    await motor_pair.move_for_degrees(MOTOR_PAIR, -170, 0, velocity=DEFAULT_VELOCITY)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 180, direction=motor.SHORTEST_PATH)
    return is_primary_route

async def do_first_tree(is_primary_route):
    if is_primary_route:
        await do_first_tree_primary_route()
        return

    await do_first_tree_secondary_route()

async def do_first_tree_primary_route():
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_ARVORE_GRANDE_PEGAR, 180, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 175, 0, velocity=120)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, PONTO_PERFEITO, 180, direction=motor.SHORTEST_PATH)
    await microadjustment(-90)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -220, 0, velocity=DEFAULT_VELOCITY)
    await turn(90)
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, 130, 0, velocity=540)
    await go_to_a_certain_distance(10.1, velocity=180)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 90, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -132, 0, velocity=DEFAULT_VELOCITY)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_UP_ANGLE, 90, direction=motor.SHORTEST_PATH)
    await motor.run_for_degrees(SECOND_MOTOR_PORT, 421, 540)
    await microadjustment(-93)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 90, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 245, 0, velocity=120)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, PONTO_PERFEITO_PEQUENO, 180, direction=motor.SHORTEST_PATH)
    await microadjustment(-90)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -170, 0, velocity=DEFAULT_VELOCITY)
    await turn(90)
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, 50, 0, velocity=DEFAULT_VELOCITY)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 90, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -150, 0, velocity=DEFAULT_VELOCITY)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_UP_ANGLE, 90, direction=motor.SHORTEST_PATH)
    await go_to_a_certain_distance(18, inverse=True, velocity=180)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -370, 0, velocity=DEFAULT_VELOCITY)
    await turn(-90)
    await microadjustment(-90)
    motion_sensor.reset_yaw(0)

async def do_first_tree_secondary_route():
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 180, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 345, 0, velocity=120)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, PONTO_PERFEITO_PEQUENO, 180, direction=motor.SHORTEST_PATH)
    await microadjustment(-90)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -165, 0, velocity=DEFAULT_VELOCITY)
    await turn(90)
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, 100, 0, velocity=540)
    await go_to_a_certain_distance(10.1, velocity=180)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 20, 0, velocity=540)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 90, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -157, 0, velocity=DEFAULT_VELOCITY)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_UP_ANGLE, 90, direction=motor.SHORTEST_PATH)
    await motor.run_for_degrees(SECOND_MOTOR_PORT, 421, 540)
    await microadjustment(-94)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -240, 0, velocity=120)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 90, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 260, 0, velocity=120)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, PONTO_PERFEITO, 180, direction=motor.SHORTEST_PATH)
    await microadjustment(-90)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -390, 0, velocity=DEFAULT_VELOCITY)
    await turn(90)
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, -10, 0, velocity=DEFAULT_VELOCITY)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 90, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -120, 0, velocity=DEFAULT_VELOCITY)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_UP_ANGLE, 90, direction=motor.SHORTEST_PATH)
    await go_to_a_certain_distance(18, inverse=True, velocity=180)
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, -400, 0, velocity=DEFAULT_VELOCITY)
    await turn(-90)
    await microadjustment(-90)
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 200, 0, velocity=DEFAULT_VELOCITY)

# pollutant mission

async def prepare_for_pollutant_mission():
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 180, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -875, 0, velocity=DEFAULT_VELOCITY * 4)

    for i in range(0, 8):
        await motor_pair.move_for_degrees(MOTOR_PAIR, -50, 25 * (1 if i % 2 == 0 else -1), velocity=DEFAULT_VELOCITY * 2)

    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_UP_ANGLE, 180, direction=motor.SHORTEST_PATH)
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, -200, 0, velocity=DEFAULT_VELOCITY)
    await microadjustment()
    await turn(-90)
    await microadjustment(-90)
    motion_sensor.reset_yaw(0)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_LINHA, 180, direction=motor.SHORTEST_PATH)
    motor_pair.move(MOTOR_PAIR, 0, velocity=-90)
    await runloop.until(lambda: color_sensor.color(PRIMARY_SENSOR_COLOR_PORT) == 0)
    motor_pair.stop(MOTOR_PAIR)

    await motor_pair.move_for_degrees(MOTOR_PAIR, 120, 0, velocity=DEFAULT_VELOCITY)
    await turn(-90)
    await microadjustment(-90)
    motion_sensor.reset_yaw(0)

    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_UP_ANGLE, 180, direction=motor.SHORTEST_PATH)
    await go_to_a_certain_distance(9, velocity=180)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 85, 0, velocity=DEFAULT_VELOCITY)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 180, direction=motor.SHORTEST_PATH)
    center_color = await read_color_with_depth(SENSOR_COLOR_DEPTH, PRIMARY_SENSOR_COLOR_PORT)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_POLUENTE, 180, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -540, 0, velocity=DEFAULT_VELOCITY)
    await microadjustment()
    await turn(90)
    await microadjustment(90)
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 350, 0, velocity=DEFAULT_VELOCITY)
    await go_to_a_certain_distance(8, velocity=180)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 15, 0, velocity=DEFAULT_VELOCITY)
    await microadjustment()
    return center_color

async def do_pollutant_mission(center_color):
    count = 0

    for i in range(0, 8):
        direction = 1 if i < 4 else -1
        print("{}. poluente:".format(i + 1))
        print("Distance: {}".format(get_distance()))
        count += await kill_pollutant_if_necessary(center_color, direction, count)

        if count == 4 or i == 7:
            await go_to_last_ramp(i)
            break

        if i == 3:
            await go_to_next_pollutant_on_another_side()
        else:
            await go_to_next_pollutant()

async def go_to_next_pollutant_on_another_side():
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, -500, 0, velocity=DEFAULT_VELOCITY)
    await turn(90)
    await microadjustment(90)
    motion_sensor.reset_yaw(0)
    await turn(45)
    await microadjustment(45)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 100, 0, velocity=DEFAULT_VELOCITY)
    await microadjustment(45)
    await turn(45)
    await microadjustment(90)
    motion_sensor.reset_yaw(0)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 85, 0, velocity=DEFAULT_VELOCITY)
    await go_to_a_certain_distance(8, velocity=180)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 5, 0, velocity=DEFAULT_VELOCITY)
    await microadjustment()

async def go_to_next_pollutant():
    await microadjustment()
    await turn(-90)
    await microadjustment(-90)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 507, 0, velocity=DEFAULT_VELOCITY)
    await turn(90)
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, 70, 0, velocity=DEFAULT_VELOCITY)

# useful functions for pollutant mission

async def kill_pollutant_if_necessary(center_color, direction, count):
    pollutant_color = await read_color_with_depth(10, SECONDARY_SENSOR_COLOR_PORT)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -70, 0, velocity=DEFAULT_VELOCITY)

    if pollutant_color == center_color:
        await turn(50 * direction)
        await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_POLUENTE_DERRUBAR, 180, direction=motor.SHORTEST_PATH)
        await runloop.sleep_ms(100)
        await turn(-40 * direction)
        await turn(40 * direction)
        await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_POLUENTE, 180, direction=motor.SHORTEST_PATH)
        await turn(-50 * direction)
        print("Killed!")
        await microadjustment()
        return 1

    return 0

# second and third tree mission

async def go_to_last_ramp(pollutant_index):
    if pollutant_index == 3:
        await motor_pair.move_for_degrees(MOTOR_PAIR, -300, 0, velocity=DEFAULT_VELOCITY)
        await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_LINHA, 180, direction=motor.SHORTEST_PATH)
        motor_pair.move(MOTOR_PAIR, 0, velocity=-90)
        await runloop.until(lambda: color_sensor.color(PRIMARY_SENSOR_COLOR_PORT) == 0)
        motor_pair.stop(MOTOR_PAIR)
        await motor_pair.move_for_degrees(MOTOR_PAIR, 90, 0, velocity=DEFAULT_VELOCITY)
    else:
        await motor_pair.move_for_degrees(MOTOR_PAIR, -50, 0, velocity=DEFAULT_VELOCITY)
        await turn(90)
        await microadjustment(90)
        motion_sensor.reset_yaw(0)
        await motor_pair.move_for_degrees(MOTOR_PAIR, 507 * (pollutant_index - 4) , 0, velocity=DEFAULT_VELOCITY)
        await turn(90)
        await microadjustment(90)
        motion_sensor.reset_yaw(0)
        await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_LINHA, 180, direction=motor.SHORTEST_PATH)
        motor_pair.move(MOTOR_PAIR, 0, velocity=90)
        await runloop.until(lambda: color_sensor.color(PRIMARY_SENSOR_COLOR_PORT) == 0)
        motor_pair.stop(MOTOR_PAIR)
        await motor_pair.move_for_degrees(MOTOR_PAIR, 90, 0, velocity=DEFAULT_VELOCITY)


    await turn(90)
    await microadjustment(90)
    motion_sensor.reset_yaw(0)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 180, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -875, 0, velocity=DEFAULT_VELOCITY * 4)

    for i in range(0, 4):
        await motor_pair.move_for_degrees(MOTOR_PAIR, -50, 25 * (1 if i % 2 == 0 else -1), velocity=DEFAULT_VELOCITY * 2)

    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_UP_ANGLE, 180, direction=motor.SHORTEST_PATH)
    await microadjustment()

async def prepare_for_second_tree():
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_LINHA, 180, direction=motor.SHORTEST_PATH)

    motor_pair.move(MOTOR_PAIR, 0, velocity=-90)
    await runloop.until(lambda: color_sensor.color(PRIMARY_SENSOR_COLOR_PORT) == 0)
    motor_pair.stop(MOTOR_PAIR)

    motor_pair.move(MOTOR_PAIR, 0, velocity=-90)
    await runloop.until(lambda: color_sensor.color(PRIMARY_SENSOR_COLOR_PORT) == 10)
    motor_pair.stop(MOTOR_PAIR)

    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_UP_ANGLE, 180, direction=motor.SHORTEST_PATH)
    await turn(-90)
    await microadjustment(-90)
    motion_sensor.reset_yaw(0)
    await go_to_a_certain_distance(19, velocity=180)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -90, 0, velocity=DEFAULT_VELOCITY)
    await turn(-94)
    await microadjustment(-94)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -45, 0, velocity=DEFAULT_VELOCITY)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, 15, 180, direction=motor.SHORTEST_PATH)
    await runloop.sleep_ms(500)
    is_primary_route = await read_color_with_depth(75, PRIMARY_SENSOR_COLOR_PORT) == "Verde"
    await motor_pair.move_for_degrees(MOTOR_PAIR, -170, 0, velocity=DEFAULT_VELOCITY)
    return is_primary_route

async def do_second_tree(is_primary_route):
    if is_primary_route:
        await do_second_tree_primary_route()
        return

    await do_second_tree_secondary_route()

async def do_second_tree_primary_route():
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_ARVORE_GRANDE_PEGAR, 180, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 175, 0, velocity=120)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, PONTO_PERFEITO, 180, direction=motor.SHORTEST_PATH)
    await microadjustment(-90)
    await turn(90)
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, 100, 0, velocity=540)
    await go_to_a_certain_distance(10.1, velocity=180)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 90, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -150, 0, velocity=DEFAULT_VELOCITY)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_UP_ANGLE, 90, direction=motor.SHORTEST_PATH)
    await motor.run_for_degrees(SECOND_MOTOR_PORT, 421, 540)
    await microadjustment(-94)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -240, 0, velocity=DEFAULT_VELOCITY)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 90, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 265, 0, velocity=120)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, PONTO_PERFEITO_PEQUENO, 180, direction=motor.SHORTEST_PATH)
    await microadjustment(-90)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -330, 0, velocity=DEFAULT_VELOCITY)
    await turn(90)
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, 50, 0, velocity=DEFAULT_VELOCITY)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 90, direction=motor.SHORTEST_PATH)

async def do_second_tree_secondary_route():
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 180, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 230, 0, velocity=120)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, PONTO_PERFEITO_PEQUENO, 180, direction=motor.SHORTEST_PATH)
    await microadjustment(-90)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -185, 0, velocity=DEFAULT_VELOCITY)
    await turn(90)
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, 100, 0, velocity=540)
    await go_to_a_certain_distance(10.1, velocity=180)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 90, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -156, 0, velocity=DEFAULT_VELOCITY)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_UP_ANGLE, 90, direction=motor.SHORTEST_PATH)
    await motor.run_for_degrees(SECOND_MOTOR_PORT, 421, 540)
    await microadjustment(-94)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -200, 0, velocity=120)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 90, direction=motor.SHORTEST_PATH)
    await motor_pair.move_for_degrees(MOTOR_PAIR, 240, 0, velocity=120)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, PONTO_PERFEITO, 180, direction=motor.SHORTEST_PATH)
    await microadjustment(-90)
    await motor_pair.move_for_degrees(MOTOR_PAIR, -10, 0, velocity=DEFAULT_VELOCITY)
    await turn(90)
    await microadjustment()
    await motor_pair.move_for_degrees(MOTOR_PAIR, -10, 0, velocity=DEFAULT_VELOCITY)
    await motor.run_to_absolute_position(CLAW_MOTOR_PORT, CLAW_TOTALLY_DOWN_ANGLE, 90, direction=motor.SHORTEST_PATH)

# useful functions

async def go_to_a_certain_distance(distance, inverse=False, velocity=360):
    if not inverse:
        motor_pair.move(MOTOR_PAIR, 0, velocity=velocity)
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

async def read_color_with_depth(depth=SENSOR_COLOR_DEPTH, sensor=PRIMARY_SENSOR_COLOR_PORT):
    color = color_sensor.color(sensor)

    if color == 9:
        light_matrix.write("V")
        return "Vermelho"
    elif color == 6:
        return "Verde"
 
    if depth == 0:
        light_matrix.write("P")
        return "Preto"
    return await read_color_with_depth(depth - 1)

# run main function
runloop.run(main())
