# import time
# import random
# import cv2
# ob = open("example_fur_school.txt")
# cap = cv2.VideoCapture(0)
# cap.set(3,480)
# cap.set(4,480)
# x = ob.readline()
# n=0
# while True:
#     n+=0.25
#     if n%3==0:
#         x = ob.readline()
#     success, image = cap.read()
#     coordinates = (50, 100)
#     font = cv2.FONT_HERSHEY_SIMPLEX
#     fontScale = 1
#     color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
#     thickness = 2
#     cv2.putText(image, x, coordinates, font, fontScale, color, thickness, cv2.LINE_AA)
#     cv2.imshow("Text", image)
#     cv2.waitKey(1)
# ob = open("example_fur_school.txt")
# #print(ob.read().count("n"))
#
# # l = (ob.read()).split()
# # c=0
# # for x in l:
# #     if x[0] == "a" or x[0]== "A":
# #         c+=1
# # st = {" "}
# # # while st:
# # #     st.clear()
# # #     print(st)
# # print(type(st))
# def Displayline(ob):
#     s1 = ob.readlines()
#     s11=0
#     key = s1[0]
#     for x in s1:
#         if s11<len(x):
#             key = x
#             s11 = len(x)
#     return key[:-1]
# def FindTheHastage(ob):
#     s1 = ob.readlines()
#     key = {}
#     line_no = 0
#     for x in s1:
#         line_no+=1
#         if "#" in x:
#             if x != s1[:-1]:
#                 key[line_no]=x[:-1]
#             else:
#                 key[line_no] = x
#     return key
# def Line_no_and_line(ob):
#     line_no = 0
#     j = {}
#     #k= ob.readline()
#     for x in ob.readlines():
#         line_no+=1
#         K = x.split()
#         #print(K)
#         j[line_no] = len(K)
#     # while k:
#     #     line_no+=1
#     #     j[line_no] = k
#     #     k=ob.readline()
#
#     return j
# def readfirstthreeline(ob):
#     return ob.readlines()[0:3]
# #k = ob.read()
# k = Line_no_and_line(ob)
# #K = readfirstthreeline(ob)
# print(k)
# ob.close()
ob = open("sports.txt","w")
for x in range(5):
    user = input("enter the names james! :")
    ob.write(user+"/n")
ob.close()
