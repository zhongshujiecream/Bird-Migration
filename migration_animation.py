import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from shapely.geometry import Point, LineString
import numpy as np
import contextily as cx
from IPython.display import HTML # <-- 最终解决方案的关键

# --- 1. 模拟真实的迁徙路线 ---
locations = {
    "Siberian Start": (108.0, 52.0),
    "North China Plain": (117.0, 39.0),
    "Yangtze River Delta": (121.0, 31.0),
    "Poyang Lake": (116.0, 29.0),
    "Guangdong Coast (Destination)": (113.5, 22.5)
}

points_df = gpd.GeoDataFrame(
    geometry=[Point(lon, lat) for lon, lat in locations.values()],
    crs="EPSG:4326"
)
line = LineString(points_df['geometry'].tolist())

# --- 2. 准备动画数据 ---
num_frames = 300
num_birds = 10

smooth_path = [line.interpolate(i / num_frames, normalized=True) for i in range(num_frames + 1)]
path_lons = np.array([p.x for p in smooth_path])
path_lats = np.array([p.y for p in smooth_path])

np.random.seed(42)
bird_paths_lons = []
bird_paths_lats = []
for i in range(num_birds):
    speed_factor = 1 + (i - num_birds / 2) * 0.05 
    offset_lon = np.random.randn(num_frames + 1) * 0.1 * (np.sin(np.linspace(0, 2*np.pi, num_frames + 1)) + 0.5)
    offset_lat = np.random.randn(num_frames + 1) * 0.1 * (np.sin(np.linspace(0, 2*np.pi, num_frames + 1)) + 0.5)
    bird_paths_lons.append(path_lons + offset_lon)
    bird_paths_lats.append(path_lats + offset_lat)

# --- 3. 设置图形和地图 ---
fig, ax = plt.subplots(figsize=(12, 12))
bounds = points_df.total_bounds
ax.set_xlim(bounds[0] - 2, bounds[2] + 2)
ax.set_ylim(bounds[1] - 2, bounds[3] + 2)

cx.add_basemap(ax, crs=points_df.crs.to_string(), source=cx.providers.CartoDB.DarkMatter)
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("2024 Autumn Bird Migration to Guangdong (Simulated Flock)", fontsize=18, fontweight='bold', pad=20, color='white')

# --- 4. 设置动画元素 ---
bird_glows = ax.scatter([], [], s=150, color='yellow', alpha=0.3, zorder=10)
birds = ax.scatter([], [], s=20, color='red', marker='*', zorder=11)

trail_length = 50
trails = []
for _ in range(num_birds):
    trail, = ax.plot([], [], color='orange', linewidth=2, alpha=0.7, zorder=9)
    trails.append(trail)

ax.plot(locations["Siberian Start"][0], locations["Siberian Start"][1], marker='o', markersize=10, color='cyan', label='Starting Point')
ax.plot(locations["Guangdong Coast (Destination)"][0], locations["Guangdong Coast (Destination)"][1], marker='v', markersize=12, color='lime', label='Destination')
ax.legend(loc='upper right', labelcolor='white')

# --- 5. 定义动画更新函数 ---
def animate(i):
    current_lons = [p[i] for p in bird_paths_lons]
    current_lats = [p[i] for p in bird_paths_lats]
    
    birds.set_offsets(np.c_[current_lons, current_lats])
    bird_glows.set_offsets(np.c_[current_lons, current_lats])

    for j in range(num_birds):
        start_index = max(0, i - trail_length)
        trail_lons = bird_paths_lons[j][start_index:i+1]
        trail_lats = bird_paths_lats[j][start_index:i+1]
        trails[j].set_data(trail_lons, trail_lats)
        
    return birds, bird_glows, *trails

# --- 6. 创建并显示动画 ---
ani = FuncAnimation(fig, animate, frames=num_frames, interval=50, blit=False)

# =======================================================
# 这是最终的、绝对有效的显示方式！
plt.close() # 关闭静态图的显示
html_video = ani.to_html5_video()
HTML(html_video)
# =======================================================
