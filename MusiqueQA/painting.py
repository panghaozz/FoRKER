import os
import matplotlib.pyplot as plt
import matplotlib

def painting_from_path(file_path: str, item: str, save_path: str):
    matplotlib.rc("font", family='Microsoft YaHei')
    MESSAGE = item.split("_")
    FORMAT, TIME_DAY, TIME_HOUR, TYPE, LEVEL = MESSAGE[0], MESSAGE[1], MESSAGE[2], MESSAGE[3], MESSAGE[4]
    item_path = item + ".txt"
    full_path = os.path.join(file_path, item_path)
    ACC_LIST = []
    with open(full_path, "r", encoding="utf-8") as file:
        for line in file:
            text = (line.strip())
            if "成功的数量为" in text:
                acc = round(float(text.split("：")[3].split("%")[0]), 2)
                ACC_LIST.append(acc)

    plt.figure(figsize=(20, 10), dpi=100)
    plt.plot(ACC_LIST, color="red")
    y_ticks = range(100)
    plt.yticks(y_ticks[::10])
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("问题数", fontdict={'size': 16})
    plt.ylabel("准确率", fontdict={'size': 16})
    title = "难度：" + LEVEL + " 类型：" + TYPE + " 时间：" + TIME_DAY + "_" + TIME_HOUR
    plt.title(title, fontdict={'size': 20})
    save_item = "picture_" + FORMAT + "_" + TIME_DAY + "_" + TIME_HOUR + "_" + TYPE + "_" + LEVEL + ".png"
    full_save_path = os.path.join(save_path, save_item)
    plt.savefig(full_save_path)
    plt.show()
    print(ACC_LIST)

def painting_from_list(list: list, save_path: str, LEVEL="", TYPE="", TIME="", Epochs = ""):
    matplotlib.rc("font", family='Microsoft YaHei')
    ACC_LIST = list
    plt.figure(figsize=(20, 10), dpi=100)
    plt.plot(ACC_LIST, color="red")
    y_ticks = range(100)
    plt.yticks(y_ticks[::10])
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.xlabel("问题数", fontdict={'size': 16})
    plt.ylabel("准确率", fontdict={'size': 16})
    title = "难度：" + LEVEL + " 类型：" + TYPE + " 时间：" + TIME
    plt.title(title, fontdict={'size': 20})
    save_item = Epochs + "_picture_" + LEVEL + "_" + TYPE + "_" + TIME + ".png"
    full_save_path = os.path.join(save_path, save_item)
    plt.savefig(full_save_path)
    # plt.show()

def run():
    file_path = "result\\SupIdx\\distractor\\V2\\"
    item = "8-4-3-joint_06-04_15-45_result_distractor_test"
    save_path = "result\\SupIdx\\distractor\\PICTURE\\"
    painting_from_path(file_path, item, save_path)

# run()
