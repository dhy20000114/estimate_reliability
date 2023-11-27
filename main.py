# 输入：报警信息excel表
# 输出：平均故障持续时间、平均故障间隔时间、平均故障概率、平均可靠性
import math
import random
import numpy as np
import pandas as pd
from config import *

# 平均故障持续时间、平均故障间隔时间、平均故障概率、平均可靠性
# 读取设备故障报警信息
data_n = pd.read_excel('CH_1-CH-F-.xlsx')
T = len(data_n)
state = [0 for i in range(T)]
state_ini = data_n['item_val']
for i in range(T):
    if state_ini[i] == 0:
        state[i] = 1


def params(data_T, unit_T, data_state):
    # 根据既有告警信息计算故障持续时间、故障间隔时间的估计量
    """
    :param data_T: 读取信息的次数
    :param unit_T: 采集时间粒度，即多久采集一次数据
    :param data_state: 告警信息
    """
    # 根据既有数据计算故障概率等基本参数
    failure_times = 0  # 故障次数
    for i in range(data_T - 1):
        if data_state[i] == data_state[i + 1]:  #
            failure_times = failure_times  # 故障次数
        else:
            failure_times = failure_times + 1
    failure_times = int(failure_times / 2)
    if failure_times == 0:
        a_failure_duration = unit_T * data_T  # 平均故障持续时间 即TTF
        a_TTF = 0
    else:
        a_failure_duration = unit_T * (data_T - sum(data_state)) / failure_times  # 平均故障持续时间 即TTR
        a_TTF = unit_T * sum(data_state) / failure_times  # 平均故障间隔时间
    a_false_rate = (data_T - sum(data_state)) / data_T  # 平均故障概率
    a_true_rate = sum(data_state) / data_T  # 平均可靠性
    data = [a_failure_duration, a_TTF, a_false_rate, a_true_rate]
    return data


def sample(simulation_N, TTF, TTR, unit_T):  # N是模拟采样次数，p是故障概率
    # 蒙特卡洛仿真单次循环模拟
    """
    :param simulation_N: 一个大循环下的蒙特卡洛仿真模拟次数
    :param TTF: 由params函数计算的故障间隔时间估计量
    :param TTR: 由params函数计算的故障持续时间估计量
    :param unit_T: 采集时间粒度
    """
    #  抽样模拟
    s_ua = [0 for i in range(simulation_N)]  # 0表示故障、1表示正常
    t = 0
    s_ua[0] = 1  # 初始状态默认是正常

    while t < simulation_N:
        # 大循环下的单论小循环
        U = random.random()
        if s_ua[t] == 1:
            ttf = (-1 * TTF * 10 * math.log(U)) // 1 + 1
            ttf = int(ttf)
            if (t + ttf) < simulation_N:
                for tt in range(ttf):
                    s_ua[t + tt] = 1
                s_ua[t + ttf] = 0
            if (t + ttf) > simulation_N:
                for tt in range(simulation_N - t):
                    s_ua[t + tt] = 1
            t = t + ttf
        else:
            ttr = (-1 * TTR * math.log(U)) // 1 + 1
            ttr = int(ttr)
            if (t + ttr) < simulation_N:
                for tt in range(ttr):
                    s_ua[t + tt] = 0
                s_ua[t + ttr] = 1
            if (t + ttr) > simulation_N:
                for tt in range(simulation_N - t):
                    s_ua[t + tt] = 0
            t = t + ttr
    failure_times = 0  # 计数采集期间的故障时间
    for i in range(simulation_N - 1):
        if s_ua[i] == s_ua[i + 1]:  #
            failure_times = failure_times
        else:
            failure_times = failure_times + 1
    failure_times = int(failure_times / 2)
    if failure_times == 0:
        a_failure_duration = 0  # 平均故障持续时间 即TTR
        a_TTF = unit_T * simulation_N
    else:
        a_failure_duration = unit_T * (simulation_N - sum(s_ua)) / failure_times  # 平均故障持续时间 即TTF
        a_TTF = unit_T * sum(s_ua) / failure_times  # 平均故障间隔时间
    a_false_rate = (simulation_N - sum(s_ua)) / simulation_N  # 平均故障概率
    a_true_rate = sum(s_ua) / simulation_N  # 平均可靠性
    data = [a_failure_duration, a_TTF, a_false_rate, a_true_rate]  # 索引从0开始
    return data


data = params(T, unit_T, state)

while s < NN:
    # 蒙特卡洛仿真大循环
    s = s + 1
    result = sample(N, data[1], data[0], unit_T)

    failure_duration_list.append(result[0])
    TTF_list.append(result[1])
    false_rate_list.append(result[2])
    true_rate_list.append(result[3])

    failure_duration = np.array(failure_duration_list)
    TTF = np.array(TTF_list)
    false_rate = np.array(false_rate_list)
    true_rate = np.array(true_rate_list)

    average_failure_duration = sum(failure_duration) / s
    average_TTF = sum(TTF) / s
    average_false_rate = sum(false_rate) / s
    average_true_rate = sum(true_rate) / s
    sig = (1 / s * (average_false_rate - average_false_rate ** 2)) ** 0.5 / (average_false_rate + 0.00000001)

# result = sample(100000, data[2], data[1], data[0], unit_T)
print('平均故障持续时间/小时')
print(average_failure_duration)
print('平均故障间隔时间/小时')
print(average_TTF)
print('平均故障概率')
print(average_false_rate)
print('平均可靠性')
print(average_true_rate)
#  平均故障持续时间，故障间隔时间，故障概率，可靠性
