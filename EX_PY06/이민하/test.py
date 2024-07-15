from turtle import Screen, Turtle
import random
import time

# --------------------------------------------------------------------
# [절차]
# 1. 거북이는 키를 누르면 방향대로 움직인다. 
# 2. 자동차는 범위 내에서 무작위로 생성되며, 화면의 오른쪽에서 왼쪽으로 움직인다. 
# 3. 거북이가 제일 윗 부분에 도착하면, 거북이는 원래 위치로 돌아가고 플레이어는 다음 레벨로 넘어간다.
# 4. 다음 단계에서 자동차의 개수가 증가하고 속도가 빨라진다.
# 5. 거북이와 자동차가 충돌하면, 게임은 종료되고 모든 것이 멈춘다. 
# --------------------------------------------------------------------
# [Constant]
STARTING_POSITION = (0, -280)
CAR_SPEED = 1
NUMBER_OF_CARS = 10
MOVE_DISTANCE = 20.
LEVEL_SCORE = 1

# [Screen]
screen = Screen()
screen.setup(width=600, height=600)
screen.title("turtle-crossing")
screen.bgcolor("black")
screen.tracer(0) # 스크린 창 출력을 조절할 수 있는 tracer함수

# [Player]
def go_up():
    new_y = player.ycor() + MOVE_DISTANCE
    player.goto(player.xcor(), new_y)


def go_down():
    if player.ycor() > -280:
        new_y = player.ycor() - MOVE_DISTANCE
        player.goto(player.xcor(), new_y)


def go_left():
    if player.xcor() > -280:
        new_x = player.xcor() - MOVE_DISTANCE
        player.goto(new_x, player.ycor())


def go_right():
    if player.xcor() < 280:
        new_x = player.xcor() + MOVE_DISTANCE
        player.goto(new_x, player.ycor())


def come_back_home():
    player.goto(STARTING_POSITION)


player = Turtle()
player.shape("turtle")
player.color("white")
player.setheading(90)
player.penup()
come_back_home()

# [Car]
COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]

cars = []

def create_cars():
    for i in range(NUMBER_OF_CARS):
        car = Turtle()
        car.shape("square")
        car.color(random.choice(COLORS))
        car.penup()
        car.goto(random.randint(-400, 400), random.randint(-200, 200))
        cars.append(car)

def update_cars():
    for car in cars:
        car.clear()
        car.goto(random.randint(-400, 400), random.randint(-200, 200))

create_cars()

# [Scoreboard]
def update_scoreboard():
    scoreboard.clear()
    scoreboard.goto(-200, 250)
    scoreboard.write(f"Level: {LEVEL_SCORE}", align="center", font=("Courier", 20, "normal"))


scoreboard = Turtle()
scoreboard.color("white")
scoreboard.penup()
scoreboard.hideturtle()
update_scoreboard()

screen.listen()
screen.onkey(go_up, "Up")
screen.onkey(go_down, "Down")
screen.onkey(go_left, "Left")
screen.onkey(go_right, "Right")

# [Gameoverboard]
def game_over():
    game_over_board.clear()
    game_over_board.write("Game Over", align="center", font=("Courier", 50, "normal"))


game_over_board = Turtle()
game_over_board.color("white")
game_over_board.penup()
game_over_board.hideturtle()

# [Game Loop]
game_is_on = True
while game_is_on:
    time.sleep(0.01)
    screen.update()
    # car is moving from right to left
    for car in cars:
        new_x = car.xcor() - CAR_SPEED
        car.goto(new_x, car.ycor())
        if car.xcor() < -400:
            car.goto(400, car.ycor())
    # collison
    for car in cars:
        if player.distance(car) < 20:
            game_is_on = False
            game_over()
    # arrived at target point 
    if player.ycor() == 280:
        create_cars()
        update_cars()
        come_back_home()
        LEVEL_SCORE += 1
        update_scoreboard()
        CAR_SPEED *= (1.2)
    

screen.exitonclick()