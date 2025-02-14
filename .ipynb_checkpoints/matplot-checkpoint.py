import matplotlib.pyplot as plt
x = [    "17:02:43.517",    "17:02:35.484",    "17:02:33.473",    "17:01:04.041",    "17:00:57.002",    "17:00:43.941",    "17:00:41.944",    "17:00:05.785",    "17:00:02.771",    "16:59:09.502",    "16:59:00.446",    "16:58:59.441",    "16:58:54.417",    "16:58:53.411",    "16:58:43.375",    "16:55:56.574",    "16:55:54.563",    "16:54:34.207",    "16:54:30.191",    "16:34:19.979",    "16:34:17.979",    "16:32:53.52",    "16:32:51.512"]

y = [    -91,    -83,    -81,    -80,    -84,    -86,    -80,    -80,    -80,    -88,    -81,    -86,    -82,    -81,    -83,    -89,    -82,    -79,    -83,    -88,    -80,    -89,    -80]


plt.figure(figsize=(10, 6))
plt.scatter(range(len(x)), y, color='black', label='RSSI values')
plt.xlabel("Time (s)")
plt.ylabel("RSSI (dbm)")
plt.title("RSSI comparison for open_v/s_pidi: open_pcb")
plt.xticks(range(len(x)), x, rotation=90, fontsize=5)
plt.plot(x,y)
plt.show()

# import matplotlib.pyplot as plt
# x = [0, 2, 4, 6, 8]
# y = [0, 4, 16, 36, 64]
# fig, ax = plt.subplots()
# ax.plot(x, y, marker='o', label="Data Points")
# ax.set_title("Basic Components of Matplotlib Figure")
# ax.set_xlabel("X-Axis")
# ax.set_ylabel("Y-Axis")
# plt.show()