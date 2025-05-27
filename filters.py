import cv2

def apply_grayscale(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def apply_blur(img):
    return cv2.GaussianBlur(img, (7,7), 1.5)

def apply_edge(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(gray, 100, 200)

def apply_brightness(img, beta):
    return cv2.convertScaleAbs(img, alpha=1, beta=beta)

def apply_contrast(img, alpha):
    return cv2.convertScaleAbs(img, alpha=alpha, beta=0)
