import sys
import random
from PyQt5 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):

    # Cost, Benefit, Random?
    dishes_dict = {
        "一等菜": [9, 3, True],
        "二等菜": [6, 3, False],
        "三等菜": [3, 2, False],
        "四等菜": [0, 1, False],
    }

    # Cost, Benefit, Random?
    store_dict = {
        "挂肆": [6, 0, True],
        "蹴鞠场": [6, 0, False],
        "书坊": [6, 3, False],
        "酒肆": [7, 1, False],
        "绸缎庄": [7, 4, False],
        "勾栏瓦舍": [8, 0, False],
        "瓷器铺": [9, 6, False],
        "饮子铺": [5, 2, False],
        "说书场": [5, 2, False],
        "关扑铺": [5, 2, False],
        "首饰铺": [5, 2, False],
        "茶馆": [5, 2, False],
    }

    def __init__(self):
        super().__init__()

        self.money = 10
        self.store_list = []
        self.new_money = 0
        self.new_store_list = []

        # Title
        self.title_label = QtWidgets.QLabel("大宋百商图 计算器",
                                            alignment=QtCore.Qt.AlignCenter)

        # Status
        self.money_text = QtWidgets.QLabel()
        self.store_text = QtWidgets.QLabel()
        self.new_money_text = QtWidgets.QLabel()
        self.new_store_text = QtWidgets.QLabel()

        self.set_money_status()
        self.set_store_status()
        self.set_new_money_status()
        self.set_new_store_status()

        status_layout = QtWidgets.QGridLayout()
        status_layout.addWidget(self.money_text, 0, 0)
        status_layout.addWidget(self.store_text, 1, 0)
        status_layout.addWidget(self.new_money_text, 0, 1)
        status_layout.addWidget(self.new_store_text, 1, 1)
        status_widget = QtWidgets.QGroupBox("老板状态")
        status_widget.setLayout(status_layout)

        # Effort group
        effort_layout = QtWidgets.QHBoxLayout()
        effort_buttons = []
        for key in ["俭以养德", "门可罗雀", "无奸不商", "时和年丰", "张灯结彩", "银装素裹", "辞旧迎新", "苛捐杂税", "硕果累累"]:
            effort_button = QtWidgets.QPushButton(key)
            effort_button.setCheckable(True)
            effort_buttons.append(effort_button)
            effort_layout.addWidget(effort_button)
        effort_widget = QtWidgets.QGroupBox("效果牌")
        effort_widget.setLayout(effort_layout)

        # Ground dishes
        ground_layout = QtWidgets.QHBoxLayout()
        ground_layout.addWidget(QtWidgets.QLabel("老板要扩展产业吗？"))
        for key in ["0", "2", "3", "4", "7", "8", "9", "10"]:
            ground_button = QtWidgets.QPushButton(key)
            ground_button.clicked.connect(self.buy_ground)
            ground_layout.addWidget(ground_button)
        ground_layout.addStretch()

        # Buy dishes
        dishes_layout = QtWidgets.QHBoxLayout()
        dishes_layout.addWidget(QtWidgets.QLabel("老板要增加菜品吗？"))
        for key in self.dishes_dict.keys():
            dishes_button = QtWidgets.QPushButton(key)
            dishes_button.clicked.connect(self.buy_dishes)
            dishes_layout.addWidget(dishes_button)
        dishes_layout.addStretch()

        # Store dishes
        store_layout = QtWidgets.QHBoxLayout()
        store_layout.addWidget(QtWidgets.QLabel("老板要建设店铺吗？"))
        for key in self.store_dict.keys():
            store_button = QtWidgets.QPushButton(key)
            store_button.clicked.connect(self.buy_store)
            store_layout.addWidget(store_button)
        store_layout.addStretch()

        # Group 1
        group1_layout = QtWidgets.QVBoxLayout()
        group1_layout.addLayout(ground_layout)
        group1_layout.addLayout(dishes_layout)
        group1_layout.addLayout(store_layout)
        group1_widget = QtWidgets.QGroupBox("第一阶段")
        group1_widget.setLayout(group1_layout)

        # Ground dishes
        dish_rm_layout = QtWidgets.QHBoxLayout()
        dish_rm_layout.addWidget(QtWidgets.QLabel("老板要优化菜单吗？"))
        dish_rm_button = QtWidgets.QPushButton("优化菜单")
        dish_rm_button.clicked.connect(self.remove_dish)
        dish_rm_layout.addWidget(dish_rm_button)
        dish_rm_layout.addStretch()

        # Group 2
        group2_layout = QtWidgets.QVBoxLayout()
        group2_layout.addLayout(dish_rm_layout)
        group2_widget = QtWidgets.QGroupBox("第二阶段")
        group2_widget.setLayout(group2_layout)


        # Group 3
        group3_layout = QtWidgets.QVBoxLayout()
        group3_widget = QtWidgets.QGroupBox("第三阶段")
        group3_widget.setLayout(group3_layout)

        # OK
        self.reset_button = QtWidgets.QPushButton("重置")
        self.reset_button.clicked.connect(self.reset_round)
        self.ok_button = QtWidgets.QPushButton("确认")
        self.ok_button.clicked.connect(self.next_round)

        ok_layout = QtWidgets.QHBoxLayout()
        ok_layout.addStretch()
        ok_layout.addWidget(self.reset_button)
        ok_layout.addWidget(self.ok_button)
        ok_layout.addStretch()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(status_widget)
        self.layout.addWidget(effort_widget)
        self.layout.addWidget(group1_widget)
        self.layout.addWidget(group2_widget)
        self.layout.addWidget(group3_widget)
        self.layout.addLayout(ok_layout)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def set_money_status(self):
        self.money_text.setText(f"老板现有银钱数：{self.money}")

    def set_store_status(self):
        store_str = ", ".join(self.store_list)
        self.store_text.setText(f"老板现有店铺：\n{store_str}")

    def set_new_money_status(self):
        self.new_money_text.setText(f"老板花费银钱数：{self.new_money}")

    def set_new_store_status(self):
        store_str = ", ".join(self.new_store_list)
        self.new_store_text.setText(f"老板购入店铺：\n{store_str}")

    @QtCore.pyqtSlot()
    def buy_ground(self):
        if self.sender():
            cost = int(self.sender().text())
            self.new_money += cost
            self.set_new_money_status()

    @QtCore.pyqtSlot()
    def buy_dishes(self):
        if self.sender():
            dishes_name = self.sender().text()
            cost = self.dishes_dict[dishes_name][0]
            self.new_money += cost
            self.set_new_money_status()

    @QtCore.pyqtSlot()
    def buy_store(self):
        if self.sender():
            store_name = self.sender().text()
            cost = self.store_dict[store_name][0]
            self.new_money += cost
            self.set_new_money_status()
            self.new_store_list.append(store_name)
            self.set_new_store_status()

    @QtCore.pyqtSlot()
    def remove_dish(self):
        if self.sender():
            cost = 3
            self.new_money += cost
            self.set_new_money_status()

    @QtCore.pyqtSlot()
    def reset_round(self):
        self.new_money = 0
        self.new_store_list = []
        self.set_money_status()
        self.set_store_status()
        self.set_new_money_status()
        self.set_new_store_status()

    @QtCore.pyqtSlot()
    def next_round(self):
        self.money -= self.new_money
        self.new_money = 0
        self.store_list.extend(self.new_store_list)
        self.store_list.sort()
        self.new_store_list = []
        self.set_money_status()
        self.set_store_status()
        self.set_new_money_status()
        self.set_new_store_status()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec_())
