import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


@dataclass
class TrajectoryTemplate:
    times: np.ndarray
    positions: np.ndarray
    start: np.ndarray
    end: np.ndarray


def load_trajectory_data(dataset_path: Path) -> pd.DataFrame:
    data = pd.read_csv(dataset_path, header=None)
    column_count = data.shape[1]

    if column_count == 6:
        data.columns = ["time", "person_id", "x", "y", "velocity", "motion_angle"]
    elif column_count == 8:
        data.columns = ["time", "person_id", "x", "y", "z", "velocity", "motion_angle", "facing_angle"]
    else:
        raise ValueError(
            f"Unsupported dataset format with {column_count} columns. Expected 6 or 8 columns."
        )

    numeric_columns = ["time", "person_id", "x", "y"]
    data[numeric_columns] = data[numeric_columns].apply(pd.to_numeric, errors="coerce")
    data = data.dropna(subset=numeric_columns)
    data["person_id"] = data["person_id"].astype("int64")
    return data[["time", "person_id", "x", "y"]].copy()


def load_points(points_path: Path) -> np.ndarray:
    raw_points = pd.read_csv(points_path, header=None)
    points = raw_points.iloc[:, :2].apply(pd.to_numeric, errors="coerce").dropna()
    if points.empty:
        raise ValueError(f"No valid points found in {points_path}. Expected two numeric columns: x,y")
    return points.to_numpy(dtype=float)


def build_templates(data: pd.DataFrame, min_points: int) -> list[TrajectoryTemplate]:
    templates: list[TrajectoryTemplate] = []

    for _, person_data in data.groupby("person_id"):
        ordered = person_data.sort_values("time")
        if len(ordered) < min_points:
            continue

        times = ordered["time"].to_numpy(dtype=float)
        positions = ordered[["x", "y"]].to_numpy(dtype=float)
        start = positions[0]
        end = positions[-1]

        if np.linalg.norm(end - start) < 1e-9:
            continue

        templates.append(TrajectoryTemplate(times=times, positions=positions, start=start, end=end))

    return templates


def _rotation_matrix(theta: float) -> np.ndarray:
    return np.array([[np.cos(theta), -np.sin(theta)], [np.sin(theta), np.cos(theta)]], dtype=float)


def transform_template_to_endpoints(
    template: TrajectoryTemplate,
    spawn_point: np.ndarray,
    despawn_point: np.ndarray,
    person_id: int,
    start_time: float,
) -> pd.DataFrame:
    source_vector = template.end - template.start
    target_vector = despawn_point - spawn_point

    source_norm = np.linalg.norm(source_vector)
    target_norm = np.linalg.norm(target_vector)
    if source_norm < 1e-9 or target_norm < 1e-9:
        raise ValueError("Cannot transform trajectory with degenerate start/end vector.")

    scale = target_norm / source_norm
    source_angle = np.arctan2(source_vector[1], source_vector[0])
    target_angle = np.arctan2(target_vector[1], target_vector[0])
    rotation = _rotation_matrix(target_angle - source_angle)

    centered_positions = template.positions - template.start
    transformed_positions = spawn_point + scale * (centered_positions @ rotation.T)
    transformed_times = start_time + (template.times - template.times[0])

    velocities = np.zeros(len(transformed_times), dtype=float)
    motion_angles = np.zeros(len(transformed_times), dtype=float)

    if len(transformed_times) > 1:
        delta_positions = np.diff(transformed_positions, axis=0)
        delta_times = np.diff(transformed_times)
        valid_delta_times = np.where(delta_times <= 0, 1e-6, delta_times)
        step_velocity = np.linalg.norm(delta_positions / valid_delta_times[:, None], axis=1)
        step_angle = np.arctan2(delta_positions[:, 1], delta_positions[:, 0])

        velocities[1:] = step_velocity
        velocities[0] = step_velocity[0]
        motion_angles[1:] = step_angle
        motion_angles[0] = step_angle[0]

    return pd.DataFrame(
        {
            "time": transformed_times,
            "person_id": np.full(len(transformed_times), person_id, dtype=int),
            "x": transformed_positions[:, 0],
            "y": transformed_positions[:, 1],
            "velocity": velocities,
            "motion_angle": motion_angles,
        }
    )


def matching_templates(
    templates: list[TrajectoryTemplate],
    spawn_point: np.ndarray,
    despawn_point: np.ndarray,
    endpoint_radius: float,
) -> list[TrajectoryTemplate]:
    if endpoint_radius <= 0:
        return templates

    compatible_templates: list[TrajectoryTemplate] = []
    for template in templates:
        if np.linalg.norm(template.start - spawn_point) <= endpoint_radius and np.linalg.norm(template.end - despawn_point) <= endpoint_radius:
            compatible_templates.append(template)

    return compatible_templates if compatible_templates else templates


def build_pairs(spawn_points: np.ndarray, despawn_points: np.ndarray, pair_by_index: bool) -> list[tuple[np.ndarray, np.ndarray]]:
    if pair_by_index:
        pair_count = min(len(spawn_points), len(despawn_points))
        return [(spawn_points[index], despawn_points[index]) for index in range(pair_count)]

    return [(spawn_point, despawn_point) for spawn_point in spawn_points for despawn_point in despawn_points]


def generate_trajectories(
    dataset_path: Path,
    spawn_points_path: Path | None,
    despawn_points_path: Path | None,
    output_path: Path,
    num_trajectories: int,
    min_points: int,
    endpoint_radius: float,
    pair_by_index: bool,
    seed: int | None,
    time_offset_step: float,
    waypoints_path: Path | None = None,
) -> pd.DataFrame:
    if num_trajectories <= 0:
        raise ValueError("num_trajectories must be greater than zero")
    if min_points < 2:
        raise ValueError("min_points must be at least 2")

    trajectory_data = load_trajectory_data(dataset_path)
    templates = build_templates(trajectory_data, min_points=min_points)
    if not templates:
        raise ValueError("No valid trajectory templates available from input dataset.")

    rng = np.random.default_rng(seed)
    generated_tracks: list[pd.DataFrame] = []

    if waypoints_path is not None:
        waypoint_sequence = load_points(waypoints_path)
        if len(waypoint_sequence) < 2:
            raise ValueError("Waypoints CSV must contain at least two points.")

        for trajectory_index in range(num_trajectories):
            current_time = trajectory_index * time_offset_step
            segment_frames: list[pd.DataFrame] = []

            for waypoint_index in range(len(waypoint_sequence) - 1):
                spawn_point = waypoint_sequence[waypoint_index]
                despawn_point = waypoint_sequence[waypoint_index + 1]

                if np.linalg.norm(despawn_point - spawn_point) <= 1e-9:
                    continue

                candidate_templates = matching_templates(
                    templates,
                    spawn_point=spawn_point,
                    despawn_point=despawn_point,
                    endpoint_radius=endpoint_radius,
                )
                template_index = int(rng.integers(0, len(candidate_templates)))
                selected_template = candidate_templates[template_index]

                segment = transform_template_to_endpoints(
                    selected_template,
                    spawn_point=spawn_point,
                    despawn_point=despawn_point,
                    person_id=trajectory_index,
                    start_time=current_time,
                )

                if segment_frames:
                    segment = segment.iloc[1:].copy()
                    if segment.empty:
                        continue

                segment_frames.append(segment)
                current_time = float(segment["time"].iloc[-1])

            if not segment_frames:
                raise ValueError(
                    "No valid waypoint segments generated. Ensure consecutive waypoints are not identical."
                )

            generated_tracks.append(pd.concat(segment_frames, ignore_index=True))
    else:
        if spawn_points_path is None or despawn_points_path is None:
            raise ValueError("spawn_points_path and despawn_points_path are required when --waypoints is not used")

        spawn_points = load_points(spawn_points_path)
        despawn_points = load_points(despawn_points_path)
        pairs = build_pairs(spawn_points, despawn_points, pair_by_index=pair_by_index)
        pairs = [pair for pair in pairs if np.linalg.norm(pair[1] - pair[0]) > 1e-9]
        if not pairs:
            raise ValueError("No valid spawn/despawn pairs found. Ensure spawn and despawn points are not identical.")

        for trajectory_index in range(num_trajectories):
            pair_index = int(rng.integers(0, len(pairs)))
            spawn_point, despawn_point = pairs[pair_index]

            candidate_templates = matching_templates(
                templates,
                spawn_point=spawn_point,
                despawn_point=despawn_point,
                endpoint_radius=endpoint_radius,
            )
            template_index = int(rng.integers(0, len(candidate_templates)))
            selected_template = candidate_templates[template_index]

            transformed_track = transform_template_to_endpoints(
                selected_template,
                spawn_point=spawn_point,
                despawn_point=despawn_point,
                person_id=trajectory_index,
                start_time=trajectory_index * time_offset_step,
            )
            generated_tracks.append(transformed_track)

    generated = pd.concat(generated_tracks, ignore_index=True)
    generated = generated.sort_values(["person_id", "time"]).reset_index(drop=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    generated.to_csv(output_path, index=False, header=False)
    return generated


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generate synthetic trajectories from an existing CSV so each trajectory starts at a "
            "spawn point and ends at a despawn point."
        )
    )
    parser.add_argument("dataset", type=Path, help="Input CSV with existing tracks (6 or 8 columns).")
    parser.add_argument("spawn_points", type=Path, nargs="?", help="CSV with spawn points (x,y).")
    parser.add_argument("despawn_points", type=Path, nargs="?", help="CSV with despawn points (x,y).")
    parser.add_argument(
        "--waypoints",
        type=Path,
        default=None,
        help="CSV with an ordered waypoint sequence (x,y). Consecutive waypoint pairs are stitched as trajectory segments.",
    )
    parser.add_argument("--output", type=Path, required=True, help="Output CSV path for generated trajectories.")
    parser.add_argument("--num-trajectories", type=int, required=True, help="Number of trajectories to generate.")
    parser.add_argument(
        "--min-points",
        type=int,
        default=8,
        help="Minimum number of points required for an input trajectory template.",
    )
    parser.add_argument(
        "--endpoint-radius",
        type=float,
        default=0.0,
        help=(
            "If > 0, prefer templates whose original start/end are within this radius from selected "
            "spawn/despawn points; fallback to all templates if none match."
        ),
    )
    parser.add_argument(
        "--pair-by-index",
        action="store_true",
        help="Use spawn[i] with despawn[i] (up to the shortest list) instead of all Cartesian combinations.",
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible generation.")
    parser.add_argument(
        "--time-offset-step",
        type=float,
        default=0.0,
        help="Start time offset between generated trajectories (for trajectory i: i * step).",
    )
    return parser


def main() -> int:
    parser = build_argument_parser()
    args = parser.parse_args()

    using_waypoints = args.waypoints is not None
    using_spawn_despawn = args.spawn_points is not None or args.despawn_points is not None

    if using_waypoints and using_spawn_despawn:
        parser.error("Use either spawn/despawn positional files or --waypoints, not both.")
    if not using_waypoints and (args.spawn_points is None or args.despawn_points is None):
        parser.error("Provide both spawn_points and despawn_points, or use --waypoints.")

    generated = generate_trajectories(
        dataset_path=args.dataset,
        spawn_points_path=args.spawn_points,
        despawn_points_path=args.despawn_points,
        output_path=args.output,
        num_trajectories=args.num_trajectories,
        min_points=args.min_points,
        endpoint_radius=args.endpoint_radius,
        pair_by_index=args.pair_by_index,
        seed=args.seed,
        time_offset_step=args.time_offset_step,
        waypoints_path=args.waypoints,
    )

    print(
        f"Generated {generated['person_id'].nunique()} trajectories with {len(generated)} points in {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())