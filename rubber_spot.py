import numpy as np
import cv2

def rubber_spot():
    image = cv2.imread('gloves/spot.jpeg')

    #resizing the image
    width = int(image.shape[1] * 50 / 100)
    height = int(image.shape[0] * 50 / 100)
    img = cv2.resize(image, (width, height))

    # convert to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # upper bounds and lower bounds of latex
    r_lower = np.array([0, 0, 0])
    r_upper = np.array([255, 120, 255])

    # extraction
    rubber_extract = cv2.inRange(hsv, r_lower, r_upper)
    rubber_extract = cv2.bitwise_not(rubber_extract, rubber_extract)
    rubber_extract = cv2.erode(rubber_extract, None, iterations=1)
    rubber_extract = cv2.dilate(rubber_extract, None, iterations=1)

    contours, _ = cv2.findContours(rubber_extract, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    min_area = 0
    aspect_ratio_threshold = 0.0
    filtered_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > min_area:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.03 * perimeter, True)
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w)/h
            if aspect_ratio > aspect_ratio_threshold:
                filtered_contours.append(contour)

    mask_filtered = np.zeros_like(rubber_extract)
    cv2.drawContours(mask_filtered, filtered_contours, -1, 255, thickness=cv2.FILLED)
    res = cv2.bitwise_and(img, img, mask=mask_filtered) # just glove, no background


    # grayscale
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    # thresholding
    _, thresh = cv2.threshold(gray, 165, 255, cv2.THRESH_BINARY)

    # Morphological operations
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.erode(thresh, kernel, iterations=1)
    thresh = cv2.dilate(thresh, kernel, iterations=1)

    # finding contour
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filtered_contours = []
    min_area = 0.4
    max_aspect_ratio = 0.4

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        aspect_ratio = float(w)/h
        if area > min_area and aspect_ratio < max_aspect_ratio:
            filtered_contours.append(contour)

    result = img.copy()
    cv2.drawContours(result, filtered_contours, -1, (0,0,255), 2)

    # boxing
    glove_img = img.copy()
    spot_extract = glove_img.copy()
    for contour in filtered_contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)
        aspect_ratio = float(w)/h
        if area > min_area and aspect_ratio < max_aspect_ratio:
            (x, y, w, h) = cv2.boundingRect(contour)
            cv2.rectangle(spot_extract, (x, y), (x + w, y + h), (0,0,255), 2)
            cv2.putText(spot_extract, 'Spot', (x, y - 5), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)

    # cv2.imshow('Original Image', img)
    # cv2.imshow('Glove Only', res)
    # cv2.imshow('Thresholded', thresh)
    # cv2.imshow('Spot Highlights', result)
    cv2.imshow('Spot Detect', spot_extract)
    cv2.waitKey(0)
    cv2.destroyAllWindows()