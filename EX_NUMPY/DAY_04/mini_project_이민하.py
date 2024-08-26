import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

data = pd.read_csv("Mushroom.csv")
data.drop("Unnamed: 0", axis = 1, inplace = True)

data2 = data.copy()

data2 = data2[["poison", "stalk_shape", "stalk_root", "stalk_surface_above_ring", "stalk_surface_below_ring", "stalk_color_above_ring", "stalk_color_below_ring"]]
data2['stalk_root'] = data2['stalk_root'].replace("missing", np.NAN)

data2.dropna(axis = 0, inplace = True)


# 독버섯과 식용버섯 비율
enable_mushroom_rate = 100 - ((data2["poison"] == "poison").sum() / len(data2) * 100)
poison_mushroom_rate = (data2["poison"] == "poison").sum() / len(data2) * 100

print(enable_mushroom_rate, poison_mushroom_rate)

print(data2["stalk_color_above_ring"].value_counts())

plt.title("독 버섯과 식용 버섯의 비율")
plt.pie([enable_mushroom_rate, poison_mushroom_rate], autopct = "%.1f%%", explode = [0.01, 0.01] , labels = ["enable", "poison"])
plt.legend()
plt.show()

def count_poison_mushroom(data, column):
    count_list = []
    cnt = (data[data['poison'] == 'poison'][column].value_counts())
    
    name_list = cnt.index.values
    for num in cnt:
        count_list.append(num) 
    return dict(zip(name_list, count_list))

def count_enable_mushroom(data, column):
    count_list = []
    cnt = (data[data['poison'] == 'enable'][column].value_counts())
    
    name_list = cnt.index.values
    for num in cnt:
        count_list.append(num) 
    return dict(zip(name_list, count_list))


poison_dict = count_poison_mushroom(data2, 'stalk_shape') 
enable_dict = count_enable_mushroom(data2, 'stalk_shape')

def draw_graph(dict1, dict2, title):
    fig = plt.figure(figsize = (12, 7))
    axes = fig.subplots(1, 2, sharex = True)
    poison_color_list = ["lime", "darkgreen", "mediumslateblue", "blueviolet", "hotpink", "crimson", "blue"]
    enable_color_list = ["bisque", "burlywood", "gold", "lightyellow", "darkorange", 'grey', "coral"]
    axes[0].bar(list(dict1.keys()), list(dict1.values()), edgecolor='black', color = poison_color_list)
    axes[0].set_ylim(0, 3500)
    axes[0].set_title("Poison", size = 15)
    axes[0].legend()
    
    axes[1].bar(list(dict2.keys()), list(dict2.values()), edgecolor='black', color = enable_color_list)
    axes[1].set_ylim(0, 3500)
    axes[1].set_title("Enable", size = 15)
    axes[1].legend()

    plt.suptitle(title)
    plt.show()

draw_graph(poison_dict, enable_dict, "stalk_shape")

poison_dict = count_poison_mushroom(data2, 'stalk_root') 
enable_dict = count_enable_mushroom(data2, 'stalk_root')

draw_graph(poison_dict, enable_dict, "stalk_root")

poison_dict = count_poison_mushroom(data2, 'stalk_surface_above_ring') 
enable_dict = count_enable_mushroom(data2, 'stalk_surface_above_ring')

draw_graph(poison_dict, enable_dict, "stalk_surface_above_ring")

poison_dict = count_poison_mushroom(data2, 'stalk_surface_below_ring') 
enable_dict = count_enable_mushroom(data2, 'stalk_surface_below_ring')

draw_graph(poison_dict, enable_dict, "stalk_surface_below_ring")

poison_dict = count_poison_mushroom(data2, 'stalk_color_above_ring') 
enable_dict = count_enable_mushroom(data2, 'stalk_color_above_ring')


draw_graph(poison_dict, enable_dict, "stalk_color_above_ring")

poison_dict = count_poison_mushroom(data2, 'stalk_color_below_ring') 
enable_dict = count_enable_mushroom(data2, 'stalk_color_below_ring')

draw_graph(poison_dict, enable_dict, "stalk_color_below_ring")


poison_rate = ((data2["stalk_color_above_ring"] != data2["stalk_color_below_ring"]) & (data2["poison"] == "poison")).sum() / (data2["stalk_color_above_ring"] != data2["stalk_color_below_ring"]).sum() * 100
enable_rate = ((data2["stalk_color_above_ring"] != data2["stalk_color_below_ring"]) & (data2["poison"] == "enable")).sum() / (data2["stalk_color_above_ring"] != data2["stalk_color_below_ring"]).sum() * 100

plt.pie([poison_rate, enable_rate], explode = [0.01, 0.01], labels = ['poison_rate', 'enable_rate'], autopct = '%.1f%%', colors = ['#DA70D6', 'gray'])
plt.legend()
plt.title("위 아래 색깔이 다른 버섯의 독버섯 비율")
plt.tight_layout()
plt.show()

poison_rate = ((data2["stalk_surface_above_ring"] != data2["stalk_surface_below_ring"]) & (data2["poison"] == "poison")).sum() / (data2["stalk_surface_above_ring"] != data2["stalk_surface_below_ring"]).sum() * 100
enable_rate = ((data2["stalk_surface_above_ring"] != data2["stalk_surface_below_ring"]) & (data2["poison"] == "enable")).sum() / (data2["stalk_surface_above_ring"] != data2["stalk_surface_below_ring"]).sum() * 100

plt.pie([poison_rate, enable_rate], explode = [0.01, 0.01], labels = ['poison_rate', 'enable_rate'], autopct = '%.1f%%', colors = ['#DA70D6', 'gray'])
plt.legend()
plt.title("위 아래 표면이 다른 버섯의 독버섯 비율")
plt.tight_layout()
plt.show()