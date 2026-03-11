import cv2 as cv

video = cv.VideoCapture(0) # 0 = 기본 노트북 웹캠
flip = False # 좌우 반전 상태 (False = 기본, True = Flip)
recording = False # 녹화 상태 (False = Preview m. True = Recording m.)

target_format = 'avi' # 파일 확장자
target_fourcc = 'XVID' # 코덱

def mouse_event_handler(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        img = param['img']
        cv.imwrite('capture.png', img)

cv.namedWindow('MECORDER')
param = {'img' : None}
cv.setMouseCallback('MECORDER', mouse_event_handler, param)

if video.isOpened():
    target = cv.VideoWriter()
    fps = video.get(cv.CAP_PROP_FPS)
    wait_msec = int(1/fps*1000)

    contrast = 1.0 # 대비 default
    brightness = 0 # 명암 default
    contrast_step = 0.1 # 대비 증감가율
    brightness_step = 1 # 명암 증감가율

    while True:
        valid, img = video.read()
        if not valid:
            break
        
        # Capture
        param['img'] = img

        # Flip
        if flip:
            img = cv.flip(img, 1)

        # Record
        if recording:
            cv.circle(img, (30, 40), 10, (0, 0, 255), -1) 
            cv.putText(img, "REC", (10,25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 255), 1)  
            cv.putText(img, "REC", (10,25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 255), 2)
            target.write(img)

        
        cv.putText(img, "CLICK : CAPTURE", (10,380), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 1)
        cv.putText(img, "F : FLIP", (10,410), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 1)
        cv.putText(img, "SPACE : RECORD", (10,440), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 1)
        cv.putText(img, "ESC : EXIT", (10,470), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 0, 0), 1)

        cv.imshow('MECORDER', img) # 웹캠 이름 = MECORDER


        key = cv.waitKey(wait_msec)

        if key == 27: # ESC = 27(ASCII) (Stop Webcam)
            video.release() # 웹캠 = 하드웨어 자원 = 반환 필요
            cv.destroyAllWindows()
            break
        elif key == ord('f'):
            flip = not flip
        elif key == 32: # SPACEBAR = 32(ASCII) (Stop/Start recording)
            recording = not recording
            if recording:
                fps = video.get(cv.CAP_PROP_FPS)
                h, w, *_ = img.shape
                is_color = (img.ndim > 2) and (img.shape[2] > 1)
                target = cv.VideoWriter('output.avi', cv.VideoWriter_fourcc(*target_fourcc), fps, (w, h), is_color)
            else :
                if target.isOpened():
                    target.release()

else :
    print("카메라를 열 수 없음.") # 웹캠이 열리지 않는다면 오류문 출력

