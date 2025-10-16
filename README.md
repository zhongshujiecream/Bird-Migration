migration_animation.py
======================

Overview
--------
`migration_animation.py` is an example script that uses GeoPandas, Matplotlib and Contextily to simulate and visualize bird migration paths. The script creates a smooth migration route from Siberia through the North China Plain and the Yangtze River Delta to the Guangdong coast, and generates multiple "bird" trajectories with jitter and trailing effects. The animation is exported as an HTML5 video for convenient display inside a Jupyter notebook.

Key features
------------
- Generates a smooth migration path using linear interpolation along geographic waypoints
- Creates multiple individual bird tracks with random offsets to simulate flock dispersion
- Renders glow points and trailing lines for each bird, with configurable frame count and flock size
- Adds a dark-themed basemap via Contextily for geographic context

Dependencies (major)
--------------------
- Python 3.8+
- geopandas
- matplotlib
- numpy
- shapely
- contextily
- IPython (used to display the HTML5 video in Jupyter)

Note: This repository already contains a `requirements.txt` file. Installing from it is recommended.

Quick start
-----------
1) Install dependencies (recommended)

Windows PowerShell:

```powershell
python -m pip install -r requirements.txt
```

Or install packages individually:

```powershell
python -m pip install geopandas matplotlib numpy shapely contextily ipython
```

2) Run in Jupyter Notebook / JupyterLab (recommended)

Open `migration_animation.py` (or copy the code into a notebook cell) and run it inside a Jupyter environment. The script produces an animation and embeds it as an HTML5 video using `IPython.display.HTML`. This is the most convenient way to view the result.

3) Run as a script and save a video file (optional)

By default the script calls `ani.to_html5_video()` and displays the result via `IPython.display.HTML`. That display method does not produce an interactive popup when run in a non-interactive shell. To run from the command line and save to an MP4 or GIF file:

- Install `ffmpeg` (for MP4) or `imagemagick` (for GIF) and ensure the binary is available on your system PATH.
- Add saving logic to the end of the script or replace the display code, for example:

```python
# Replace the HTML display at the end and save to MP4
ani.save('migration_animation.mp4', writer='ffmpeg', fps=20)
print('Saved migration_animation.mp4')
```

Run:

```powershell
python migration_animation.py
```

Troubleshooting & debugging
---------------------------
- Basemap tiles misaligned / CRS issues:
  - `contextily` typically expects Web Mercator coordinates (`EPSG:3857`). If the basemap does not align with your features, convert the GeoDataFrame or geometries using `to_crs(epsg=3857)` and plot using that CRS.
- Contextily tile download failures:
  - Check network connectivity or try a different provider from `cx.providers` (the script currently uses `CartoDB.DarkMatter`).
- Saving MP4 fails:
  - Make sure `ffmpeg` is installed and available on the command line, or use GIF export via ImageMagick.
- No visible output when running as a script:
  - The script is configured to produce notebook-friendly HTML output. When running in a plain terminal, either save the animation to a file or call `plt.show()` to open an interactive window (requires a graphical environment).

Advanced tips
-------------
- For more geospatially accurate display, convert both the path coordinates and the basemap to `EPSG:3857` and use GeoAxes for plotting.
- Consider adding command-line options (via `argparse`) to expose parameters such as flock size, trail length, frame count, output filename, and colors.

Files
-----
- `migration_animation.py`: The main script (this README is based on that file)
- `requirements.txt`: Recommended Python dependency list

License
-------
Add a license as desired for your repository. This README does not specify a license—treat the code as an educational/demonstration example unless you choose otherwise.

Contact
-------
If you would like me to change the script to save video files directly or convert it into a notebook (`.ipynb`), tell me the desired output format and resolution and I will update the code accordingly.
