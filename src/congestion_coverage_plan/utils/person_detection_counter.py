import argparse
from pathlib import Path
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


MADAMA3_FIG_SIZE = [-21.2, 36.4, -53.4, 9.2]
MADAMA_FIG_SIZE = [0, 72, 72, 0]


def load_detection_data(dataset_path: Path) -> pd.DataFrame:
    data = pd.read_csv(dataset_path, header=None)
    column_count = data.shape[1]

    if column_count == 6:
        data.columns = ["time", "person_id", "x", "y", "value_1", "value_2"]
    elif column_count == 8:
        data.columns = ["time", "person_id", "x", "y", "z", "value_1", "value_2", "value_3"]
    else:
        raise ValueError(
            f"Unsupported dataset format with {column_count} columns. Expected 6 or 8 columns."
        )

    data["person_id"] = data["person_id"].astype("int64")
    return data


def get_person_ids_above_threshold(dataset_path: Path, threshold: int) -> pd.Series:
    data = load_detection_data(dataset_path)
    detection_counts = data.groupby("person_id").size().sort_values(ascending=False)
    return detection_counts[detection_counts > threshold]


def get_matching_detections(dataset_path: Path, matching_people: pd.Series) -> pd.DataFrame:
    data = load_detection_data(dataset_path)
    return data[data["person_id"].isin(matching_people.index)].copy()


def limit_matching_people(matching_people: pd.Series, max_people: int | None) -> pd.Series:
    if max_people is None:
        return matching_people
    return matching_people.head(max_people)


def shift_each_person_time_to_zero(detections: pd.DataFrame) -> pd.DataFrame:
    shifted = detections.copy()
    min_time_per_person = shifted.groupby("person_id")["time"].transform("min")
    shifted["time"] = np.round(shifted["time"] - min_time_per_person, 10)
    return shifted


def save_matching_detections(
    dataset_path: Path,
    matching_people: pd.Series,
    output_path: Path,
    start_from_zero: bool = False,
) -> None:
    matching_detections = get_matching_detections(dataset_path, matching_people)
    if start_from_zero:
        matching_detections = shift_each_person_time_to_zero(matching_detections)
    matching_detections["person_id"] = matching_detections["person_id"].astype("int64")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    matching_detections.to_csv(output_path, index=False, header=False)
    print(f"Saved {len(matching_detections)} detections to {output_path}")


def resample_detections_to_time_step(detections: pd.DataFrame, time_step: float) -> pd.DataFrame:
    if time_step <= 0:
        raise ValueError("time_step must be greater than zero")

    if detections.empty:
        return detections.copy()

    time_step = float(time_step)
    resampled_frames = []

    for person_id, person_data in detections.groupby("person_id"):
        person_data = person_data.sort_values("time").copy()
        start_time = float(person_data.iloc[0]["time"])
        detection_count = len(person_data)
        person_data.loc[:, "time"] = np.round(
            start_time + np.arange(detection_count, dtype=float) * time_step,
            10,
        )
        resampled_frames.append(person_data)

    return pd.concat(resampled_frames, ignore_index=True).sort_values(["person_id", "time"]).reset_index(drop=True)


def format_time_step_label(time_step: float) -> str:
    numeric_time_step = float(time_step)
    if numeric_time_step.is_integer():
        return f"{int(numeric_time_step)}s"
    return f"{str(numeric_time_step).replace('.', 'p')}s"


def resolve_resample_output_path(
    dataset_path: Path,
    output_path: Path | None,
    time_step: float,
) -> Path:
    time_step_label = format_time_step_label(time_step)

    if output_path is None:
        return dataset_path.with_name(f"{dataset_path.stem}_{time_step_label}{dataset_path.suffix}")

    updated_name = output_path.name.replace("{time_step}", time_step_label)
    if updated_name != output_path.name:
        return output_path.with_name(updated_name)

    updated_stem = re.sub(r"_\d+(?:p\d+)?s$", f"_{time_step_label}", output_path.stem)
    if updated_stem == output_path.stem:
        updated_stem = f"{output_path.stem}_{time_step_label}"

    return output_path.with_name(f"{updated_stem}{output_path.suffix}")


def resolve_interpolated_output_path(
    dataset_path: Path,
    output_path: Path | None,
    time_step: float,
) -> Path:
    time_step_label = format_time_step_label(time_step)

    if output_path is None:
        return dataset_path.with_name(
            f"{dataset_path.stem}_interp_{time_step_label}{dataset_path.suffix}"
        )

    updated_name = output_path.name.replace("{time_step}", time_step_label)
    if updated_name != output_path.name:
        return output_path.with_name(updated_name)

    updated_stem = re.sub(r"_interp_\d+(?:p\d+)?s$", f"_interp_{time_step_label}", output_path.stem)
    if updated_stem == output_path.stem:
        updated_stem = f"{output_path.stem}_interp_{time_step_label}"

    return output_path.with_name(f"{updated_stem}{output_path.suffix}")


def save_resampled_detections(
    dataset_path: Path,
    output_path: Path,
    time_step: float,
    start_from_zero: bool = False,
    person_ids: pd.Index | None = None,
) -> None:
    detections = load_detection_data(dataset_path)
    if person_ids is not None:
        detections = detections[detections["person_id"].isin(person_ids)].copy()
    resampled_detections = resample_detections_to_time_step(detections, time_step)
    if start_from_zero:
        resampled_detections = shift_each_person_time_to_zero(resampled_detections)
    resampled_detections["person_id"] = resampled_detections["person_id"].astype("int64")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    resampled_detections.to_csv(output_path, index=False, header=False)
    print(
        f"Saved {len(resampled_detections)} detections with time step {time_step} to {output_path}"
    )


def interpolate_detections_to_time_step(detections: pd.DataFrame, time_step: float) -> pd.DataFrame:
    if time_step <= 0:
        raise ValueError("time_step must be greater than zero")

    if detections.empty:
        return detections.copy()

    time_step = float(time_step)
    interpolated_frames = []
    value_columns = [column for column in detections.columns if column not in {"time", "person_id"}]

    for person_id, person_data in detections.groupby("person_id"):
        person_data = person_data.sort_values("time").drop_duplicates(subset=["time"])
        person_rows = []

        for row_index in range(len(person_data) - 1):
            start_row = person_data.iloc[row_index]
            end_row = person_data.iloc[row_index + 1]
            person_rows.append(start_row.to_dict())

            gap = float(end_row["time"] - start_row["time"])
            if gap <= time_step:
                continue

            intermediate_times = np.arange(
                float(start_row["time"]) + time_step,
                float(end_row["time"]),
                time_step,
            )
            intermediate_times = np.round(intermediate_times, 10)

            for intermediate_time in intermediate_times:
                interpolation_ratio = (intermediate_time - float(start_row["time"])) / gap
                interpolated_row = {
                    "time": intermediate_time,
                    "person_id": int(person_id),
                }
                for column in value_columns:
                    start_value = float(start_row[column])
                    end_value = float(end_row[column])
                    interpolated_row[column] = start_value + interpolation_ratio * (end_value - start_value)
                person_rows.append(interpolated_row)

        person_rows.append(person_data.iloc[-1].to_dict())
        interpolated_person_data = pd.DataFrame(person_rows, columns=["time", "person_id", *value_columns])
        interpolated_frames.append(interpolated_person_data)

    interpolated_detections = pd.concat(interpolated_frames, ignore_index=True)
    interpolated_detections["person_id"] = interpolated_detections["person_id"].astype("int64")
    return interpolated_detections.sort_values(["person_id", "time"]).reset_index(drop=True)


def save_interpolated_detections(
    dataset_path: Path,
    output_path: Path,
    time_step: float,
    start_from_zero: bool = False,
    person_ids: pd.Index | None = None,
) -> None:
    detections = load_detection_data(dataset_path)
    if person_ids is not None:
        detections = detections[detections["person_id"].isin(person_ids)].copy()
    interpolated_detections = interpolate_detections_to_time_step(detections, time_step)
    if start_from_zero:
        interpolated_detections = shift_each_person_time_to_zero(interpolated_detections)
    interpolated_detections["person_id"] = interpolated_detections["person_id"].astype("int64")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    interpolated_detections.to_csv(output_path, index=False, header=False)
    print(
        f"Saved {len(interpolated_detections)} interpolated detections with time step {time_step} to {output_path}"
    )


def infer_map_configuration(dataset_path: Path) -> tuple[Path | None, list[float] | None]:
    dataset_name = dataset_path.name
    repo_root = dataset_path.resolve().parents[3]

    if dataset_name == "madama3_september.csv":
        return repo_root / "data" / "maps" / "madama3.jpg", MADAMA3_FIG_SIZE
    if dataset_name in {"madama_reduced_decimals.csv", "madama.csv"}:
        return repo_root / "data" / "maps" / "madama.png", MADAMA_FIG_SIZE

    return None, None


def plot_matching_people(
    dataset_path: Path,
    matching_people: pd.Series,
    threshold: int,
    map_path: Path | None,
    fig_size: list[float] | None,
    save_plot: Path | None,
    map_extent: list[float] | None = None,
) -> None:
    matching_data = get_matching_detections(dataset_path, matching_people)

    figure, axis = plt.subplots(figsize=(12, 8))

    if map_path is not None and map_path.exists():
        image = plt.imread(map_path)
        if map_extent is not None:
            axis.imshow(image, cmap="gray", vmin=0, vmax=255, extent=map_extent)
        elif fig_size is not None:
            axis.imshow(image, cmap="gray", vmin=0, vmax=255, extent=fig_size)
        else:
            x_min, x_max = matching_data["x"].min(), matching_data["x"].max()
            y_min, y_max = matching_data["y"].min(), matching_data["y"].max()
            x_pad = max((x_max - x_min) * 0.05, 1.0)
            y_pad = max((y_max - y_min) * 0.05, 1.0)
            inferred_extent = [x_min - x_pad, x_max + x_pad, y_min - y_pad, y_max + y_pad]
            axis.imshow(image, cmap="gray", vmin=0, vmax=255, extent=inferred_extent)

    for person_id, person_data in matching_data.groupby("person_id"):
        axis.plot(person_data["x"], person_data["y"], marker="o", markersize=2, linewidth=1, label=str(int(person_id)))

    axis.set_title(f"People with detections > {threshold}")
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.legend(loc="upper right", fontsize=8, ncol=2)
    axis.set_aspect("equal")

    if save_plot is not None:
        figure.savefig(save_plot, dpi=200, bbox_inches="tight")
        print(f"Plot saved to {save_plot}")

    plt.show()


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Return person IDs whose number of detections is higher than a chosen threshold."
    )
    parser.add_argument("dataset", type=Path, help="Path to the detections CSV file.")
    parser.add_argument(
        "threshold",
        type=int,
        help="Minimum number of detections required. Only IDs with detections strictly greater than this value are returned.",
    )
    parser.add_argument(
        "--plot",
        action="store_true",
        help="Plot the matching persons on the associated map when a known map is available.",
    )
    parser.add_argument(
        "--map-path",
        type=Path,
        default=None,
        help="Override the map image path used for plotting.",
    )
    parser.add_argument(
        "--save-plot",
        type=Path,
        default=None,
        help="Save the generated plot to this file path.",
    )
    parser.add_argument(
        "--map-extent",
        type=float,
        nargs=4,
        metavar=("XMIN", "XMAX", "YMIN", "YMAX"),
        default=None,
        help="Optional map extent for plotting background image: xmin xmax ymin ymax.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Write the matching detection rows to this CSV file.",
    )
    parser.add_argument(
        "--resample-output",
        type=Path,
        default=None,
        help="Write a resampled copy of the input detections to this CSV file. The file name is adjusted to match the selected time step.",
    )
    parser.add_argument(
        "--time-step",
        type=float,
        default=None,
        help="Target time step for resampling or interpolation, for example 1.0 or 0.5.",
    )
    parser.add_argument(
        "--interpolate-output",
        type=Path,
        default=None,
        help="Write a linearly interpolated copy of the input detections to this CSV file.",
    )
    parser.add_argument(
        "--start-from-zero",
        action="store_true",
        help="Shift timestamps independently per person so each trajectory starts at time 0.",
    )
    parser.add_argument(
        "--max-people",
        type=int,
        default=None,
        help="Limit outputs and plot to the top N matching people by detection count.",
    )
    return parser


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()

    if args.max_people is not None and args.max_people <= 0:
        parser.error("--max-people must be greater than zero")

    matching_people = get_person_ids_above_threshold(args.dataset, args.threshold)
    matching_people = limit_matching_people(matching_people, args.max_people)
    needs_threshold_matches = args.output is not None or args.plot

    if args.resample_output is not None or args.time_step is not None:
        if args.time_step is None:
            parser.error("Resampling requires --time-step")
        if args.resample_output is not None:
            resolved_resample_output = resolve_resample_output_path(
                args.dataset,
                args.resample_output,
                args.time_step,
            )
            save_resampled_detections(
                args.dataset,
                resolved_resample_output,
                args.time_step,
                start_from_zero=args.start_from_zero,
                person_ids=matching_people.index if args.max_people is not None else None,
            )

    if args.interpolate_output is not None:
        if args.time_step is None:
            parser.error("Interpolation requires --time-step")
        resolved_interpolated_output = resolve_interpolated_output_path(
            args.dataset,
            args.interpolate_output,
            args.time_step,
        )
        save_interpolated_detections(
            args.dataset,
            resolved_interpolated_output,
            args.time_step,
            start_from_zero=args.start_from_zero,
            person_ids=matching_people.index if args.max_people is not None else None,
        )

    if matching_people.empty:
        if needs_threshold_matches:
            print(f"No person IDs found with more than {args.threshold} detections.")
            return 0
        return 0

    print("person_id,detections")
    for person_id, detection_count in matching_people.items():
        print(f"{int(person_id)},{int(detection_count)}")

    if args.output is not None:
        save_matching_detections(
            args.dataset,
            matching_people,
            args.output,
            start_from_zero=args.start_from_zero,
        )

    if args.plot:
        inferred_map_path, fig_size = infer_map_configuration(args.dataset)
        map_path = args.map_path if args.map_path is not None else inferred_map_path
        map_extent = list(args.map_extent) if args.map_extent is not None else None
        plot_matching_people(
            args.dataset,
            matching_people,
            args.threshold,
            map_path,
            fig_size,
            args.save_plot,
            map_extent,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())