from hub import light_matrix, port, motion_sensor
import color_sensor
import motor
import motor_pair
import runloop
import distance_sensor

# Main function
async def main():
    motion_sensor.set_yaw_face(motion_sensor.TOP)
    motion_sensor.reset_yaw(0)
    motor_pair.pair(motor_pair.PAIR_1, port.D, port.C) # Definir o Par de Motores 1 para F e E

    center_color = 0 # Definir varíavel para representar a cor do centro da mesa

    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 960, 0, velocity=360)        # Mover para frente até a rampa
    await turn(90)
    motion_sensor.reset_yaw(0)                                                            # Girar 90 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 1200, 0, velocity=700)
    await runloop.sleep_ms(100)

    await turn(angle())

    dis = distance()
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, int(22 * dis), 0, velocity=360)

    await runloop.sleep_ms(250) # Esperar 500 milissegundos
    center_color = color()# Ver a cor do centro
    print("A cor do centro identicada foi {}".format(center_color))

    print("Primeiro poluente:")
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=-360) # Voltar até o primeiro poluente
    await runloop.until(lambda: distance() > 21)
    motor_pair.stop(motor_pair.PAIR_1)
    await turn(90)                                                            # Girar 90 graus para direita
    motion_sensor.reset_yaw(0)                                                            # Girar 90 graus para direita
    await runloop.sleep_ms(100)
    await go_to_pollutant()
    await do_pollutant_mission(center_color, 1) # Fazer a missão

    print("Segundo poluente:")
    await runloop.sleep_ms(100)                                                # Esperar 500 milissegundos
    await go_not_to_pollutant()
    await turn(-90)                                                            # Girar 90 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 515, 0, velocity=360) # Ir para frente até o terceiro poluente
    await turn(90)                                                            # Girar 90 graus para esquerda
    await go_to_pollutant()
    await do_pollutant_mission(center_color, 1) # Fazer a missão
    motion_sensor.reset_yaw(0)

    print("Terceiro poluente:")
    await runloop.sleep_ms(100)                                                # Esperar 500 milissegundos
    await go_not_to_pollutant()
    await turn(-45)                                                            # Girar 45 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 105, 0, velocity=360)# Ir mediamente para frente
    await turn(-45)                                                            # Girar 45 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 605, 0, velocity=360) # Ir mediamente para frente
    await motor.run_for_degrees(port.C, -528, 360)
    await turn(angle())
    await go_to_pollutant()
    await do_pollutant_mission(center_color, 1) # Fazer a missão
    motion_sensor.reset_yaw(0)

    print("Quarto poluente:")
    await runloop.sleep_ms(100)                                                # Esperar 500 milissegundos
    await go_not_to_pollutant()
    await turn(-90)                                                            # Girar 90 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 525, 0, velocity=360) # Ir para a frente até o quinto poluente
    await turn(90)                                                            # Girar 90 graus para esquerda
    await go_to_pollutant()
    await do_pollutant_mission(center_color, 1) # Fazer a missão
    motion_sensor.reset_yaw(0)

    print("Quinto poluente:")
    await runloop.sleep_ms(100)                                                # Esperar 500 milissegundos
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -380, 0, velocity=360) # Ir para trás até +/- o centro
    await turn(178)                                                           # Girar 180 graus para direita
    await runloop.sleep_ms(100)
    motion_sensor.reset_yaw(0)
    await go_to_pollutant()
    await do_pollutant_mission(center_color, -1) # Fazer a missão
    motion_sensor.reset_yaw(0)

    print("Sexto poluente:")
    await runloop.sleep_ms(100)                                                # Esperar 500 milissegundos
    await go_not_to_pollutant()
    await turn(-90)                                                            # Girar 90 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 525, 0, velocity=360) # Ir para frente até o terceiro poluente
    await turn(90)                                                            # Girar 90 graus para esquerda
    await go_to_pollutant()
    await do_pollutant_mission(center_color, -1) # Fazer a missão
    motion_sensor.reset_yaw(0)

    print("Sétimo poluente:")
    await runloop.sleep_ms(100)                                                # Esperar 500 milissegundos
    await go_not_to_pollutant()
    await turn(-45)                                                            # Girar 45 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 105, 0, velocity=360)# Ir mediamente para frente
    await turn(-45)                                                            # Girar 45 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 605, 0, velocity=360) # Ir mediamente para frente
    await motor.run_for_degrees(port.C, -528, 360)
    await turn(angle())
    await go_to_pollutant()
    await do_pollutant_mission(center_color, -1) # Fazer a missão
    motion_sensor.reset_yaw(0)

    print("Oitavo poluente:")
    await runloop.sleep_ms(100)                                                # Esperar 500 milissegundos
    await go_not_to_pollutant()
    await turn(-90)                                                            # Girar 90 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 525, 0, velocity=360) # Ir para a frente até o quinto poluente
    await turn(90)                                                            # Girar 90 graus para esquerda
    await go_to_pollutant()
    await do_pollutant_mission(center_color, -1) # Fazer a missão
    motion_sensor.reset_yaw(0)

async def do_pollutant_mission(center_color, k):
    await turn(angle())
    await runloop.sleep_ms(100) # Esperar 500 milissegundos
    pollutant_color = color() # Ver a cor do sensor
    print("A cor do poluente identicada foi {}".format(pollutant_color))

    if pollutant_color == center_color:
        await turn(-25 * k)        # Girar 30 graus para esquerda (ou o inverso, depende do k)
        await runloop.sleep_ms(100) # Esperar 250 milissegundos
        await turn(25 * k)        # Girar 30 graus para direita (ou o inverso, depende do k)
    
    await turn(angle())

def angle():
    return motion_sensor.tilt_angles()[0] / 10

def distance():
    return distance_sensor.distance(port.F) / 10

def color():
    color = color_sensor.color(port.E) # Ver a cor do sensor
    # Retornando um texto, dependendo do número retornado
    if color == 9:
        return "Vermelho"
    else:
        return "Preto"

async def turn(degrees):
    # O descoberto foi que 285 de ângulo faz o robô girar 90 graus
    # Nesse caso é só fazer a regra de três para o quanto é necessário para outros ângulos
    mov_degrees = int((272 * degrees) / 90)                                                # Regra de três (já simplificada)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, mov_degrees, 100, velocity=480) # Movendo o robô

async def go_to_pollutant():
    motor_pair.move(motor_pair.PAIR_1, 0, velocity=360)
    await runloop.until(lambda: distance() < 4.7)
    motor_pair.stop(motor_pair.PAIR_1)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 55, 0, velocity=360)

async def go_not_to_pollutant():
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -75, 0, velocity=360)

runloop.run(main()) # Rodando a função principal
