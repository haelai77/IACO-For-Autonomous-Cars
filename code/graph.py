import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import BSpline, splrep, splev
from ast import literal_eval
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("-density", default=2.3)
# parser.add_argument("-alpha", default=0)
# args = parser.parse_args()

# # 0 to 11 graphs
# density = args.density
# alpha = args.alpha
# directory_prefix = f"../output/out_directory/density_{density}__alpha_{alpha}/"
# file = f"density_{density}__alpha_{alpha}"

# chunk_size = 1000
# t_max = 20000

# max_of_means = []
# min_of_means = []
# mean_of_means = []

# time_steps = [str(i+1000) for i in range(0, t_max, chunk_size)]
# batches = [i for i in range(1, 1001)]

# # holds data points for each individual simulation  (row = sim, col = time step)
# batches_of_means = pd.DataFrame(index = batches, columns=time_steps)


# # puts the means into the batches of means
# for row in range(1, 11): #1000):
#     data = pd.read_csv(f"{directory_prefix}{row}_{file}.out", sep=" ",names=["min", "max", "mean", "finished"])

#     for col in range(0, t_max, chunk_size): 
#         chunk = data.iloc[col:(col+chunk_size), 2].mean()
#         if chunk == 0: print(col, row)
#         batches_of_means.loc[row, str(col+1000)] = chunk

# # 
# for i in time_steps:
#     time_step_data = batches_of_means.loc[:, i]
#     mean_of_means.append(time_step_data.mean())
#     min_of_means.append(time_step_data.min())
#     max_of_means.append(time_step_data.max())


# # draw graph
# plt.figure(figsize=(7, 4))
# plt.margins(x=0)
# plt.ylim(0, 100)
# plt.xticks(rotation=55)
# plt.yticks(ticks=[i for i in range(0, 101, 10)])

# plt.plot(time_steps, min_of_means, color='blue', linestyle='--', linewidth=1.2)
# plt.plot(time_steps, max_of_means, color='red', linestyle='--', linewidth=1.2)
# plt.plot(time_steps, mean_of_means, color='purple', linewidth=1.2)


# plt.title(f'{file}')
# plt.xlabel('Time')
# plt.ylabel('Average Density')
# plt.legend(["mins", "maxs", "means"])

# plt.grid(True)
# plt.tight_layout()
# plt.show()
# plt.savefig("fig.png")
########################################
# itereate through every directory,
# take mean of last 1000 of all files
# take max mean of last 1000 out of all files
# take min mean of last 1000 out of all files

#plot average delay, y, against density, x.

alpha = 10
densities = [i/10 for i in range(23, 30+1)] 
p_drops = [i/100 for i in range(10, 101, 5)]
p_drop_indexes = [i for i in range(1, 101)]
print(densities)

mins_p_drop = []
maxs_p_drop = []
means_p_drop = []

for i, p in enumerate(p_drops):
    means_within_100 = []
    for sim_num in p_drop_indexes:
        file = f"../results/poster_day_p_dropoff/density_3.0__alpha_10_p_drop_{p}/{sim_num}_density_3.0__alpha_10_p_drop_{p}"
        print(file)
        data = pd.read_csv(f"{file}.out", sep=" ", header=None, names=["min", "max", "mean", "finished"])
        means_within_100.append(data.iloc[19000: , 2].mean())

    means_p_drop.append( sum(means_within_100) / len(means_within_100))
    mins_p_drop.append( min(i for i in means_within_100 if i > 0))
    maxs_p_drop.append( max(i for i in means_within_100 if i > 0))

# draw graph
plt.figure(figsize=(7, 4))
plt.margins(x=0)
plt.ylim(0, 100)
plt.xticks(rotation=55)
plt.yticks(ticks=[i for i in range(0, 101, 10)])

plt.plot(p_drops, mins_p_drop, color='blue', linestyle='--', linewidth=1.2)
plt.plot(p_drops, maxs_p_drop, color='red', linestyle='--', linewidth=1.2)
plt.plot(p_drops, means_p_drop, color='purple', linewidth=1.2)


plt.title(f'{file}')
plt.xlabel('Time')
plt.ylabel('Average Density')
plt.legend(["mins", "maxs", "means"])

plt.grid(True)
plt.tight_layout()
plt.show()