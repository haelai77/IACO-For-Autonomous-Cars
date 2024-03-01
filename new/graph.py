import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import BSpline, splrep, splev

# 0 to 11 graphs
directory_prefix = "./unordered_batches/unordered_batch_"
density = 3.0
alpha = 10
file = f"density_{density}__alpha_{alpha}"

chunk_size = 1000
timestep_per_run = 20000

max_of_means = []
min_of_means = []
mean_of_means = []

time_steps = [str(i+1000) for i in range(0, 20000, 1000)]
batches = [i for i in range(0, 100)]
means_of_batches = pd.DataFrame(index = batches, columns=time_steps)
# columns are for each time step
# rows are for each batch
# mean of means = mean of columns

# fill means_of_batches data frame
for j in range(0, 100):
    data = pd.read_csv(f"{directory_prefix}{j}/{file}.csv")

    # append means for each folder in directories to means data frame
    for k in range(0, len(data), chunk_size): 
        chunk = data.iloc[k:k+chunk_size, 2].mean()
        if chunk == 0: print(j, k)
        means_of_batches.loc[j, str(k+1000)] = chunk

# calculate means
for i in time_steps:
    time_step_data = means_of_batches.loc[:, i]
    mean_of_means.append(time_step_data.mean())
    min_of_means.append(time_step_data.min())
    max_of_means.append(time_step_data.max())


# draw graph
plt.figure(figsize=(7, 4))
plt.margins(x=0)
plt.ylim(0, 100)
plt.xticks(rotation=55)
plt.yticks(ticks=[i for i in range(0, 101, 10)])

plt.plot(time_steps, min_of_means, color='blue', linestyle='--', linewidth=1.2)
plt.plot(time_steps, max_of_means, color='red', linestyle='--', linewidth=1.2)
plt.plot(time_steps, mean_of_means, color='purple', linewidth=1.2)


plt.title(f'{file}')
plt.xlabel('Time')
plt.ylabel('Average Density')
plt.legend(["mins", "maxs", "means"])

plt.grid(True)
plt.tight_layout()
plt.show()



# # Step 1: Read data from the CSV file
# data = pd.read_csv('unordered_batch_0/density_2.9__alpha_10.csv')

# # Step 2: Compute the average of every 1000 rows for the mean values
# chunk_size = 1000
# mins = []
# maxs = []
# means = []

# for i in range(0, len(data), chunk_size):
#     chunk = data.iloc[i:i+chunk_size, :]
#     mins.append(chunk.iloc[:, 0].mean())
#     maxs.append(chunk.iloc[:, 1].mean())
#     means.append(chunk.iloc[:, 2].mean())

# x = range(1000, 20001, chunk_size)

# # Step 3: Plot the graph
# xticks = [1000]
# xticks.extend([i for i in range(3000, 20001, 1000)])


# plt.figure(figsize=(12, 6))
# plt.xlim(1000, 20000)
# plt.ylim(0, 100)
# plt.xticks(ticks=xticks)
# plt.yticks(ticks=[i for i in range(0, 101, 10)])

# plt.plot(x, mins, color='blue', linestyle='--')
# plt.plot(x, maxs, color='red', linestyle='--')
# plt.plot(x, means, color='purple')

# plt.legend(["mins", "maxs", "means"])

# plt.title('Average Density Over Time')
# plt.xlabel('Time')
# plt.ylabel('Average Density')

# plt.grid(True)
# plt.show()

