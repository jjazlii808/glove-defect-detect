import numpy as np
import cv2

def rubber_stain():
    image = cv2.imread('gloves/paint.jpeg')

    # resizing the image
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

    # stain finding
    hsv2 = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
    stain_l = np.array([80, 50, 50])
    stain_u = np.array([140, 255, 255])
    stain_mask = cv2.inRange(hsv2, stain_l, stain_u)
    stain_contours, _ = cv2.findContours(stain_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # detecting the stain
    min_stain_area = 10
    max_aspect_ratio = 2.0
    stain_image = img.copy()
    for contour in stain_contours:
        area = cv2.contourArea(contour)
        if area > min_stain_area:
            x,y,w,h, = cv2.boundingRect(contour)
            aspect_ratio = float(w)/h
            if aspect_ratio < max_aspect_ratio:
                # cv2.drawContours(stain_image, [contour], -1, (0, 0, 255), 2)
                cv2.rectangle(stain_image, (x,y), (x+w,y+h), (0,0,255), 2)
                cv2.putText(stain_image, 'Stain', (x,y-5), cv2.FONT_HERSHEY_TRIPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)


    # cv2.imshow('Original Image', img)
    # cv2.imshow('Glove Masking', mask_filtered)
    # cv2.imshow('Glove Only', res)
    # cv2.imshow('Stain Masking', stain_mask)
    cv2.imshow('Stain Detection', stain_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
