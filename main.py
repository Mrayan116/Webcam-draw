import cv2


camera = cv2.VideoCapture(0)

if camera.isOpened() == False:
    print("Error: Could not open webcam.")
else:
    while True:
        success, frame = camera.read()

        if success == True:
            cv2.imshow("Air Drawing Board", frame)

        key = cv2.waitKey(1)

        if key == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()