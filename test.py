from sklearn import linear_model

reg = linear_model.Ridge(alpha=0.5)
reg.fit([[0, 0], [0, 0], [1, 1]], [0, 0.1, 1])

print(reg.coef_)

print(reg.intercept_)

reg = linear_model.RidgeCV(alphas=[0.1, 1.0, 10.0])
reg.fit([[0, 0], [0, 0], [1, 1]], [0, 0.1, 1])
print(reg.alpha_)

import matplotlib.pyplot as plt
from numpy import *

#创建数据集
def load_dataset():
    n = 100
    X = [[1, 0.005*xi] for xi in range(1, 100)]
    Y = [2*xi[1]  for xi in X]
    return X, Y

def sigmoid(z):
    t = exp(z)
    return t/(1+t)

#让sigmodi函数向量化，可以对矩阵求函数值，矩阵in，矩阵out
sigmoid_vec = vectorize(sigmoid)

#梯度下降法求解线性回归
def grad_descent(X, Y):
    X = mat(X)
    Y = mat(Y)
    row, col = shape(X)
    alpha = 0.05
    maxIter = 5000
    W = ones((1, col))
    V = zeros((row, row), float32)
    for k in range(maxIter):
        L = sigmoid_vec(W*X.transpose())
        for i in range(row):
            V[i, i] = L[0, i]*(L[0,i] - 1)
        W = W - alpha * (Y - L)*V*X
    return W

def main():
    X, Y = load_dataset()
    print(X)
    print(Y)
    W = grad_descent(X, Y)
    print("W = ", W)

    #绘图
    x = [xi[1] for xi in X]
    y = Y
    plt.plot(x, y, marker="*")
    xM = mat(X)
    y2 =  sigmoid_vec(W*xM.transpose())
    y22 = [y2[0,i] for i in range(y2.shape[1]) ]
    plt.plot(x, y22, marker="o")
    plt.show()

if __name__ == "__main__":
    main()