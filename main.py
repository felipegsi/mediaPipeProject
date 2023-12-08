import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk

def printarQuadro(dedos_levantados, frame):
    cv2.rectangle(frame, (80, 10), (200, 100), (255, 255, 0), -1)
    cv2.putText(frame, str(dedos_levantados), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 255), 5)

def moverMouse(dedos_levantados):
    # Código que permite desenho com o dedo
    speed = 10
    if dedos_levantados == 1:
        pyautogui.move(0, -speed)
    elif dedos_levantados == 2:
        pyautogui.move(0, speed)
    elif dedos_levantados == 3:
        pyautogui.move(speed, 0)
    elif dedos_levantados == 4:
        pyautogui.move(-speed, 0)
    elif dedos_levantados == 5:
        pyautogui.mouseDown()
def numero_dedos(pontos, frame):
    if pontos is not None and len(pontos) > 0:
        dedos_levantados = 0

        if pontos[4][0] > pontos[3][0]:
            dedos_levantados += 1

        for x in [8, 12, 16, 20]:
            if pontos[x][1] < pontos[x - 2][1]:
                dedos_levantados += 1

        moverMouse(dedos_levantados)
        printarQuadro(dedos_levantados, frame)

def processar_maos():
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    vid = cv2.VideoCapture(0)
    vid.set(3, 900)
    vid.set(4, 600)

    while True:
        ret, frame = vid.read()

        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        h, w, _ = frame.shape
        pontos = []

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                for id, cord in enumerate(hand_landmarks.landmark):
                    cx, cy = int(cord.x * w), int(cord.y * h)
                    pontos.append((cx, cy))
                numero_dedos(pontos, frame)
        cv2.imshow('MediaPipe Hands', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    hands.close()
    vid.release()
    cv2.destroyAllWindows()


def processar_comando():
    entrada = entrada_text.get()

    if entrada == 'd':
        processar_maos()
    elif entrada == 'q':
        root.quit()
    else:
        # Mostra uma mensagem de erro na própria janela
        label_erro = tk.Label(root, text="Comando inválido. Digite 'd' para processar ou 'q' para sair.", fg="red")
        label_erro.pack()

#melhorar a interface

root = tk.Tk()
root.title("Interface para comandos")

entrada_text = tk.Entry(root)
entrada_text.pack()

botao_processar = tk.Button(root, text="Processar", command=processar_comando)
botao_processar.pack()

root.mainloop()