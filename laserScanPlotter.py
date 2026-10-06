import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

def plot_one_frame(files):
    fig, axes = plt.subplots(1, len(files), figsize=(6 * len(files), 6), squeeze=False, layout="constrained")
    for ax, filename in zip(axes[0], files):
        path = Path(filename)
        data = np.loadtxt(path, delimiter=",", skiprows=1, ndmin=2)
        scan = data[len(data) // 2]
        ranges = scan[:-2]
        angles = np.arange(len(ranges)) * scan[-2]  # Assumes angle_min = 0
        valid = np.isfinite(ranges)
        ranges, angles = ranges[valid], angles[valid]
        x = ranges * np.cos(angles)
        y = ranges * np.sin(angles)
        np.savetxt(
            path.with_name(path.stem + "_filtered.csv"),
            np.column_stack((ranges, angles, x, y)),
            delimiter=",", header="range_m,angle_rad,x_m,y_m", comments="",
        )
        ax.scatter(x, y, s=5)
        ax.set_title(path.stem.removeprefix("laser_content_").capitalize())
        ax.set_xlabel("X in laser frame (m)")
        ax.set_ylabel("Y in laser frame (m)")
        ax.set_aspect("equal", adjustable="box")
        ax.grid()
    fig.suptitle("Single lidar scan from each motion")
    fig.savefig("laser_scans.png", dpi=200)
    plt.show()


def plot_two_frames(files):
    fig, axes = plt.subplots(
        2, len(files), figsize=(6 * len(files), 12),
        squeeze=False, sharex="col", sharey="col", layout="constrained",
    )
    fig.set_constrained_layout_pads(h_pad=0.15, w_pad=0.15, hspace=0.12, wspace=0.08)

    for column, filename in enumerate(files):
        path = Path(filename)
        data = np.loadtxt(path, delimiter=",", skiprows=1, ndmin=2)
        if len(data) < 25:
            raise ValueError(f"{filename} needs at least 25 scans; found {len(data)}")
        # The 5th and 25th scans have zero-based indices 4 and 24.
        indices = [4, 24]

        for row, index in enumerate(indices):
            ax = axes[row, column]
            frame = index + 1
            scan = data[index]
            ranges = scan[:-2]
            angles = np.arange(len(ranges)) * scan[-2]  # Assumes angle_min = 0

            valid = np.isfinite(ranges)
            ranges, angles = ranges[valid], angles[valid]

            x = ranges * np.cos(angles)
            y = ranges * np.sin(angles)

            np.savetxt(
                path.with_name(path.stem + f"_frame{frame}_filtered.csv"),
                np.column_stack((ranges, angles, x, y)),
                delimiter=",",
                header="range_m,angle_rad,x_m,y_m",
                comments="",
            )

            motion = path.stem.removeprefix("laser_content_").capitalize()
            ax.scatter(x, y, s=5)
            ax.set_title(f"{motion} — frame {frame}")
            ax.set_xlabel("X in laser frame (m)")
            ax.set_ylabel("Y in laser frame (m)")
            ax.set_aspect("equal", adjustable="box")
            ax.grid()

    fig.suptitle("Lidar scans: 5th and 25th frames")
    fig.savefig("laser_scans_2_frames.png", dpi=200)
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--files", nargs="+", required=True)
    parser.add_argument("--frames", type=int, choices=[1, 2], default=1)
    args = parser.parse_args()
    if args.frames == 1:
        plot_one_frame(args.files)
    else:
        plot_two_frames(args.files)
