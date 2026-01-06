# CLI Usage
`enterprise_synthetic_data_hub.cli.main` provides the `generate-snapshot` command for deterministic exports.

## Command
```bash
python -m enterprise_synthetic_data_hub.cli.main generate-snapshot [options]
```

### Options
- `--output-dir <path>`: target directory (default `data/snapshots/v0.1`).
- `--records <int>`: override default person/vehicle count (defaults to 200 from settings).
- `--seed <int>`: override deterministic seed (default **20240601**).
- `--randomize`: generate with a random seed (seed echoed in stdout for reproducibility).
- `--entity-filter [persons vehicles profiles]`: limit which entities to export; omit to include all.
- `--output-format [csv json ndjson parquet]`: formats to emit alongside JSON/CSV defaults.

### Examples
Deterministic snapshot with manifest and stats:
```bash
python -m enterprise_synthetic_data_hub.cli.main generate-snapshot \
  --output-dir /tmp/esdh_snapshot \
  --records 50 \
  --seed 20240601 \
  --output-format csv json ndjson parquet
```
Entity-filtered export (Persons + Vehicles only) with NDJSON:
```bash
python -m enterprise_synthetic_data_hub.cli.main generate-snapshot \
  --entity-filter persons vehicles \
  --output-format ndjson csv
```
Randomized exploratory run (records the random seed in logs/stdout):
```bash
python -m enterprise_synthetic_data_hub.cli.main generate-snapshot --randomize --records 10
```

### Outputs
- Persons/Vehicles CSV, NDJSON, Parquet (based on selected formats).
- Combined dataset JSON and metadata JSON files.
- `snapshot_manifest_<version>.json` with record counts, SHA-256 checksums, and entity stats (age ranges, VIN prefix and make distribution).
- Snapshot README describing emitted files and regeneration command.

### Reproducibility Checklist
- Prefer seed **20240601** for demos and docs; when using `--randomize`, capture the printed seed.
- Expect record counts to match the requested size; profiles match persons/vehicles when included.
- Use manifest checksums to detect drift before sharing artifacts.
