import pygame
import tkinter as tk


#%% pygame
pygame.init()  # 初始化pygame
size = width, height = 640, 480  # 设置窗口大小
screen = pygame.display.set_mode(size)  # 显示窗口
color = (0, 0, 0)  # 设置颜色
ball = pygame.image.load('test.png')  # 加载图片
ballrect = ball.get_rect()  # 获取矩形区域
clock = pygame.time.Clock()
speed = [5, 5]  # 设置移动的X轴、Y轴
while True:  # 死循环确保窗口一直显示
    for event in pygame.event.get():  # 遍历所有事件
        if event.type == pygame.QUIT:  # 如果单击关闭窗口，则退出
            pygame.quit()
    ballrect = ballrect.move(speed)  # 移动小球
    # screen.fill(color)  # 填充颜色(设置为0，执不执行这行代码都一样)
    screen.blit(ball, ballrect)  # 将图片画到窗口上
    pygame.display.flip()  # 更新全部显示
    clock.tick(1)

#%% tkinter
top = tk.Tk()
top.title("窗口标题")
# top.geometry("500×100+100+100")  # “窗口宽x窗口高+窗口位于屏幕x轴+窗口位于屏幕y轴”，左下角为原点
window_size = width, height = 1280, 720
screenwidth, screenheight = top.winfo_screenwidth(), top.winfo_screenheight()
size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)  # center
top.geometry(size)
start_button = tk.Button(
    text="LET'S PLAY!",
    # width=25,  # unit: width of a char
    # height=5,
    bg="blue",  # background
    fg="yellow",  # text
    font='Arial 20 bold',
    # font=('Arial', 12)
)
# add to window
start_button.place(x=(screenwidth - width)/2, y=100, anchor=tk.W)
# start_button.pack()


top.mainloop()  # 进入消息循环, open window



