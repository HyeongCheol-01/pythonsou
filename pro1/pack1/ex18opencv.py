#opencv(Computer Vision)
#pip install opencv-python

import cv2
print(cv2.__version__)

img1 = cv2.imread('ani.jpeg')
print(type(img1))
cv2.imshow('image test', img1)
cv2.waitKey()
cv2.destroyAllWindows()
#print('end')

#다른 이름으로 저장
cv2.imwrite('ani2.jpg', img1)
cv2.imwrite('ani3.jpg', img1, [cv2.IMWRITE_JPEG_QUALITY,10])

#이미지 크기 조정


#이미지 밝기 조정









