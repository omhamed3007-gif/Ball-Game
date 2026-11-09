import tkinter
import random 
import math


WIDTH, HEIGHT = 400, 500
GRAVITY = [350,700,600,430,800,1200]      # pixels per second² 600
BOUNCE = [0.4,0.5,0.6,0.7,0.8,0.9]      # 1 = perfect bounce, 0 = no bounce
FPS = 100
DT = 1 / FPS       # time step in seconds

colors=["orange","white","lime green","light blue","red","yellow"]

window = tkinter.Tk()
canvas = tkinter.Canvas(window, width=WIDTH, height=HEIGHT, bg="black",
                        highlightthickness=0)
canvas.pack()


class Ball:
    global ballsCounter,nothingInthelist
    def __init__(self, x, y, vx, vy):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.radius = random.randint(4,36)
        self.color=random.choice(colors)
        self.gravity=random.choice(GRAVITY)
        self.bounce=random.choice(BOUNCE)
        self.mass=self.radius**2 #add weight to balls
        self.temp=random.randint(30,80)

    def update(self):
        # 1. gravity changes velocity
        self.vy += self.gravity * DT
        # 2. velocity changes position
        self.x += self.vx * DT
        self.y += self.vy * DT

        # 3. collisions with floor and walls
        if self.y + self.radius >= HEIGHT:
            self.y = HEIGHT - self.radius
            self.vy *= -self.bounce
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.vx *= -self.bounce
        elif self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius
            self.vx *= -self.bounce
    
    def draw(self):
      canvas.create_text(10, 10, text=f"BALLS: {ballsCounter}", fill="white",font=("Arial", 16), anchor="nw")
      canvas.create_text(10, 30, text=f"press Up to add 100 balls\nAnd Down to dellete a ball", fill="white",font=("Arial", 16), anchor="nw")
      canvas.create_oval(self.x - self.radius, self.y - self.radius,self.x + self.radius, self.y + self.radius,fill=self.color)
    def combineColors():
        for i in range (len(balls)):
            for j in range(i+1,len(balls)):
                if balls[i].color==balls[j].color:
                                    if balls[i].radius>=balls[j].radius:
                                        balls[i].radius+=balls[j].radius
                                        del balls[j]
                                    elif balls[j].radius>=balls[i].radius:
                                        balls[j].radius+=balls[i].radius
                                        del balls[i]
     
    def handle_collisions():
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):      # each pair checked once
                a,b = balls[i],balls[j]

                dx = b.x - a.x
                dy = b.y - a.y
                dist = math.hypot(dx, dy)
                min_dist = a.radius + b.radius

                if dist >= min_dist or dist == 0:
                    continue                         # not touching
                   

            # normal: unit vector from a to b
                nx, ny = dx / dist, dy / dist

            # 1. separate: split the overlap according to mass
                overlap = min_dist - dist
                total_mass = a.mass + b.mass
                a.x -= nx * overlap * (b.mass / total_mass)
                a.y -= ny * overlap * (b.mass / total_mass)
                b.x += nx * overlap * (a.mass / total_mass)
                b.y += ny * overlap * (a.mass / total_mass)

            # 2. bounce: relative velocity along the normal
                rvx = b.vx - a.vx
                rvy = b.vy - a.vy
                vn = rvx * nx + rvy * ny

                if vn > 0:
                    continue                         # already moving apart

                e = min(a.bounce, b.bounce)          # restitution
                impulse = -(1 + e) * vn / (1 
                     / a.mass + 1 / b.mass)

                a.vx -= impulse * nx / a.mass
                a.vy -= impulse * ny / a.mass
                b.vx += impulse * nx / b.mass
                b.vy += impulse * ny / b.mass
                if balls[i].color==balls[j].color:
                    if balls[i].radius>=balls[j].radius:
                        balls[i].radius+=balls[j].radius
                        del balls[j]
                    elif balls[j].radius>=balls[i].radius:
                        balls[j].radius+=balls[i].radius
                        del balls[i]



balls = [Ball(x=random.randint(0,300), y=random.randint(0,300), vx=random.randint(120,300), vy=0)]
ballsCounter=1
ball100=0
def addnewBall(e):
        global ball,ballsCounter,ball100
        if e.keysym=="space":
            balls.append(Ball(x=random.randint(0,300), y=random.randint(0,300), vx=random.randint(120,300), vy=0))
            ballsCounter+=1
        elif e.keysym=="Up":
            while ball100 <= 20:
             balls.append(Ball(x=random.randint(0,300), y=random.randint(0,300), vx=random.randint(120,300), vy=0))
             ballsCounter+=1
             ball100+=1
            ball100=0
        elif e.keysym=="Down":
            if len(balls)<=0:
                canvas.create_text(10,50,text="Cannot have 0 balls",fill="red",font=("Arial",20),anchor="nw")
            elif len(balls)>=1:
                del balls[0]
                ballsCounter-=1

def loop():
    canvas.delete("all")
    for ball in balls:
        ball.update()
        ball.draw()
    Ball.handle_collisions()
    Ball.combineColors()
    window.after(1000 // FPS, loop)   # scheduled once, at the end

window.bind("<KeyPress>",addnewBall)
loop()
window.mainloop()