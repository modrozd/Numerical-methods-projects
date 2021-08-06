// Projekt nr 2 Metody Numeryczne
// Monika Drozd

#include "Rownanie.h"
#include <iostream>
#include <time.h>
using namespace std;

float liczCzas(Rownanie& eq, void(Rownanie::* initF)(), double(Rownanie::* methodF)());

// A - macierz o rozmiarze N x N gdzie N = 9cd
// c = 6, d = 8, e = 7, f = 5
// N = 9cd = 968

#define N 968

int main()
{
	// Zadanie A - tworzenie ukladu rownan
	Rownanie eq(N);
	/*
	cout << "Zadanie B, iteracje:" << endl;
	cout << "Jacobi: " << liczCzas(eq, &Rownanie::initA, &Rownanie::metodaJacobiego) << "s" << endl;
	cout << "Gauss-Seidl: " << liczCzas(eq, &Rownanie::initA, &Rownanie::metodaGaussaSeidla) << "s" << endl;


	cout << "Zadanie C, zmiana a1: nie zbiegaja sie" << endl;

	eq.initC();
	cout << eq.metodaJacobiego();
	eq.initC();
	cout << eq.metodaGaussaSeidla();
	*/

	cout << "Zadanie D, LU:" << endl;
	cout << endl << liczCzas(eq, &Rownanie::initC, &Rownanie::metodaLU) << "s" << "Norma z residuum uzywajac LU wynosi: " << endl;

	cout << "Zadanie E:" << endl;
	int arrN[] = { 100, 500, 968, 1000, 2000, 3000, 5000 };
	int nSize = sizeof(arrN)/sizeof(arrN[0]);
	cout << "Metoda Jacobiego:" << endl;
	for (int i = 0; i < nSize; i++) {
		Rownanie X(arrN[i]);
		cout << "N = " << arrN[i] << " czas: " << liczCzas(X, &Rownanie::initA, &Rownanie::metodaJacobiego) << "s" << endl;
	}
	cout << endl << "Metoda Gaussa-Seidla:" << endl;
	for (int i = 0; i < nSize; i++) {
		Rownanie X(arrN[i]);
		cout << "N = " << arrN[i] << " czas: " << liczCzas(X, &Rownanie::initA, &Rownanie::metodaGaussaSeidla) << "s" << endl;
	}
	cout << endl << "Metoda LU:" << endl;
	for (int i = 0; i < nSize; i++) {
		Rownanie X(arrN[i]);
		cout << "N = " << arrN[i] << " czas: " << liczCzas(X, &Rownanie::initA, &Rownanie::metodaLU) << "s" << endl;
	}
	return 0;
}

float liczCzas(Rownanie& eq, void(Rownanie::* initF)(), double(Rownanie::* methodX)()) {
	(eq.*initF)();
	int start = clock();
	cout << (eq.*methodX)() << " iteracje, ";
	return (float)(clock() - start) / CLOCKS_PER_SEC;
}
