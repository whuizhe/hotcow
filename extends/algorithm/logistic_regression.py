# coding=utf-8
"""逻辑回归"""

import pickle
from django.core.cache import cache
from sklearn.linear_model import LogisticRegression


def logistic_regression(label: list, title: list):
    """
    :param label: X 特征数据
    :param title: Y 标示学习样本为 0 or 1
    数据预测 clf.predict(data: list)
    liblinear 小量数据效果更好
    sag or saga 适合大量数据
    :return:
    """
    clf = LogisticRegression(solver='liblinear', C=10)
    clf.fit(label, title)
    cache_key = 'logistic_regression_model_cache'
    cache.set(cache_key, pickle.dumps(clf), timeout=None)
    return clf
