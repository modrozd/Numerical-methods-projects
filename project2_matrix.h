#pragma once
#include <iostream>
#include <assert.h>

class Matrix {
private:
	double** M;

public:
	int rows;
	int cols;

	void init(int a1, int a2, int a3) {
		for (int i = 0; i < rows - 2; i++) {
			for (int j = 0; j < cols - 2; j++) {
				if (i == j) {
					M[i][j] = a1;
					M[i + 1][j] = M[i][j + 1] = a2;
					M[i + 2][j] = M[i][j + 2] = a3;
				}
			}
		}
		M[rows - 2][cols - 2] = M[rows - 1][cols - 1] = a1;
		M[rows - 1][cols - 2] = M[rows - 2][cols - 1] = a2;
	}

	static double norm(Matrix m) {
		assert(m.cols == 1);
		double val = 0.0;
		for (int i = 0; i < m.rows; i++) {
			val += pow(m[i][0], 2);
		}
		return sqrt(val);
	}
	void allocateMemory() {
		M = new double* [rows];
		for (int i = 0; i < rows; i++)
			M[i] = new double[cols];

	}
	Matrix() : rows(1), cols(1) {
		allocateMemory();
		M[0][0] = 0;
	}
	Matrix(int rows, int cols) {
		this->rows = rows;
		this->cols = cols;
		allocateMemory();
		for (int i = 0; i < rows; i++) {
			for (int j = 0; j < cols; j++) {
				M[i][j] = 0;
			}
		}
	}
	Matrix(const Matrix& m) {
		this->rows = m.rows;
		this->cols = m.cols;
		allocateMemory();
		for (int i = 0; i < rows; i++) {
			for (int j = 0; j < cols; j++) {
				M[i][j] = m[i][j];
			}
		}
	}
	~Matrix() {
		for (int i = 0; i < rows; i++) {
			delete[] M[i];
		}
		delete[] M;
	}


// Operacje na macierzach
	Matrix& operator=(const Matrix& m) {
		if (this == &m) {
			return *this;
		}
		this->~Matrix();
		this->rows = m.rows;
		this->cols = m.cols;
		allocateMemory();
		for (int i = 0; i < rows; i++) {
			for (int j = 0; j < cols; j++) {
				M[i][j] = m[i][j];
			}
		}
		return *this;
	}
	Matrix& operator+=(const Matrix& m)
	{
		for (int i = 0; i < rows; i++) {
			for (int j = 0; j < cols; j++) {
				M[i][j] += m[i][j];
			}
		}
		return *this;
	}
	Matrix& operator-=(const Matrix& m)
	{
		for (int i = 0; i < rows; i++) {
			for (int j = 0; j < cols; j++) {
				M[i][j] -= m[i][j];
			}
		}
		return *this;
	}
	Matrix& operator*=(const Matrix& m) {
		Matrix temp(rows, m.cols);
		for (int i = 0; i < temp.rows; ++i) {
			for (int j = 0; j < temp.cols; ++j) {
				for (int k = 0; k < cols; ++k) {
					temp[i][j] += (M[i][k] * m[k][j]);
				}
			}
		}
		return (*this = temp);
	}

	Matrix& operator*=(double num)
	{
		for (int i = 0; i < rows; i++) {
			for (int j = 0; j < cols; j++) {
				M[i][j] *= num;
			}
		}
		return *this;
	}

	Matrix& operator-() {
		for (int i = 0; i < rows; i++) {
			for (int j = 0; j < cols; j++) {
				if (M[i][j] != 0)
					M[i][j] = -M[i][j];
			}
		}
		return *this;
	}

	double* operator[](size_t elem) {
		return M[elem];
	}
	double* operator[](size_t elem)const {
		return M[elem];
	}
	friend std::ostream& operator <<(std::ostream& stream, const Matrix& m) {
		for (int i = 0; i < m.rows; i++) {
			for (int j = 0; j < m.cols; j++) {
				stream << m[i][j] << " ";
			}
			stream << std::endl;
		}
		return stream;
	}
};

Matrix operator+(const Matrix& m1, const Matrix& m2)
{
	Matrix temp(m1);
	return (temp += m2);
}
Matrix operator-(const Matrix& m1, const Matrix& m2)
{
	Matrix temp(m1);
	return (temp -= m2);
}
Matrix operator*(const Matrix& m1, const Matrix& m2)
{
	Matrix temp(m1);
	return (temp *= m2);
}
Matrix operator*(const Matrix& m, double num)
{
	Matrix temp(m);
	return (temp *= num);
}
Matrix operator*(double num, const Matrix& m)
{
	return (m * num);
}
