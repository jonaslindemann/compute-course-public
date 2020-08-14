#include <iostream>

using namespace std;

extern "C" void myfunc(int a, double b, double *c)
{
  cout << "a = " << a << endl;
  cout << "b = " << b << endl;
  cout << "c = " << *c << endl; 
}
