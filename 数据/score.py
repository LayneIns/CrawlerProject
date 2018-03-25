# coding: utf-8

from snownlp import SnowNLP

def senScore(x):
	return SnowNLP(x).sentiments
