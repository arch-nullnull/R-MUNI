#!/usr/bin/env python3
# CSV03-resolve_run_scope.py
#
# Purpose (Flow-Stage):
# - Resolve the deterministic run scope for the current CSV flow execution
# - Decide WHICH models are in scope based on declarative mapping rules
# - Persist the run scope as the single binding contract for all following stages
#
# Output:
# - <rootfolder>/03-stages/run-scope.txt
# - <rootfolder>/03-stages/99-logs/CSV03-resolve_run_scope.log
#
# Rules:
# - Scope-defining stage (decision point)
# - No directory creation
# - No heuristics, no defaults
# - Abort if no scope can be resolved

import os
import sys
from datetime import datetime


DEBUG = False


def now_ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def die(message: str, log_path: str | None = None) -> None:
    line = f"[CSV03] {now_ts()} | ERROR | {message}"
    print(line, file=sys.stderr)
    if log_path:
        try:
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass
    sys.exit(1)


def log(message: str, log_path: str | None = None) -> None:
    line = f"[CSV03] {now_ts()} | {message}"
    if DEBUG:
        print(line)
    if log_path:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def read_root_resolved(script_dir: str) -> str:
    path = os.path.abspath(
        os.path.join(script_dir, "..", "..", "03-stages", "99-logs", "CSV00-root.resolved.txt")
    )
    if not os.path.isfile(path):
        die(f"missing CSV00 root artifact: {path}", None)

    try:
        with open(path, "r", encoding="utf-8") as f:
            root = f.readline().strip()
    except Exception as e:
        die(f"cannot read CSV00 root artifact: {e}", None)

    if root == "" or not os.path.isdir(root):
        die(f"invalid root path resolved by CSV00: {root}", None)

    return root


def read_model_scope(stages_dir: str, log_path: str) -> list[str]:
    path = os.path.join(stages_dir, "model-scope.txt")
    if not os.path.isfile(path):
        die(f"missing model-scope artifact: {path}", log_path)

    models = []
    current_section = None

    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped.endswith(":"):
                    current_section = stripped
                    continue
                if stripped.startswith("- "):
                    model = stripped[2:].strip()
                    if model:
                        models.append(model)
    except Exception as e:
        die(f"cannot read model-scope artifact: {e}", log_path)

    return sorted(set(models))


def read_csv_mapping(mapping_path: str, log_path: str) -> list[str]:
    if not os.path.isfile(mapping_path):
        die(f"missing csvmapping.txt: {mapping_path}", log_path)

    rules = []

    try:
        with open(mapping_path, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if stripped == "" or stripped.startswith("#"):
                    continue
                rules.append(stripped)
    except Exception as e:
        die(f"cannot read csvmapping.txt: {e}", log_path)

    if not rules:
        die("csvmapping.txt contains no active rules", log_path)

    return rules


def extract_model_patterns(mapping_rules: list[str]) -> list[str]:
    patterns = []
    for rule in mapping_rules:
        if rule.startswith("archi[") and "model=" in rule:
            try:
                part = rule.split("model=", 1)[1]
                pattern = part.split("]", 1)[0]
                patterns.append(pattern)
            except Exception:
                continue
    return patterns


def model_matches_pattern(model_name: str, pattern: str) -> bool:
    if pattern == "*":
        return True
    token = pattern.replace("*", "")
    return token.lower() in model_name.lower()


def main() -> None:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_path = read_root_resolved(script_dir)

    stages_dir = os.path.join(root_path, "03-stages")
    logs_dir = os.path.join(stages_dir, "99-logs")

    if not os.path.isdir(stages_dir):
        die(f"expected stages directory not found: {stages_dir}", None)

    if not os.path.isdir(logs_dir):
        die(f"expected logs directory not found: {logs_dir}", None)

    log_path = os.path.join(logs_dir, "CSV03-resolve_run_scope.log")
    log(f"Resolved root path: {root_path}", log_path)

    models = read_model_scope(stages_dir, log_path)
    log(f"Models available from model-scope: {len(models)}", log_path)

    mapping_path = os.path.join(
        root_path, "02-artifacts", "02-csv", "01-mapping", "csvmapping.txt"
    )
    rules = read_csv_mapping(mapping_path, log_path)
    log(f"Active mapping rules: {len(rules)}", log_path)

    patterns = extract_model_patterns(rules)
    log(f"Extracted model patterns: {patterns}", log_path)

    scope_models = []

    for model in models:
        for pattern in patterns:
            if model_matches_pattern(model, pattern):
                scope_models.append(model)
                log(f"Model matched: {model} (pattern={pattern})", log_path)
                break

    scope_models = sorted(set(scope_models))

    if not scope_models:
        die("no models matched mapping rules; run scope is empty", log_path)

    out_path = os.path.join(stages_dir, "run-scope.txt")

    try:
        with open(out_path, "w", encoding="utf-8") as f:
            for model in scope_models:
                f.write("SOURCE=archi\n")
                f.write(f"MODEL={model}\n\n")
    except Exception as e:
        die(f"cannot write run-scope artifact: {e}", log_path)

    log(f"Run scope written with {len(scope_models)} model(s)", log_path)
    print(f"[CSV03] OK | run scope resolved -> {out_path}")


if __name__ == "__main__":
    main()
