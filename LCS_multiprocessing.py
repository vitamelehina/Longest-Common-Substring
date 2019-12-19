# Основной алгоритм взят из "https://www.geeksforgeeks.org/longest-common-substring-dp-29/"
from multiprocessing import Process, freeze_support, Queue # импортируем библиотеки процесса, проверки и очереди
from time import time# импортируем библиотеку времени, для того, чтобы засечь сколько работала программа
tic = time()
my_file = open("string1.txt", "r", encoding='utf-8') # открываем файл на чтение
text = my_file.read() # считываем текст из файла в переменную
my_file.close() # закрываем файл

my_file = open("string2.txt", "r", encoding='utf-8') # открываем файл на чтение
text2 = my_file.read() # считываем текст из файла в переменную
my_file.close() # закрываем файл
def LCSubStr2(q,q1):
	spis = q1.get() # достаем из очереди строки
	X = spis[0]  # присваиваем первый список - строку Х
	Y = spis[1] # присваиваем второй список - строку У
	m = len(X) # длина первого списка
	n = len(Y) # длина второго списка
	LCSuff = [[0 for k in range(n+1)] for l in range(m+1)]#создаем и зануляем данный двумерный массив
	result = 0 # создаем переменную результат и обнуляем. В ней будет хранится длина наибольшей общей подстроки
	k = 0 # создаем переменную К и обнуляем. В ней будет хранится последний номер элемента совпадающей общей подстроки

	# пробегаем по двумерному массиву выше главной диагонали
	for i in range(m):# пробегаем по строчкам
		for j in range(i+1, n+1): # пробегаем по столбцам
			if (i == 0 or j == 0): # если i или j равны нулю
				LCSuff[i][j] = 0 # зануляем
			elif (X[i-1] == Y[j-1]): #в противном случае, если предыдущие элементы по данной диагонали равнялись
				LCSuff[i][j] = LCSuff[i-1][j-1] + 1  # добавляем единицу в текущее значение массива
				if result < LCSuff[i][j]: # если "результат" меньше текущего значения массива
					result = LCSuff[i][j] # присваиваем "результату" данное число
					k = i # записываем номер
			else:
				LCSuff[i][j] = 0 # в других случаях зануляем
	q.put([k, result]) # добавляем в очередь результаты - номер и длину.
	return None # возвращаем ничего

def LCSubStr1(q,q1):
	spis = q1.get() # достаем из очереди списки
	X = spis[0] # присваиваем первый список - строку Х
	Y = spis[1] # присваиваем второй список - строку У
	m = len(X) # длина первого списка
	n = len(Y) # длина второго списка
	LCSuff = [[0 for k in range(n+1)] for l in range(m+1)]#создаем и зануляем данный двумерный массив
	result = 0 # создаем переменную результат и обнуляем. В ней будет хранится длина наибольшей общей подстроки
	k = 0 # создаем переменную К и обнуляем. В ней будет хранится последний номер элемента совпадающей общей подстроки

	# пробегаем по двумерному массиву ниже главной диагонали, включая главную диагональ
	for i in range(m + 1): # пробегаем по строчкам
		for j in range(i+1): # пробегаем по столбцам
			if (i == 0 or j == 0): # если i или j равны нулю
				LCSuff[i][j] = 0 # зануляем
			else: #в противном случае
				try: # пытаемся
					if (X[i-1] == Y[j-1]): # если предыдущие элементы по данной диагонали равнялись
						LCSuff[i][j] = LCSuff[i-1][j-1] + 1  # добавляем единицу в текущее значение массива
						if result < LCSuff[i][j]: # если "результат" меньше текущего значения массива
							result = LCSuff[i][j] # присваиваем "результату" данное число
							k = i # записываем номер
					else:
						LCSuff[i][j] = 0 # в других случаях зануляем
				except IndexError: # если массив выскачит за границу, например, если изначально строка 1 больше второй
					continue # тогда пропускаем цикл
	q.put([k, result]) # добавляем в очередь результаты - номер и длину.
	return None # возвращаем ничего

X = text  # записываем в Х тест из первого файла
Y = text2 # записываем в У текст из второго файла
if len(Y) > len(X): # если длина Х меньше, чем У, тогда меняем их местами
	X, Y = Y, X # переприсваиваем

N = 2 # задаем количество процессов равное двум
t1 = [] # создаем пустой список t1
t2 = [] # создаем пустой список t2

# для первого процесса
h1 = Queue() # создаем переменную h1 типа очередь
h2 = Queue() # создаем переменную h2 типа очередь
h2.put([X,Y]) # кладем в очередь h2 наши строки
t1+=[h1] # добавляем в 1 список пустую очередь h1
t2+=[h2] # добавляем в 2 список очередь h2

# для второго процесса
h1 = Queue() # создаем переменную h1 типа очередь
h2 = Queue() # создаем переменную h2 типа очередь
h2.put([X,Y]) # кладем в очередь h2 наши строки
t1+=[h1] # добавляем в 1 список пустую очередь h1
t2+=[h2] # добавляем в 2 список очередь h2

G = [] # создаем пустой список
if __name__ == '__main__': # используем это условие для работы с параллельными процессами на винде
	freeze_support() # проверка того, должен ли исполняемый процесс запускать код, полученный по каналу, или нет.
	g=Process(target=LCSubStr1, args= (t1[0],t2[0]))# создаем процесс с целью функцией LCSubStr1 и аргументами - очередями
	g1=Process(target=LCSubStr2, args= (t1[1],t2[1]))# создаем процесс с целью функцией LCSubStr2 и аргументами - очередями

	# запускаем два процесса
	g.start()
	g1.start()

	# ждем пока процессы завершатся
	g.join()
	g1.join()

	spis = t1[0].get() # достаем список из очереди первого процесса
	k = spis[0] # достаем номер последнего элемента совпадающей общей подстроки
	result = spis[1]# достаем длину наибольшей общей подстроки
	spis = t1[1].get()# достаем список из очереди второго процесса
	k2 = spis[0]# достаем номер последнего элемента совпадающей общей подстроки
	result2 = spis[1]# достаем длину наибольшей общей подстроки
	if result2 > result: # если длина второго общей подстроки второго процесса больше первого
		# выводим результат
		print("Длина наибольшей общей подстроки:",result2)# выводим длину наибольшей общей подсроки
		print('Наибольшая общая подстрока:"{}"'.format(X[k2-result2:k2]))# срезом выводим наибольшую общую подстроку
	else: # иначе
		# выводим результат
		print("Длина наибольшей общей подстроки:",result)# выводим длину наибольшей общей подсроки
		print('Наибольшая общая подстрока:"{}"'.format(X[k-result:k]))# срезом выводим наибольшую общую подстроку

	toc = time() # берем текущее время
	print("Время работы программы:",toc-tic) # вычисляем время
