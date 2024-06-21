from ultralytics import YOLO
import cv2

class Axe_Fogg_Detection:
    def __init__(self, model_path, video_source):
        self.model = YOLO(model_path)
        self.model.overrides['conf'] = 0.9
        self.model.overrides['max_det'] = 1
        self.cap = cv2.VideoCapture(video_source)

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            self.draw_center_point(frame)
            print(frame.shape) 
            results = self.model(frame) # code stuck here
            boxes = results[0].boxes.xyxy.tolist()
            class_names = results[0].boxes.cls.tolist()
            self.show_class_onFrame(frame, class_names)
            self.draw_bounding_boxes(frame, boxes)
            self.move_camera(boxes, frame)

            cv2.imshow("YOLOv8 Retail Wizardry", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def draw_center_point(self, frame):
        cv2.circle(frame, (int(frame.shape[1] / 2), int(frame.shape[0] / 2)), 3, (0, 0, 255), 3)

    def draw_bounding_boxes(self, frame, boxes):
        for box in boxes:
            x1, y1, x2, y2 = map(int, box)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    def show_class_onFrame(self, frame, class_names):
        if class_names:
            cv2.putText(frame, "Fogg" if class_names[0] == 1.0 else "Axe", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 225, 0), 2, cv2.LINE_AA)
        else:
            cv2.putText(frame, "None", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 225, 255), 2, cv2.LINE_AA)

    def move_camera(self, boxes, frame):
        if len(boxes) > 0:
            x_center_sum = 0
            y_center_sum = 0
            for i in range(len(boxes)):
                x1, y1, x2, y2 = map(int, boxes[i])
                x_center = (x2 - x1) / 2 + x1
                y_center = (y2 - y1) / 2 + y1
                x_center_sum += x_center
                y_center_sum += y_center

            x_center_avg = x_center_sum / len(boxes)
            y_center_avg = y_center_sum / len(boxes)

            cv2.circle(frame, (int(x_center_avg), int(y_center_avg)), 3, (255, 0, 0), 3)
            cv2.circle(frame, (int(x_center_avg), int(y_center_avg)), 20, (255, 0, 0), 1)

            if x_center_avg < int(frame.shape[1] / 2) - 20:
                # print("Move camera left")
                cv2.putText(frame, "Move camera left", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            elif x_center_avg > int(frame.shape[1] / 2) + 20:
                # print("Move camera right")
                cv2.putText(frame, "Move camera right", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            elif y_center_avg < int(frame.shape[0] / 2) - 20:
                # print("Move camera up")
                cv2.putText(frame, "Move camera up", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            elif y_center_avg > int(frame.shape[0] / 2) + 20:
                # print("Move camera down")
                cv2.putText(frame, "Move camera down", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            else:
                # print("Camera is centered")
                cv2.putText(frame, "Camera is centered", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

# Usage
model_path = 'best3.pt'
video_source = 0
axe_detection = Axe_Fogg_Detection(model_path, video_source)
axe_detection.run()
