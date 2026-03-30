class SimplePredictor:
    def __init__(self):
        # 初始化模型参数（假设已经训练好）
        self.coefficients = {
            'depth': 0.05,
            'power_usage': 0.1,
            'well_age': 0.02,
            'drawdown': 0.08,
            'lift': 0.03,
            'pump_power': 0.12
        }
        self.intercept = 10.0

    def predict(self, input_data):
        # 提取特征
        depth = input_data.get('depth', 0)
        power_usage = input_data.get('power_usage', 0)
        well_age = input_data.get('well_age', 0)
        drawdown = input_data.get('drawdown', 0)
        lift = input_data.get('lift', 0)
        pump_power = input_data.get('pump_power', 0)

        # 简单线性回归预测
        prediction = (
            self.coefficients['depth'] * depth +
            self.coefficients['power_usage'] * power_usage +
            self.coefficients['well_age'] * well_age +
            self.coefficients['drawdown'] * drawdown +
            self.coefficients['lift'] * lift +
            self.coefficients['pump_power'] * pump_power +
            self.intercept
        )

        return prediction

