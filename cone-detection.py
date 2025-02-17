import cv2
import numpy as np

# load image of cones with no line
image_path = "red.png"
image = cv2.imread(image_path)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# define red colors for the range in which a cone is detected
lower_red = np.array([0, 120, 100])
upper_red = np.array([10, 255, 255])
mask = cv2.inRange(hsv, lower_red, upper_red)

# find contours of cones to better find the location of the cones
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cone_positions = [cv2.boundingRect(cnt)[:2] for cnt in contours]

# sort cones into left and right and right lines to simulate lane lines
cone_positions.sort()
mid_x = np.mean([x for x, y in cone_positions])
left_cones = [(x, y) for x, y in cone_positions if x < mid_x]
right_cones = [(x, y) for x, y in cone_positions if x >= mid_x]

# fit and draw boundary lines
def draw_line(cones, color):
    if len(cones) > 1:
        fit = np.polyfit([y for x, y in cones], [x for x, y in cones], 1)
        y_min, y_max = min(y for x, y in cones), max(y for x, y in cones)
        x_min, x_max = int(np.polyval(fit, y_min)), int(np.polyval(fit, y_max))
        cv2.line(image, (x_min, y_min), (x_max, y_max), color, 3)

draw_line(left_cones, (255, 0, 0))
draw_line(right_cones, (255, 0, 0))

# show result
cv2.imshow("Detected Path", image)

# not sure why this was needed to display image, but only worked with these two lines of code
cv2.waitKey(0)
cv2.destroyAllWindows()

