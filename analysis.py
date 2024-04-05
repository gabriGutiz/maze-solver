
# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

columns_sub = {
    'algo': 'Algorithm',
    'steps_scale': 'Steps',
    'expansion_rate': 'AvgExpansionRate',
    'time_per_steps': 'AvgTimePerSteps (ms)',
    'time': 'AvgTime (ms)'
}

# %%
df = pd.read_csv('./stats.txt', delimiter=';')

# %%
df['expansion_rate'] = df.nodes / df.steps
df['time_per_steps'] = df.time / df.steps

conditions = [
    (df.steps <= 25),
    (df.steps > 25) & (df.steps <= 50),
    (df.steps > 50) & (df.steps <= 75),
    (df.steps > 75) & (df.steps <= 100),
    (df.steps > 100) & (df.steps <= 200),
    (df.steps > 200) & (df.steps <= 300),
    (df.steps > 300) & (df.steps <= 400),
    (df.steps > 400) & (df.steps <= 500),
    (df.steps > 500) & (df.steps <= 600),
    (df.steps > 600) & (df.steps <= 700),
    (df.steps > 700) & (df.steps <= 800),
    (df.steps > 800) & (df.steps <= 900),
    (df.steps > 900) & (df.steps <= 1000),
    (df.steps > 1000)
]
results = [
    '< 25',
    '25 - 50',
    '50 - 75',
    '75 - 100',
    '100 - 200',
    '200 - 300',
    '300 - 400',
    '400 - 500',
    '500 - 600',
    '600 - 700',
    '700 - 800',
    '800 - 900',
    '900 - 1000',
    '> 1000'
]

order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

df['steps_scale'] = np.select(conditions, results)
df['order'] = np.select(conditions, order)
df

# %%
stats = df[['algo', 'expansion_rate', 'time_per_steps']].groupby(['algo']).mean()
stats = stats.reset_index()

stats = stats.rename(columns=columns_sub)
stats

# %%
stats_scale = df[['algo', 'steps_scale', 'order', 'expansion_rate', 'time_per_steps', 'time']
                 ].groupby(['steps_scale', 'order', 'algo']).mean()

stats_scale = stats_scale.reset_index()
pivot_stats = stats_scale.pivot(index=['steps_scale', 'order'], columns='algo', values=['expansion_rate', 'time_per_steps', 'time'])

pivot_stats = pivot_stats.reset_index()
pivot_stats = pivot_stats.sort_values(['order'])

pivot_stats = pivot_stats.rename(columns=columns_sub)
pivot_stats

# %%
plt.rcParams['figure.figsize'] = [30, 10]
algorithms = stats_scale.algo.unique().tolist()

for algo in algorithms:
    plt.plot(pivot_stats['Steps'], pivot_stats['AvgTime (ms)'][algo], label=algo)

plt.legend()
plt.show()

# %%
plt.rcParams['figure.figsize'] = [30, 10]
stats_per_steps = df[['algo', 'steps', 'time']].groupby(['steps', 'algo']).mean().reset_index()
stats_per_steps = stats_per_steps.pivot(index=['steps'], columns='algo', values='time').reset_index()

for algo in algorithms:
    plt.plot(stats_per_steps['steps'], stats_per_steps[algo], label=algo)

plt.legend()
plt.show()
