# -*- coding: utf-8 -*-
import math

# define deslocamento dos quadrantes
def offset(a, b, order, quadrant):
	if quadrant == 1:
		a = b = 0
		
	if quadrant == 2:
		a = 0
		b = order

	if quadrant == 3:
		a = b = order

	if quadrant == 4:
		a = order
		b = 0
	
	return a,b

# soma final do algoritmo
def solve( result, A, B, order, quadrant ):
	
	a = b = 0
	a, b = offset(a, b, order, quadrant)
	
	for i in range(0, order):
		for j in range(0, order):
			result[i+a][j+b] = A[i][j] + B[i][j]

# operação de soma (op_code = 0) e subtração (op_code = 1) de matrizes
def matrix_op( result, a, b, order, op_code):

	scalar = 1

	if op_code == 1:
		scalar = -1
	
	for i in range(0, order):
		for j in range(0, order):
			result[i][j] = a[i][j] + (scalar * b[i][j])

# copia as sub-matrizes de cada quadrante
def copy_submatrix( to, of, order, quadrant ):
	
	a = b = 0
	a, b = offset(a, b, order, quadrant)

	for i in range(0, order):
			for j in range(0, order):
				to[i][j] = of[i+a][j+b]

# recursão para multiplicação de matrizes
def matrix_multiplication( A, B, order ):

	# Condição de parada (matrizes de ordem 2):
	if order == 2:
		
		C = [[0 for i in range(0, order)] for j in range(0, order)]

		M1 = (A[0][0] + A[1][1]) * (B[0][0] + B[1][1])
		M2 = (A[1][0] + A[1][1]) * B[0][0]
		M3 = A[0][0] * (B[0][1] - B[1][1])
		M4 = A[1][1] * (B[1][0] - B[0][0])
		M5 = (A[0][0] + A[0][1]) * B[1][1]
		M6 = (A[1][0] - A[0][0]) * (B[0][0] + B[0][1])
		M7 = (A[0][1] - A[1][1]) * (B[1][0] + B[1][1])

		C[0][0] = M1 + M4 - M5 + M7
		C[0][1] = M3 + M5
		C[1][0] = M2 + M4
		C[1][1] = M1 - M2 + M3 + M6

		return C

	# Se não for uma matriz 2x2, divide em 4 sub-matrizes
	else:

		order //= 2

		# Cria 4 sub-matrizes para as matrizes A e B com a nova ordem
		a1 = [[0 for i in range(0, order)] for j in range(0, order)]
		a2 = [[0 for i in range(0, order)] for j in range(0, order)]
		a3 = [[0 for i in range(0, order)] for j in range(0, order)]
		a4 = [[0 for i in range(0, order)] for j in range(0, order)]

		b1 = [[0 for i in range(0, order)] for j in range(0, order)]
		b2 = [[0 for i in range(0, order)] for j in range(0, order)]
		b3 = [[0 for i in range(0, order)] for j in range(0, order)]
		b4 = [[0 for i in range(0, order)] for j in range(0, order)]

		copy_submatrix(a1, A, order, 1)
		copy_submatrix(a2, A, order, 2)
		copy_submatrix(a4, A, order, 3)
		copy_submatrix(a3, A, order, 4)

		copy_submatrix(b1, B, order, 1)
		copy_submatrix(b2, B, order, 2)
		copy_submatrix(b4, B, order, 3)
		copy_submatrix(b3, B, order, 4)

		# Cálculo das matrizes M1...M7 do algoritmo de Strassen
		
		# M1
		a1a4 = [[0 for i in range(0, order)] for j in range(0, order)]
		matrix_op(a1a4, a1, a4, order, 0)
		b1b4 = [[0 for i in range(0, order)] for j in range(0, order)]
		matrix_op(b1b4, b1, b4, order, 0)
		M1 = matrix_multiplication(a1a4, b1b4, order)

		# M2
		a3a4 = [[0 for i in range(0, order)] for j in range(0, order)]
		matrix_op(a3a4, a3, a4, order, 0)
		M2 = matrix_multiplication(a3a4, b1, order)

		# M3
		b2b4 = [[0 for i in range(0, order)] for j in range(0, order)]
		matrix_op(b2b4, b2, b4, order, 1)
		M3 = matrix_multiplication(a1, b2b4, order)

		# M4
		b3b1 = [[0 for i in range(0, order)] for j in range(0, order)]
		matrix_op(b3b1, b3, b1, order, 1)
		M4 = matrix_multiplication(a4, b3b1, order)

		# M5
		a1a2 = [[0 for i in range(0, order)] for j in range(0, order)]
		matrix_op(a1a2, a1, a2, order, 0)
		M5 = matrix_multiplication(a1a2, b4, order)

		# M6
		a3a1 = [[0 for i in range(0, order)] for j in range(0, order)]
		matrix_op(a3a1, a3, a1, order, 1)
		b1b2 = [[0 for i in range(0, order)] for j in range(0, order)]
		matrix_op(b1b2, b1, b2, order, 0)
		M6 = matrix_multiplication(a3a1, b1b2, order)

		# M7
		a2a4 = [[0 for i in range(0, order)] for j in range(0, order)]
		matrix_op(a2a4, a2, a4, order, 1)
		b3b4 = [[0 for i in range(0, order)] for j in range(0, order)]
		matrix_op(b3b4, b3, b4, order, 0)
		M7 = matrix_multiplication(a2a4, b3b4, order)

		# Define matriz resultante C da multiplicação
		C = [[0 for i in range(0, 2*order)] for j in range(0, 2*order)]

		# C1
		m1m4 = [[0 for i in range(0, order)] for j in range(0, order)]
		matrix_op(m1m4, M1, M4, order, 0)
		m5m7 = [[0 for i in range(0, order)] for j in range(0, order)]
		matrix_op(m5m7, M7, M5, order, 1)
		solve(C, m1m4, m5m7, order, 1)

		# C2	
		solve(C, M3, M5, order, 2)

		# C3
		solve(C, M2, M4, order, 4)

		# C4
		m1m6 = [[0 for i in range(0, order)] for j in range(0, order)]
		matrix_op(m1m6, M1, M6, order, 0)
		m2m3 = [[0 for i in range(0, order)] for j in range(0, order)]
		matrix_op(m2m3, M3, M2, order, 1)
		solve(C, m1m6, m2m3, order, 3)
		
		return C

# prepara execução do algoritmo de Strassen
def Strassen( matrix1 , matrix2 ):
    
    # Verifica qual potência de 2 representa uma matriz com ordem para alocar as matrizes 1 e 2
	order = max(len(matrix1), len(matrix2), len(matrix1[0]), len(matrix2[0]))

	if(math.log2(order) != int):
		order = pow(2, math.ceil(math.log2(order)))

	# Caso especial de matriz 1x1
	if order == 1:
		order = 2

	# Novas matrizes quadradas completadas com zero
	A = [[0 for i in range(0, order)] for j in range(0, order)]
	B = [[0 for i in range(0, order)] for j in range(0, order)]

	# Copia matrizes originais 1 e 2 nas novas matrizes maiores A e B
	for i in range(len(matrix1)):
		for j in range(len(matrix1[0])):
			A[i][j] += matrix1[i][j]

	for i in range(len(matrix2)):
		for j in range(len(matrix2[0])):
			B[i][j] += matrix2[i][j]

	# Chamada da função recursiva
	A = matrix_multiplication(A, B, order)

	# Copia matriz resultante usando o tamanho correto
	C = [[0 for i in range(0, len(matrix2[0]))] for j in range(0, len(matrix1))]

	for i in range(0, len(C)):
		for j in range(0, len(C[0])):
			C[i][j] = A[i][j]

	return C

# leitura das matrizes de entrada
def readFiles( name_m1 , name_m2 ):

	matrix1 = []
	matrix2 = []

	readM1 = open(name_m1, 'r')
	lineM1, rowM1 = map( int, readM1.readline().split() )
	for i in range(lineM1):
		matrix1 += 	[list(map( int, readM1.readline().split() ))]

	readM2 = open(name_m2, 'r')
	lineM2, rowM2 = map( int, readM2.readline().split() )
	for i in range(lineM2):
		matrix2 += 	[list(map( int, readM2.readline().split() ))]

	readM2.close()
	readM1.close()

	return matrix1 , matrix2

m1 , m2 = readFiles( 'M1.in' , 'M2.in' )

print(Strassen( m1 , m2 ))