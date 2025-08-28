from picamera2 import Picamera2
import numpy as np
import cv2

def display_lines(image, lines):
    lines_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(lines_image, (x1, y1), (x2, y2), (0, 0, 255), 10)
    return lines_image

def average_slope_intercept(image, lines):
    lane_lines = []
    left_fit = []
    right_fit = []

    if lines is not None:
        for line in lines:
            print(line)
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            print(parameters)
            slope = parameters[0]
            intercept = parameters[1]
            if slope < 0:   # 這是右車道線
                right_fit.append((slope, intercept))
            else:           # 這是左車道線
                left_fit.append((slope, intercept))
      
    # 計算左右車道的平均斜率和截距        
    right_average = np.average(right_fit, axis=0)
    left_average = np.average(left_fit, axis=0)
    # 依據平均斜率和平均截距來計算出左右車道線
    lane_lines.append(make_points(image, left_average))
    lane_lines.append(make_points(image, right_average))
    return lane_lines

def make_points(image, average):
    print(average)
    try:  # 避免斜率是 0
        slope, intercept = average
    except TypeError:
        slope, intercept = 0.001, 0
    y1 = image.shape[0]
    y2 = int(y1 * (3/5))
    x1 = int((y1 - intercept) // slope)
    x2 = int((y2 - intercept) // slope)
    return np.array([x1, y1, x2, y2])

# Camera setup
camera = Picamera2()
camera.configure(camera.create_preview_configuration(main={"size": (640, 480)}))
camera.start()

while True:
    frame = camera.capture_array()
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (5, 5), 0)
    edges = cv2.Canny(image, 50, 150)
    height, width = edges.shape
    print(height, width)
    # 長方形區域
    rectangle = np.array([[
                 (0, int(height * 1 / 2)+20),
                 (width, int(height * 1 / 2)+20),
                 (width, height),
                 (0, height),
                ]])
    # 建立相同尺寸的黑色圖片
    mask = np.zeros_like(edges)
    # 截取出車道位置的長方形
    mask = cv2.fillPoly(mask, rectangle, 255)
    isolated_area = cv2.bitwise_and(edges, mask)
    lines = cv2.HoughLinesP(isolated_area, 2, np.pi/180, 100,
                            np.array([]), minLineLength=40, maxLineGap=5)
    averaged_lines = average_slope_intercept(frame, lines)
    black_lines = display_lines(frame, averaged_lines)
    lanes = cv2.addWeighted(frame, 0.8, black_lines, 1, 1)
    cv2.imshow("Road Lane", lanes)    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
