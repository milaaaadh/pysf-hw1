from colorama import Back,Style
a = int(input("please enter your window size: "))
a = a*18
up = a//6
for i in range(0, up):
    print(Back.BLUE+" "*(a-1), Style.RESET_ALL)
roof = a//3
for j in range ( 1, roof ):
    print(Back.BLUE+" "*((a-(j*2-1))//2),Back.RED+" "*(j*2-2), Back.BLUE+" "*((a-(j*2-1))//2-1), Style.RESET_ALL)


body = roof*2-2

for i in range(1,up+1):
    print(Back.BLUE+" "*((a-body)//2),Back.YELLOW+" "*(body-2),Back.BLUE+" "*((a-body)//2-1),Style.RESET_ALL)

for i in range(1,up+1):
    print(Back.BLUE+" "*((a-body)//2),Back.YELLOW+" "*((body-2)//3),Back.BLACK+" "*((body-2)//3),Back.YELLOW+" "*((body-2)//3),Back.BLUE+" "*((a-body)//2-1),Style.RESET_ALL)




#for i in range(0,a//2):
#    print(Back.BLUE,Back.GREEN,Style.RESET_ALL,end='')

#print()
#for i in range(0,a//2):
#    print(Back.GREEN,Back.LIGHTGREEN_EX,Style.RESET_ALL,end='')
