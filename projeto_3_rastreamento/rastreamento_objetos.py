import cv2
import numpy as np
from tracker import EuclideanDistTracker

# Vídeo
cap = cv2.VideoCapture(r"C:\Users\fabio\Downloads\VideoCarros.mp4")

# Detector de objetos (câmera estável)
object_detector = cv2.createBackgroundSubtractorMOG2(history=200, varThreshold= 60)

# Tracker de múltiplos objetos
tracker = EuclideanDistTracker()

# Parâmetros para limpar boxes
AREA_MINIMA = 800   # aumenta se ainda pegar pedaços do carro
MERGE_MARGIN = 30    # aumenta se sobrar 2 boxes muito coladas

def merge_close_boxes(boxes, margin=20):
    if not boxes:
        return []

    merged = True
    boxes = boxes[:]
    while merged:
        merged = False
        new_boxes = []
        used = [False] * len(boxes)

        for i in range(len(boxes)):
            if used[i]:
                continue
            x1, y1, w1, h1 = boxes[i]
            ax1, ay1 = x1, y1
            ax2, ay2 = x1 + w1, y1 + h1
            mx1, my1, mx2, my2 = ax1, ay1, ax2, ay2

            for j in range(i + 1, len(boxes)):
                if used[j]:
                    continue
                x2, y2, w2, h2 = boxes[j]
                bx1, by1 = x2, y2
                bx2, by2 = x2 + w2, y2 + h2

                # Se não há separação clara (considerando margem), funde
                if not (mx2 + margin < bx1 or bx2 + margin < mx1 or
                        my2 + margin < by1 or by2 + margin < my1):
                    mx1 = min(mx1, bx1)
                    my1 = min(my1, by1)
                    mx2 = max(mx2, bx2)
                    my2 = max(my2, by2)
                    used[j] = True
                    merged = True

            used[i] = True
            new_boxes.append([mx1, my1, mx2 - mx1, my2 - my1])

        boxes = new_boxes

    return boxes

while True:
    ret, frame = cap.read()
    if not ret:
        break

    height, width, _ = frame.shape

    # ROI (seu ajuste)
    roi = frame[600:1000, 900:1600]

    # 1. Detecção na ROI
    mask = object_detector.apply(roi)
    _, mask = cv2.threshold(mask, 150, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    detections = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > AREA_MINIMA:
            x, y, w, h = cv2.boundingRect(cnt)
            detections.append([x, y, w, h])

    # 2. Fusão de boxes próximos (reduz várias caixas no mesmo carro)
    detections = merge_close_boxes(detections, margin=MERGE_MARGIN)

    # 3. Rastreamento (associa IDs)
    boxes_ids = tracker.update(detections)

    # 4. Desenhar resultados na ROI
    for x, y, w, h, obj_id in boxes_ids:
        cx = x + w // 2
        cy = y + h // 2

        cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(roi, str(obj_id), (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.circle(roi, (cx, cy), 4, (0, 255, 255), -1)

    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)

    key = cv2.waitKey(30)
    if key == 27 or key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
