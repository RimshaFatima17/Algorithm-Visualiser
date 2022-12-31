import pygame
import random
import math
pygame.init()

class DrawInformation:
	BLACK = 0, 0, 0
	MINT = 162, 228, 184
	GREEN = 0, 255, 0
	RED = 255, 0, 0
	BACKGROUND_COLOR = MINT
    
	#we need gradients to distinguish between the bars
	GRADIENTS = [
		(152,115,172),
	    (197,180,227),
		(198,161,207)
	]

	FONT = pygame.font.SysFont('serif', 30)  #regluar font
	LARGE_FONT = pygame.font.SysFont('serif', 40)  #larger font

	SIDE_PAD = 100   #leaving 50 pixels on either side
	TOP_PAD = 150    #leaving 150 pixels from top  

	def __init__(self, width, height, lst):
		self.width = width  #width of window
		self.height = height  #height of window

		self.window = pygame.display.set_mode((width, height))
		pygame.display.set_caption("Sorting Algorithm Visualization") #name of window
		self.set_list(lst)

	def set_list(self, lst):
		'''attributes related to list'''
		self.lst = lst
		self.min_val = min(lst)
		self.max_val = max(lst)

        #width and height are dynamic. thus calculate 
		self.block_width = round((self.width - self.SIDE_PAD) / len(lst))  #rounding cuz cant draw fractional values
		
		#now calculating height of 1 unit in a block
		self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
		self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
    
	draw_info.window.fill(draw_info.BACKGROUND_COLOR)

	title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.GREEN)
	draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2 , 5))

	controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)  # 1 is for anti aliasing, to make lines sharper
	draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2 , 45))
	#to display text on screen, blit() the window. blit takes the text i.e, controls and x,y coordinates
	#x,y are coordinates of top left corner, get_width()- returns width of the text
	# x=mid of window width - mid of text width , y=how low from top we want the text to be
	
	sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
	draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2 , 75))

	draw_list(draw_info)
	pygame.display.update() 


def draw_list(draw_info, color_positions={}, clear_bg=False):
	lst = draw_info.lst
	#color_positions is dictionary that stores; index:colour of bar at that index; the indices are of values getting swapped while sorting
    
	#since we clear only a part of the window, the area where the list is drawn 
	if clear_bg:
		clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
						draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
		
		#redrawing rectangle
		pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

	for i, val in enumerate(lst):
		x = draw_info.start_x + i * draw_info.block_width  #x corrdinate
		y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height  #y coordinate

		color = draw_info.GRADIENTS[i % 3]
    
		if i in color_positions:       #if i matches any key (list index) in color positions
			color = color_positions[i] 

		pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))  #draw_info.height- will directly draw downwards to the base of window
    #updating the window after the entire list is drawn
	if clear_bg:
		pygame.display.update()


def generate_starting_list(n, min_val, max_val):
	'''to determine the range of elements in the list''' 
	lst = []

	for _ in range(n):
		val = random.randint(min_val, max_val)  #randint(start, stop+1)- returns any integer between start and stop values
		lst.append(val)

	return lst


def bubble_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(len(lst) - 1):
		for j in range(len(lst) - 1 - i):
			num1 = lst[j]
			num2 = lst[j + 1]

			if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
				lst[j], lst[j + 1] = lst[j + 1], lst[j]
				#we draw the list again not the window cuz thats not efficient
				draw_list(draw_info, {j: draw_info.GREEN, j + 1: draw_info.RED}, True)
				yield True #gives user the control to use other buttons, give control back to main loop
				# otherwise the entire control during sorting will be with the function itself and system wont respond if anyother button is pressed

	return lst

def insertion_sort(draw_info, ascending=True):
	lst = draw_info.lst

	for i in range(1, len(lst)):
		current = lst[i]

		while True:
			ascending_sort = i > 0 and lst[i - 1] > current and ascending
			descending_sort = i > 0 and lst[i - 1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			lst[i] = lst[i - 1]
			i = i - 1
			lst[i] = current
			draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
			yield True

	return lst


def main():
	run = True
	clock = pygame.time.Clock()

	n = 50
	min_val = 0
	max_val = 100

	lst = generate_starting_list(n, min_val, max_val)

	#now instantiating DrawInformation to get an window
	draw_info = DrawInformation(980, 700, lst)

	sorting = False
	ascending = True

	sorting_algorithm = bubble_sort
	sorting_algo_name = "Bubble Sort"
	sorting_algorithm_generator = None
    #we need an event loop in pygame to always run in the background so that we can handle all events occuring
	while run:
		clock.tick(60)  # fps=60 i.e maximum times loop can run per second

		if sorting:
			try:
				next(sorting_algorithm_generator)
			except StopIteration:
				sorting = False
		else:
			draw(draw_info, sorting_algo_name, ascending)

		for event in pygame.event.get():  #pygame.event.get() - return list of all events that have occured in last loop
			if event.type == pygame.QUIT:  #close button
				run = False

			if event.type != pygame.KEYDOWN:
				continue

			if event.key == pygame.K_r:
				lst = generate_starting_list(n, min_val, max_val)
				draw_info.set_list(lst)
				sorting = False
			elif event.key == pygame.K_SPACE and sorting == False:
				sorting = True
				sorting_algorithm_generator = sorting_algorithm(draw_info, ascending)
			elif event.key == pygame.K_a and not sorting:
				ascending = True
			elif event.key == pygame.K_d and not sorting:
				ascending = False
			elif event.key == pygame.K_i and not sorting:
				sorting_algorithm = insertion_sort
				sorting_algo_name = "Insertion Sort"
			elif event.key == pygame.K_b and not sorting:
				sorting_algorithm = bubble_sort
				sorting_algo_name = "Bubble Sort"


	pygame.quit()


if __name__ == "__main__":
	main()
