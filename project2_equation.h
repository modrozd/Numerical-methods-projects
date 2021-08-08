#pragma once
#include "Matrix.h"
#include <iostream>

// c = 6, d = 8, e  = 7, f = 5
// a1 = 5 + e = 5 + 7 = 12
// a2 = a3 = -1
// N = 9cd = 968


#define a1A 12
#define a2 -1
#define a3 -1
#define f 5
#define e 1e-9
#define a1C 3


class Rownanie {
private:
	Matrix A;
	Matrix x;
	Matrix b;
	int N;
public:

	double metodaJacobiego() {
		Matrix temp(x);
		double iter = 0;
		while(true) 
		{
			iter++;
			for (int i = 0; i < N; i++) {
				double val = b[i][0];
				for (int k = 0; k < N; k++) {
					if (k != i)
						val -= A[i][k] * x[k][0];
				}
				val /= A[i][i];
				temp[i][0] = val;
			}
			x = temp;

			if (Matrix::norm(A * x - b) <= e)
				return iter;
		}
	}
	double metodaGaussaSeidla() {
		double iter = 0;
		while(true) 
		{
			iter++;
			for (int i = 0; i < N; i++) {
				double val = b[i][0];
				for (int k = 0; k < N; k++) {
					if (k != i)
						val -= A[i][k] * x[k][0];
				}
				val /= A[i][i];
				x[i][0] = val;
			}
			if (Matrix::norm(A * x - b) <= e)
				return iter;
		}
	}
	double metodaLU() {
		Matrix L(N, N);
		Matrix U(N, N);

		//Podzial
		for (int i = 0; i < N; i++)
			L[i][i] = 1.0;

		for (int j = 0; j < N; j++) {
			for (int i = 0; i <= j; i++) {
				U[i][j] += A[i][j];
				for (int k = 0; k <= i - 1; k++)
					U[i][j] -= L[i][k] * U[k][j];
			}

			for (int i = j + 1; i < N; i++) {
				for (int k = 0; k <= j - 1; k++)
					L[i][j] -= L[i][k] * U[k][j];

				L[i][j] += A[i][j];
				L[i][j] /= U[j][j];
			}
		}
		Matrix y(N, 1);
		//Podstawienie w przod dla Ly = b
		for (int i = 0; i < N; i++) {
			double val = b[i][0];
			for (int j = 0; j < i; j++)
				if (j != i) val -= L[i][j] * y[j][0];

			y[i][0] = val / L[i][i];
		}

		//Podstawienie wstecz dla Ux = y
		for (int i = N - 1; i >= 0; i--) {
			double val = y[i][0];
			for (int j = i; j < N; j++)
				if (j != i) 
					val -= U[i][j] * x[j][0];

			x[i][0] = val / U[i][i];
		}
		return Matrix::norm(A * x - b);
	}

	void initA() {
		A.init(a1A, a2, a3);

		for (int i = 0; i < N; i++) {
			x[i][0] = 1.0;

			double elem = sin(i * (f + 1));
			b[i][0] = elem;
		}
	}
	void initC() {
		A.init(a1C, a2, a3);

		for (int i = 0; i < N; i++) {
			x[i][0] = 1.0;

			double elem = sin(i * (f + 1));
			b[i][0] = elem;
		}
	}

	Rownanie(int _N) {
		N = _N;
		A = Matrix(N, N);
		x = Matrix(N, 1);
		b = Matrix(N, 1);
	}
};