import matplotlib.pyplot as plt
# ID 1325 106905 stars 0.1:0 cluster; 0.15:0 cluster;  0.212,:12clusters;  0.25:58 clusters;  0.3:469 clusters;
# id 76 (107417 stars):0.1:0 cluster; 0.15:0 cluster;  0.2:1clusters;  0.25:58 clusters;  0.3:238 clusters;
# id 14 (64011 stars):0.1:0 cluster; 0.15:0 cluster;  0.2:1clusters;  0.25:1 clusters;  0.3:21 clusters;

# id 67 (82124 stars):0.1:0 cluster; 0.15:0 cluster;  0.2:14 clusters;  0.25:113 clusters;  0.3:212 clusters;
# id 18( 58714stars)  0.08 :22 clusters  0.1:17 clusters; 0.12: 4 clusters; 0.15:1 cluster;  0.2: 1 clusters; 0.25: 2 clusters; 0.3:6 cluster

SMALL_SIZE = 12
MEDIUM_SIZE = 14
BIGGER_SIZE = 25
MARKERSIZE=3
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=10)

fig = plt.figure(figsize=(8, 6))
ax1 = fig.add_subplot(1, 1, 1, facecolor="#f5f6f7")
para=[0.01,0.1,0.2,0.3,0.5,0.8,1.0,1.2,1.5]
id_1325=[0,0,12,58,469]
id_76=[0,0,1,58,238]
id_14=[0,0,1,1,21]
id_67=[0,0,14,113,212]
id_18=[17,1,1,2,6]
id_m67=[0,2,10,60,2,2,3,1,1]

plt.plot(para, id_m67, '.-', c='red',label="M67")

plt.xlabel('$b_{FoF}$')
plt.ylabel('Number of Clusters')
plt.legend()
plt.savefig('fof_link_M67' + ".pdf", format='pdf', dpi=100, bbox_inches='tight')
plt.show()
