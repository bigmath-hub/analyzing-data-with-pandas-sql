import numpy as np

def f(x, y):
    return x ** 2 + y ** 3

def grad_f(x, y):
    df_dx = 2 * x
    df_dy = 3 * y ** 2

    return np.array([df_dx, df_dy])

def main():
    point = (2, 3)

    grad = grad_f(point[0], point[1])

    print(f"funcao no ponto: {f(point[0], point[1])}")
    print(f"o gradiente no ponto: {grad}")


if __name__ == "__main__":
    main()

