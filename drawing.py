import cv2
import mediapipe as mp
import numpy as np

# Inicializando MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Inicializando a captura de vídeo da webcam
cap = cv2.VideoCapture(0)

# Definindo uma tela preta para desenhar
canvas = None
x, y = 0, 0
drawing = False
color = (0, 255, 0)  # Cor inicial (verde)
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0)]  # Azul, Verde, Vermelho, Amarelo, Rosa, Ciano

# Função para desenhar quadrados de seleção de cor
def draw_color_boxes(frame):
    for i, c in enumerate(colors):
        cv2.rectangle(frame, (i * 60, 0), (i * 60 + 60, 60), c, -1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Espelhando a imagem
    frame = cv2.flip(frame, 1)

    # Convertendo a imagem para RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Processando a imagem com MediaPipe
    result = hands.process(rgb_frame)

    # Inicializando o canvas na primeira iteração
    if canvas is None:
        canvas = np.zeros_like(frame)

    # Desenhando os quadrados de seleção de cor
    draw_color_boxes(frame)

    # Verificando se há alguma mão detectada
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            # Desenhando os pontos da mão
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Coordenadas do dedo indicador (ponto 8)
            x_new = int(hand_landmarks.landmark[8].x * frame.shape[1])
            y_new = int(hand_landmarks.landmark[8].y * frame.shape[0])

            # Verificando se o dedo indicador toca um quadrado de cor
            if y_new < 60:  # Altura dos quadrados de seleção de cor
                for i in range(len(colors)):
                    if i * 60 < x_new < i * 60 + 60:
                        color = colors[i]  # Atualizando a cor de desenho

            # Coordenadas do polegar (ponto 4)
            thumb_tip = hand_landmarks.landmark[4]
            thumb_up = thumb_tip.y < hand_landmarks.landmark[2].y  # Verifica se o polegar está levantado

            # Verifica se o polegar e o indicador estão levantados (para desenhar)
            if thumb_up and hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y:
                drawing = True
            else:
                drawing = False

            # Desenho com polegar e indicador levantados
            if drawing:
                cv2.line(canvas, (x, y), (x_new, y_new), color, 5)

            # Apagar a área onde a mão está quando todos os dedos estão levantados
            finger_up = [hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y for tip in [8, 12, 16, 20]]
            if all(finger_up):  # Se todos os dedos estiverem levantados, apaga a área ao redor da mão
                erase_area = 50  # Tamanho da área a ser apagada
                cv2.circle(canvas, (x_new, y_new), erase_area, (0, 0, 0), -1)

            # Atualizando a posição do dedo
            x, y = x_new, y_new

    # Combinando o desenho com o vídeo
    frame = cv2.add(frame, canvas)

    # Exibindo o resultado
    cv2.imshow("Desenhando", frame)

    # Tecla 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
