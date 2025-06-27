import socket
import cv2
import pickle
import struct
import pyautogui
import os



def save_screenshot(dat,filename='screenshot.png'):
    with open(filename, "wb") as f:
        f.write(dat)


def receive_video_stream(host, port):
    while True:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((host, port))
            server_socket.listen(5)
            print("Сервер запущен. Ожидание подключения...")

            conn, addr = server_socket.accept()
            print(f"Подключен клиент: {addr}")



            try:
                while True:

                    comm = input("Command: ")
                    conn.send(comm.encode())

                    if comm=="exit":
                         server_socket.close()

                    elif comm=="webcam":
                        data = b""
                        payload_size = struct.calcsize("Q")


                        while True:
                            while len(data) < payload_size:
                                packet = conn.recv(4 * 1024)
                                if not packet:
                                    break
                                data += packet

                            if not data:
                                break




                            packed_msg_size = data[:payload_size]
                            data = data[payload_size:]
                            msg_size = struct.unpack("Q", packed_msg_size)[0]

                            while len(data) < msg_size:
                                data += conn.recv(4 * 1024)

                            frame_data = data[:msg_size]
                            data = data[msg_size:]


                            frame = pickle.loads(frame_data)


                            cv2.imshow("Received Video", frame)
                            if cv2.waitKey(1) & 0xFF ==ord("q"):
                                break


                        cv2.destroyAllWindows()



                    elif comm=="screenshot":
                        scr_size = int.from_bytes(conn.recv(8), byteorder="big")
                        rec_dat=b''
                        while len(rec_dat) < scr_size:
                            dat=conn.recv(4096)
                            if not dat:
                                break
                            rec_dat+=dat

                        if len(rec_dat)==scr_size:
                            save_screenshot(rec_dat)
                        else:
                            print("Error")






            finally:
                cv2.destroyAllWindows()
                conn.close()
                server_socket.close()

        except Exception as e:
            print(e)

receive_video_stream('localhost', 12345)