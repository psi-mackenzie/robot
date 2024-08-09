from hub import light_matrix, port
import color_sensor
import motor
import motor_pair
import runloop
import distance_sensor

debug_mode = True

# Main function
async def main():
    motor_pair.pair(motor_pair.PAIR_1, port.F, port.E) # Definir o Par de Motores 1 para F e E

    center_color = 0 # Definir varíavel para representar a cor do centro da mesa

    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 890, 0, velocity=360)           # Mover para frente até a rampa
    await turn(90)                                                                       # Girar 90 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 1000, 0, velocity=360)

    motor_pair.move(motor_pair.PAIR_1, 0, velocity=360)
    await runloop.until(lambda: distance_sensor.distance(port.D) < 250)
    motor_pair.stop(motor_pair.PAIR_1)

    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 550, 0, velocity=360)

    await runloop.sleep_ms(500) # Esperar 500 milissegundos
    center_color = see_color()  # Ver a cor do centro
    await debug("A cor do centro identicada foi {}".format(center_color), center_color[0])

    # Reposicionar o robô para fazer o primeiro poluente
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -485, 0, velocity=360) # Voltar até o primeiro poluente
    await turn(90)                                                              # Girar 90 graus para direita

    motor_pair.move(motor_pair.PAIR_1, 0, velocity=360)
    await runloop.until(lambda: distance_sensor.distance(port.D) < 45)
    motor_pair.stop(motor_pair.PAIR_1)

    motor_pair.move_for_degrees(motor_pair.PAIR_1, 55, 0, velocity=360)

    print("Primeiro poluente:")
    await do_pollutant_mission(center_color, 1) # Fazer a missão

    # Reposiocionar para o segundo poluente
    await runloop.sleep_ms(500)                                                 # Esperar 500 milissegundos
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -340, 0, velocity=360) # Ir para trás até +/- o centro
    await turn(180)                                                             # Girar 180 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 315, 0, velocity=360)

    print("Segundo poluente:")
    await do_pollutant_mission(center_color, -1) # Fazer a missão

    # Reposiocionar para o terceiro poluente
    await runloop.sleep_ms(500)                                                # Esperar 500 milissegundos
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -60, 0, velocity=360) # Ir um pouco para trás
    await turn(90)                                                             # Girar 90 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 515, 0, velocity=360) # Ir para frente até o terceiro poluente
    await turn(-90)                                                            # Girar 90 graus para esquerda
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 60, 0, velocity=360)  # Posicionar o robô para a missão

    print("Terceiro poluente:")
    await do_pollutant_mission(center_color, -1) # Fazer a missão

    # Reposicionar o robô para o quarto poluente
    await runloop.sleep_ms(500)                                                 # Esperar 500 milissegundos
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -60, 0, velocity=360)  # Ir um pouco para trás
    await turn(45)                                                              # Girar 45 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 105, 0, velocity=360)  # Ir mediamente para frente
    await turn(45)                                                              # Girar 45 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 605, 0, velocity=360) # Ir mediamente para frente
    await motor.run_for_degrees(port.F, 528, 360)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 135, 0, velocity=360)


    print("Quarto poluente:")
    await do_pollutant_mission(center_color, -1) # Fazer a missão

    # Reposicionar o robô para o quinto poluente
    await runloop.sleep_ms(500)                                                # Esperar 500 milissegundos
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -70, 0, velocity=360) # Ir um pouco para trás
    await turn(90)                                                             # Girar 90 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 500, 0, velocity=360) # Ir para a frente até o quinto poluente
    await turn(-90)                                                            # Girar 90 graus para esquerda
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 60, 0, velocity=360)  # Posicionar o robô para a missão

    print("Quinto poluente:")
    await do_pollutant_mission(center_color, -1) # Fazer a missão

    # Reposicionar o robô para o sexto poluente
    await runloop.sleep_ms(500)                                                # Esperar 500 milissegundos
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -340, 0, velocity=360) # Ir para trás até +/- o centro
    await turn(180)                                                            # Girar 180 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 315, 0, velocity=360)

    print("Sexto poluente:")
    await do_pollutant_mission(center_color, 1) # Fazer a missão

    # Reposicionar o robô para o sétimo poluente
    await runloop.sleep_ms(500)                                                # Esperar 500 milissegundos
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -60, 0, velocity=360) # Ir um pouco para trás
    await turn(90)                                                            # Girar 90 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 515, 0, velocity=360) # Ir para frente até o terceiro poluente
    await turn(-90)                                                            # Girar 90 graus para esquerda
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 60, 0, velocity=360)# Posicionar o robô para a missão

    print("Sétimo poluente:")
    await do_pollutant_mission(center_color, 1) # Fazer a missão


    # Reposicionar o robô para o oitavo poluente
    await runloop.sleep_ms(500)                                                # Esperar 500 milissegundos
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, -60, 0, velocity=360)# Ir um pouco para trás
    await turn(45)                                                            # Girar 45 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 105, 0, velocity=360)# Ir mediamente para frente
    await turn(45)                                                            # Girar 45 graus para direita
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 605, 0, velocity=360) # Ir mediamente para frente
    await motor.run_for_degrees(port.F, 528, 360)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, 155, 0, velocity=360)

    print("Oitavo poluente:")
    await do_pollutant_mission(center_color, 1) # Fazer a missão

async def do_pollutant_mission(center_color, k):
    await runloop.sleep_ms(500) # Esperar 500 milissegundos
    pollutant_color = see_color() # Ver a cor do sensor
    await debug("A cor do poluente identicada foi {}".format(pollutant_color), pollutant_color[0])

    if pollutant_color == center_color:
        # Derrubando o poluente
        await debug("A cor do poluente é a mesma que a do centro", "=")
        await turn(-30 * k)         # Girar 30 graus para esquerda (ou o inverso, depende do k)
        await runloop.sleep_ms(250) # Esperar 250 milissegundos
        await turn(30 * k)          # Girar 30 graus para direita (ou o inverso, depende do k)
    else:
        await debug("A cor do poluente não é a mesma que a do centro", "D")

async def debug(message, spike_message):
    print(message) # Printando a mensagem no console
    if debug_mode: # Se o debug mode estiver ativo, mostrar no robô
        light_matrix.write(spike_message) # Mostrando no robô
        await runloop.sleep_ms(500)       # Esperar 500 milissegundos
        light_matrix.clear()              # Limpando a tela do robô

def see_color():
    color = color_sensor.color(port.A) # Ver a cor do sensor
    # Retornando um texto, dependendo do número retornado
    if color == 9:
        return "Vermelho"
    else:
        return "Preto"

async def turn(degrees):
    # O descoberto foi que 285 de ângulo faz o robô girar 90 graus
    # Nesse caso é só fazer a regra de três para o quanto é necessário para outros ângulos
    mov_degrees = int((263 * degrees) / 90)                                                   # Regra de três (já simplificada)
    await motor_pair.move_for_degrees(motor_pair.PAIR_1, mov_degrees, 100, velocity=360) # Movendo o robô

runloop.run(main()) # Rodando a função principal
