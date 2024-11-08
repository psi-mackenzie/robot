from hub import light_matrix, port, motion_sensor, power_off
import color_sensor
import motor_pair
import runloop
import distance_sensor

async def main():  
    motion_sensor.set_yaw_face(motion_sensor.TOP)
    motion_sensor.reset_yaw(0)
    motor_pair.pair(motor_pair.PAIR_1, port.F, port.E)

    center_color = 0

    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 920, 0, velocity=540)
    await turn(91)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 1200, 0, velocity=570)
    await microajuste(90)
    await runloop.sleep_ms(100)
    motion_sensor.reset_yaw(0)
    await microajuste()

    dis = distance()
    await turn(180)
    await microajuste(180, 15)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -int(28 * dis) - 45, 0, velocity=540)
    await runloop.sleep_ms(250)
    center_color = await color(50, port.B)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 150, 0, velocity=540)
    await microajuste(180, 10)
    await runloop.sleep_ms(250)
    print("A cor do centro identicada foi {}".format(center_color))

    for i in range(0, 8):
        direction = 1 if i < 4 else -1
        print("{}. poluente:".format(i))

        if i == 0:
            await motor_pair.move_for_degrees(motor_pair.PAIR_1, 504, 0, velocity=540)
            await microajuste(180, 15)
            await turn(-90)
            await microajuste(90, 15)
            motion_sensor.reset_yaw(0)
            await runloop.sleep_ms(100)
            await go_to_pollutant()
            await do_pollutant_mission(center_color, direction)
        elif i == 4:
            await microajuste()
            await motor_pair.move_for_degrees(motor_pair.PAIR_1, -405, 0, velocity=540)
            await turn(180)
            await microajuste(180, 15)
            await runloop.sleep_ms(100)
            motion_sensor.reset_yaw(0)
            await motor_pair.move_for_degrees(motor_pair.PAIR_1, 100, 0, velocity=540)
            await microajuste(180, 15)
            await go_to_pollutant()
            await do_pollutant_mission(center_color, direction)
            motion_sensor.reset_yaw(0)
        else:
            await microajuste()
            await motor_pair.move_for_degrees(motor_pair.PAIR_1, -55, 0, velocity=540)
            await turn(-90)
            await microajuste(-90)
            await motor_pair.move_for_degrees(motor_pair.PAIR_1, 519, 0, velocity=540)
            await turn(90)
            await microajuste()
            await go_to_pollutant()
            await do_pollutant_mission(center_color, direction)
            motion_sensor.reset_yaw(0)

    return
    power_off()

async def do_pollutant_mission(center_color, k):
    await runloop.sleep_ms(100)
    await microajuste()
    pollutant_color = await color()
    print("A cor do poluente identicada foi {}".format(pollutant_color))

    if pollutant_color == center_color:
        await turn(-27 * k, 500)
        await runloop.sleep_ms(100)
        await turn(27 * k, 500)

    await microajuste()

def angle():
    return motion_sensor.tilt_angles()[0] / 10

def distance():
    return distance_sensor.distance(port.C) / 10

async def color(depth=20, sensor=port.D):
    c = color_sensor.color(sensor)

    if c == 9:
        light_matrix.show_image(light_matrix.IMAGE_HAPPY)
        return "Vermelho"
    else:
        if depth == 0 or c == 0:
            light_matrix.show_image(light_matrix.IMAGE_GHOST)
            return "Preto"
        else:
            await runloop.sleep_ms(10)
            return await color(depth - 1)

async def turn(degrees, velocity=360):
    await runloop.sleep_ms(100)
    mov_degrees = int((214 * degrees) / 90)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, mov_degrees, 100, velocity=velocity)

async def go_to_pollutant():
    await microajuste()
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=540)
    await runloop.until(lambda: distance() < 4.7)
    motor_pair.stop(motor_pair.PAIR_1)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 45, 0, velocity=540)
    await microajuste()

async def microajuste(ang = 0, depth = 5):
    for _ in range(0, depth - 1):
        if ang == 180:
            await runloop.sleep_ms(50)
            if angle() == 0:
                print("bro")
                break
            elif angle() < 0:
                await turn(angle() + 180)
            else:
                await turn(angle() - 180)
        else:
            await runloop.sleep_ms(50)
            await turn(ang + angle())


runloop.run(main())
