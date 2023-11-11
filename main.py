import sys
import typing
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QWidget

class MyWidget(QtWidgets.QWidget):

    # Cost, Benefit, Random?
    dishes_dict = {
        "一等菜": [9, 2, True],
        "二等菜": [6, 3, False],
        "三等菜": [3, 2, False],
        "四等菜": [0, 1, False],
    }

    # Cost, Benefit, Random?
    store_dict = {
        "卦肆": [6, 0, True],
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
        self.eat_dish_list = []
        self.visit_store_list = []

        #
        # Title
        #
        self.title_label = QtWidgets.QLabel("大宋百商图 计算器",
                                            alignment=QtCore.Qt.AlignCenter)
        title_label_font = self.title_label.font()
        title_label_font.setBold(True)
        title_label_font.setPointSize(20)
        self.title_label.setFont(title_label_font)

        #
        # Status Groups
        #
        self.money_text = QtWidgets.QLabel()
        self.store_text = QtWidgets.QLabel()
        self.set_money_status()
        self.set_store_status()

        status_layout = QtWidgets.QVBoxLayout()
        status_layout.addWidget(self.money_text)
        status_layout.addWidget(self.store_text)
        status_widget = QtWidgets.QGroupBox("老板状态")
        status_widget.setLayout(status_layout)

        #
        # Effort Groups
        #
        effort_card_list = ["俭以养德", "门可罗雀", "无尖不商", "时和年丰", "张灯结彩", "银装素裹", "辞旧迎新", "苛捐杂税", "硕果累累"]
        effort_layout = QtWidgets.QGridLayout()
        self.effort_buttons = []
        for idx, key in enumerate(effort_card_list):
            effort_button = QtWidgets.QPushButton(key)
            effort_button.setCheckable(True)
            col_idx = idx // 2
            row_idx = idx % 2
            effort_layout.addWidget(effort_button, row_idx, col_idx)
            self.effort_buttons.append(effort_button)
        effort_widget = QtWidgets.QGroupBox("效果牌")
        effort_widget.setLayout(effort_layout)

        #
        # Group 1
        #
        # Ground dishes
        ground_layout = QtWidgets.QHBoxLayout()
        ground_layout.addWidget(QtWidgets.QLabel("老板要扩展产业吗？"))
        self.ground_button_list = []
        for key in ["0", "2", "3", "4", "7", "8", "9", "10"]:
            ground_button = QtWidgets.QPushButton(key)
            ground_button.setCheckable(True)
            ground_button.clicked.connect(self.buy_ground)
            ground_layout.addWidget(ground_button)
            self.ground_button_list.append(ground_button)
        ground_layout.addStretch()

        # Buy dishes
        dishes_layout = QtWidgets.QHBoxLayout()
        dishes_layout.addWidget(QtWidgets.QLabel("老板要增加菜品吗？"))
        self.dishes_button_list = []
        for key in self.dishes_dict.keys():
            dishes_button = QtWidgets.QPushButton(key)
            dishes_button.setCheckable(True)
            dishes_button.clicked.connect(self.buy_dishes)
            dishes_layout.addWidget(dishes_button)
            self.dishes_button_list.append(dishes_button)
        dishes_layout.addStretch()

        # Store dishes
        store_layout = QtWidgets.QGridLayout()
        for idx, key in enumerate(self.store_dict.keys()):
            store_button = QtWidgets.QPushButton(key)
            store_button.clicked.connect(self.buy_store)
            col_idx = idx // 2
            row_idx = idx % 2
            store_layout.addWidget(store_button, row_idx, col_idx)

        self.new_store_text = QtWidgets.QLabel()
        self.set_new_store_status()

        # Group 1
        group1_layout = QtWidgets.QVBoxLayout()
        group1_layout.addLayout(ground_layout)
        group1_layout.addLayout(dishes_layout)
        group1_layout.addWidget(QtWidgets.QLabel("老板要建设店铺吗？"))
        group1_layout.addLayout(store_layout)
        group1_layout.addWidget(self.new_store_text)
        group1_widget = QtWidgets.QGroupBox("第一阶段")
        group1_widget.setLayout(group1_layout)

        #
        # Group 2
        #
        # Ground dishes
        dish_rm_layout = QtWidgets.QHBoxLayout()
        dish_rm_layout.addWidget(QtWidgets.QLabel("老板要优化菜单吗？"))
        self.dish_rm_button = QtWidgets.QPushButton("优化菜单")
        self.dish_rm_button.setCheckable(True)
        self.dish_rm_button.clicked.connect(self.remove_dish)
        dish_rm_layout.addWidget(self.dish_rm_button)
        dish_rm_layout.addStretch()

        # Group 2
        group2_layout = QtWidgets.QVBoxLayout()
        group2_layout.addLayout(dish_rm_layout)
        group2_widget = QtWidgets.QGroupBox("第二阶段")
        group2_widget.setLayout(group2_layout)

        #
        # Group 3
        #
        # Skip customs
        skip_custom_layout = QtWidgets.QHBoxLayout()
        skip_custom_layout.addWidget(QtWidgets.QLabel("哪位客官来访？"))
        self.skip_button_list = []
        for key in ["1", "2", "3", "4", "5", "6"]:
            skip_custom_button = QtWidgets.QPushButton(key)
            skip_custom_button.setCheckable(True)
            skip_custom_button.clicked.connect(self.skip_custom)
            skip_custom_layout.addWidget(skip_custom_button)
            self.skip_button_list.append(skip_custom_button)
        skip_custom_layout.addStretch()

        # Touzi
        touzi_layout = QtWidgets.QHBoxLayout()
        touzi_layout.addWidget(QtWidgets.QLabel("老板运气好，骰子："))
        self.touzi_edit = QtWidgets.QLineEdit("0")
        touzi_layout.addWidget(self.touzi_edit)
        touzi_layout.addStretch()

        # Eat dishes
        buy_dishes_layout = QtWidgets.QHBoxLayout()
        buy_dishes_layout.addWidget(QtWidgets.QLabel("客官吃点啥？"))
        for key in self.dishes_dict.keys():
            dishes_button = QtWidgets.QPushButton(key)
            dishes_button.clicked.connect(self.eat_dishes)
            buy_dishes_layout.addWidget(dishes_button)
        buy_dishes_layout.addStretch()

        # Visit Store
        visit_store_layout = QtWidgets.QGridLayout()
        self.visit_button_list = []
        for idx, key in enumerate(self.store_dict.keys()):
            store_button = QtWidgets.QPushButton(key)
            store_button.clicked.connect(self.visit_store)
            col_idx = idx // 2
            row_idx = idx % 2
            visit_store_layout.addWidget(store_button, row_idx, col_idx)
            self.visit_button_list.append(store_button)

        self.eat_dish_text = QtWidgets.QLabel()
        self.set_eat_dish_status()
        self.visit_store_text = QtWidgets.QLabel()
        self.set_visit_store_status()

        # Group 3
        group3_layout = QtWidgets.QVBoxLayout()
        group3_layout.addLayout(skip_custom_layout)
        group3_layout.addLayout(touzi_layout)
        group3_layout.addLayout(buy_dishes_layout)
        group3_layout.addWidget(QtWidgets.QLabel("客官逛一逛？"))
        group3_layout.addLayout(visit_store_layout)
        group3_layout.addWidget(self.eat_dish_text)
        group3_layout.addWidget(self.visit_store_text)
        group3_widget = QtWidgets.QGroupBox("第三阶段")
        group3_widget.setLayout(group3_layout)

        #
        # Summary
        #
        self.new_money_text = QtWidgets.QLabel()
        self.set_new_money_status()
        self.manual_add_button = QtWidgets.QPushButton("+")
        self.manual_add_button.clicked.connect(self.manual_add)
        self.manual_sub_button = QtWidgets.QPushButton("-")
        self.manual_sub_button.clicked.connect(self.manual_sub)

        new_money_layout = QtWidgets.QHBoxLayout()
        new_money_layout.addWidget(self.new_money_text)
        new_money_layout.addWidget(self.manual_add_button)
        new_money_layout.addWidget(self.manual_sub_button)
        new_money_layout.addStretch()

        summary_layout = QtWidgets.QVBoxLayout()
        summary_layout.addLayout(new_money_layout)
        summary_widget = QtWidgets.QGroupBox("轮次总结")
        summary_widget.setLayout(summary_layout)

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
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(status_widget)
        self.layout.addWidget(effort_widget)
        self.layout.addWidget(group1_widget)
        self.layout.addWidget(group2_widget)
        self.layout.addWidget(group3_widget)
        self.layout.addWidget(summary_widget)
        self.layout.addLayout(ok_layout)
        self.layout.addStretch()
        self.setLayout(self.layout)

    def set_money_status(self):
        self.money_text.setText(f"老板现有银钱数：{self.money}")

    def set_store_status(self):
        store_str = ", ".join(self.store_list)
        self.store_text.setText(f"老板现有店铺：{store_str}")

    def set_new_money_status(self):
        self.new_money_text.setText(f"老板本轮收益：{self.new_money}")

    def set_new_store_status(self):
        store_str = ", ".join(self.new_store_list)
        self.new_store_text.setText(f"老板购入店铺：{store_str}")

    def set_eat_dish_status(self):
        dish_str = ", ".join(self.eat_dish_list)
        self.eat_dish_text.setText(f"客官点单：{dish_str}")

    def set_visit_store_status(self):
        visit_store = ", ".join(self.visit_store_list)
        self.visit_store_text.setText(f"客官逛店：{visit_store}")

    @QtCore.pyqtSlot()
    def buy_ground(self):
        if self.sender():
            if self.sender().isChecked():
                for item in self.ground_button_list:
                    if item != self.sender():
                        item.setEnabled(False)
                for item in self.dishes_button_list:
                    item.setEnabled(False)

                cost = int(self.sender().text())
                self.new_money = self.new_money - cost
                self.set_new_money_status()
            else:
                for item in self.ground_button_list:
                    if item != self.sender():
                        item.setEnabled(True)
                for item in self.dishes_button_list:
                    item.setEnabled(True)

                cost = int(self.sender().text())
                self.new_money = self.new_money + cost
                self.set_new_money_status()


    @QtCore.pyqtSlot()
    def buy_dishes(self):
        if self.sender():
            if self.sender().isChecked():
                for item in self.ground_button_list:
                    item.setEnabled(False)
                for item in self.dishes_button_list:
                    if item != self.sender():
                        item.setEnabled(False)

                dishes_name = self.sender().text()
                cost = self.dishes_dict[dishes_name][0]
                self.new_money = self.new_money - cost
                self.set_new_money_status()
            else:
                for item in self.ground_button_list:
                    item.setEnabled(True)
                for item in self.dishes_button_list:
                    if item != self.sender():
                        item.setEnabled(True)

                dishes_name = self.sender().text()
                cost = self.dishes_dict[dishes_name][0]
                self.new_money = self.new_money + cost
                self.set_new_money_status()

    @QtCore.pyqtSlot()
    def eat_dishes(self):
        if self.sender():
            dishes_name = self.sender().text()
            cost = self.dishes_dict[dishes_name][1]
            touzi = int(self.touzi_edit.text())
            self.new_money = self.new_money + cost
            if self.dishes_dict[dishes_name][2]:
                self.new_money = self.new_money + touzi

            if self.dishes_dict[dishes_name][2]:
                self.eat_dish_list.append(dishes_name + f"(骰子{touzi})")
            else:
                self.eat_dish_list.append(dishes_name)

            self.set_new_money_status()
            self.set_eat_dish_status()
            self.touzi_edit.setText("0")

    @QtCore.pyqtSlot()
    def buy_store(self):
        if self.sender():
            store_name = self.sender().text()
            cost = self.store_dict[store_name][0]
            self.new_money = self.new_money - cost
            self.set_new_money_status()
            self.new_store_list.append(store_name)
            self.set_new_store_status()

    @QtCore.pyqtSlot()
    def visit_store(self):
        if self.sender():
            store_name = self.sender().text()
            effort_name = ""
            for item in self.effort_buttons:
                if item.isChecked():
                    effort_name = item.text()

            benefit = 0
            total_store_list = self.store_list + self.new_store_list
            for own_store_item in total_store_list:
                if own_store_item != store_name:
                    continue

                # Calculate benefit
                if store_name == "卦肆":
                    touzi = int(self.touzi_edit.text())
                    benefit = benefit + touzi + total_store_list.count("关扑铺") * 2
                elif store_name == "蹴鞠场":
                    benefit = benefit + 0
                elif store_name == "书坊":
                    benefit = benefit + 3 + total_store_list.count("茶馆")
                elif store_name == "酒肆":
                    benefit = benefit + len(self.eat_dish_list) + 1 + total_store_list.count("说书场")
                elif store_name == "绸缎庄":
                    benefit = benefit + 4 + total_store_list.count("首饰铺")
                elif store_name == "勾栏瓦舍":
                    benefit = benefit + len(total_store_list)
                elif store_name == "瓷器铺":
                    benefit = benefit + 6 + total_store_list.count("首饰铺")
                elif store_name == "饮子铺":
                    benefit = benefit + 2 + total_store_list.count("说书场")
                elif store_name == "说书场":
                    benefit = benefit + 2 + total_store_list.count("首饰铺")
                elif store_name == "关扑铺":
                    benefit = benefit + 2 + total_store_list.count("饮子铺") * 2
                elif store_name == "首饰铺":
                    benefit = benefit + 2
                elif store_name == "茶馆":
                    benefit = benefit + 2 + total_store_list.count("说书场")

                if effort_name == "无尖不商":
                    benefit = benefit - 1

            self.visit_store_list.append(f"{store_name}({benefit})")
            self.new_money = self.new_money + benefit

            self.set_new_money_status()
            self.set_visit_store_status()
            self.sender().setEnabled(False)

    @QtCore.pyqtSlot()
    def remove_dish(self):
        if self.sender():
            if self.sender().isChecked():
                cost = 3
                self.new_money = self.new_money - cost
                self.set_new_money_status()
            else:
                cost = 3
                self.new_money = self.new_money + cost
                self.set_new_money_status()

    @QtCore.pyqtSlot()
    def skip_custom(self):
        if self.sender():
            if self.sender().isChecked():
                for item in self.skip_button_list:
                    if item != self.sender():
                        item.setEnabled(False)

                custom_idx = int(self.sender().text())
                cost = custom_idx - 1
                self.new_money = self.new_money - cost
                self.set_new_money_status()
            else:
                for item in self.skip_button_list:
                    if item != self.sender():
                        item.setEnabled(True)

                custom_idx = int(self.sender().text())
                cost = custom_idx - 1
                self.new_money = self.new_money + cost
                self.set_new_money_status()

    @QtCore.pyqtSlot()
    def manual_add(self):
        self.new_money = self.new_money + 1
        self.set_new_money_status()

    @QtCore.pyqtSlot()
    def manual_sub(self):
        self.new_money = self.new_money - 1
        self.set_new_money_status()

    @QtCore.pyqtSlot()
    def reset_round(self):
        for item in self.ground_button_list:
            item.setEnabled(True)
            item.setChecked(False)
        for item in self.dishes_button_list:
            item.setEnabled(True)
            item.setChecked(False)
        self.dish_rm_button.setChecked(False)
        for item in self.skip_button_list:
            item.setEnabled(True)
            item.setChecked(False)
        for item in self.visit_button_list:
            item.setEnabled(True)

        self.new_money = 0
        self.new_store_list = []
        self.eat_dish_list = []
        self.visit_store_list = []
        self.set_new_money_status()
        self.set_new_store_status()
        self.set_eat_dish_status()
        self.set_visit_store_status()

    @QtCore.pyqtSlot()
    def next_round(self):
        self.money = self.money + self.new_money
        self.store_list.extend(self.new_store_list)
        self.store_list.sort()
        self.set_money_status()
        self.set_store_status()

        self.reset_round()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec_())
