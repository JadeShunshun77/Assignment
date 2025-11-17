"""
配置常量：容量、折旧、价格等。
这些数据直接来自作业文档。
"""

RENT_PER_MONTH = 800.0
STARTING_CASH = 7500.0

MAX_FLORISTS = 4
MIN_FLORISTS = 1
HOURS_PER_FLORIST = 80
WAGE_PER_HOUR = 15.50

# 温室容量
GREENHOUSE_CAPACITY = {
    "roses": 200,
    "daisies": 250,
    "greenery": 400,
}

# 每月折旧比例
DEPRECIATION = {
    "roses": 0.40,
    "daisies": 0.15,
    "greenery": 0.05,
}

# 温室成本（按当前库存数量收）
GREENHOUSE_COST_PER_BUNCH = {
    "roses": 1.50,
    "daisies": 0.80,
    "greenery": 0.20,
}

# 每月需求
DEMAND_PER_MONTH = {
    "fern_tastic": 175,
    "be_leaf": 100,
    "you_rose": 250,
}

# 售价
PRICE = {
    "fern_tastic": 18.50,
    "be_leaf": 17.75,
    "you_rose": 32.50,
}

# 配方与制作时间（分钟）
RECIPES = {
    "fern_tastic": {"greenery": 4, "roses": 0, "daisies": 2, "minutes": 20},
    "be_leaf":     {"greenery": 2, "roses": 1, "daisies": 3, "minutes": 30},
    "you_rose":    {"greenery": 2, "roses": 4, "daisies": 2, "minutes": 45},
}
