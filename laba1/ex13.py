from turtle import *

speed(10)

#лицо
color("black", "yellow")  # (контур, заливка)
begin_fill()
circle(100)
end_fill()

# глаз 1
pu()
goto(30, 120)
pd()
color("black", "black")
begin_fill()
circle(15)  # черный глаз
end_fill()

# глаз 2
pu()
goto(-30, 120)
pd()
begin_fill()
circle(15)
end_fill()

#улыбка
pu()
goto(-40, 70)
pd()
setheading(-60)
pensize(3)
color("red")
circle(40, 120)

done()