from tkinter import *
import random
import time
import os
import sys


stop_game = False

class ball():
	# задаю начальное положение и направление движение;
	def __init__(self, color, field, ball_size, platform):
		# определяю параметры внутри объекта
		self.field = field
		self.ball_size = ball_size
		self.platform = platform
		# свойство которое определяет достиг мяч дна или нет
		self.hit_bottom = False
		# создаю индетификатор по которому можно обращаться к мячу
		self.id = self.field.create_oval(0, 0, ball_size, self.ball_size, fill=color, width=0)
		# двигаю мяч
		self.field.move(self.id, 5, 10)
		# создаю лист где задаю вектора для направления движения мяча
		starts = [-2, -1, 1, 2]
		# перемешиваю лист с векторами для мяча
		random.shuffle(starts)
		# задаю вектор движения мяча по оси x
		self.x = starts[0]
		# задаю вектор движения мяча по оси y (всегда вниз по этому -2)
		self.y = -2
		# рисую игровое поле для того, что бы в следующем шаге получить коректные данные о размере игрового поля 
		self.field.update()
		# узнаю размеры игрового поля
		self.field_height = self.field.winfo_height()
		self.field_width = self.field.winfo_width()


	# рисю мяч
	def draw(self):

		ball_coordinates = self.field.coords(self.id)
		platform_coordinates = self.field.coords(self.platform.id)

		left_border = 0
		top_border = 0
		right_border = self.field_width
		bottom_border = self.field_height
		
		left_ball = ball_coordinates[0]
		top_ball = ball_coordinates[1]
		right_ball = ball_coordinates[2]
		bottom_ball = ball_coordinates[3]

		center_ball = left_ball + ( self.ball_size / 2 )

		# соприкосновение с левой стороной игрового поля
		if left_ball <= left_border:
			# меняем вектор движения по оси х в положительную сторону
			self.x = random.randint(1, 3)
		# соприкосновение с верхом игрового поля
		if top_ball <= top_border:
			# меняем вектор движения по оси y в положительную сторону
			self.y = random.randint(2, 3)
		# соприкосновение с правой стороной игрового поля
		if right_ball >= right_border:
			# меняем вектор движения по оси х в отрицательную сторону
			self.x = -random.randint(1, 3)
		# соприкосновение с низом игрового поля
		if bottom_ball >= bottom_border:
			# логика для пропуска мяча
			self.platform.allowed_to_move = False
			self.hit_bottom = True

		if platform_coordinates[0] <= center_ball and center_ball <= platform_coordinates[2] and bottom_ball >= platform_coordinates[1]:
			self.y = -random.randint(2, 3)

		if stop_game == False:
			# двигаем мяч
			self.field.move(self.id, self.x, self.y)
			




class platform():

	def __init__(self, color, field):
		
		self.field = field
		self.id = field.create_rectangle(0, 0, 100, 10, fill=color)
		self.allowed_to_move = True

		ran_pos = [0, 50, 100, 150, 200, 250]
		random.shuffle(ran_pos)

		field.move(self.id, ran_pos[0], 390)

		self.field.bind_all('<KeyPress-Right>', self.turn_right)
		self.field.bind_all('<KeyPress-Left>', self.turn_left)

	def turn_right(self, event):
		if self.allowed_to_move == True:
			field.move(self.id, 7, 0)

	def turn_left(self, event):
		if self.allowed_to_move == True:
			field.move(self.id, -7, 0)



# создаю окно программы
window = Tk()
# задаю заголовок окну
window.title('My first PyGame')
# запрещаю менять размер окна
window.resizable(0, 0)
# окно поверх всех других окон
window.attributes("-topmost",True)
# создаю игровое поле
field = Canvas(window, width=500, height=450, highlightthickness=0 )
# позиционирую игровое поле в окне
field.pack()


# логика перед закрытием окна
def on_closing():
	ball.hit_bottom = True
	window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)

def output(e):
	window.destroy()

# создаю объекты
platform = platform('green', field)
ball = ball('#f50', field, 30, platform)

end_game_check = True

while True:


	if not ball.hit_bottom:
		ball.draw()
		field.update()
	
	if ball.hit_bottom == True and end_game_check == True:
		# добавляю текст
		field.create_text(250, 80, text='Ты проиграл :(', font=('Courier', 30), fill='red')
		field.create_text(250, 120, text='Ты набрал туеву кучу очков', font=('Courier', 20), fill='black')
		# добавляю кнопку
		field.button = Button(field, text="Закончить игру")
		# рисую кнопку на canvas
		field.create_window((255, 150), anchor="nw", window=field.button)
		# добавляю тригер для кнопку
		field.button.bind("<Button-1>", output)
		field.update()
		break;


	time.sleep(0.016)

# обновляю окно программы
window.mainloop()