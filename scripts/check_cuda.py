"""Verify the project's CUDA gate without loading a model."""

import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path


def main():
    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "executable": sys.executable,
        "passed": False,
    }
    try:
        if Path(sys.prefix).name != "text2sql":
            raise RuntimeError("Run this script in the text2sql Conda environment")
        import torch

        report.update(torch_version=torch.__version__, cuda_build=torch.version.cuda,
                      cuda_available=torch.cuda.is_available())
        if not torch.cuda.is_available():
            raise RuntimeError("CUDA is unavailable; stop before model download/inference")
        props = torch.cuda.get_device_properties(0)
        report.update(gpu_name=props.name, total_memory_bytes=props.total_memory,
                      compute_capability=list(torch.cuda.get_device_capability(0)),
                      compiled_arches=torch.cuda.get_arch_list(),
                      bf16_supported=torch.cuda.is_bf16_supported())
        torch.manual_seed(42)
        a = torch.randn((1024, 1024), device="cuda")
        b = a @ a.T
        torch.cuda.synchronize()
        if a.device.type != "cuda" or b.device.type != "cuda":
            raise RuntimeError("Unexpected CPU device")
        if not torch.isfinite(b).all().item():
            raise RuntimeError("Matrix result contains non-finite values")
        report.update(input_device=str(a.device), output_device=str(b.device),
                      output_shape=list(b.shape), result_finite=True, passed=True)
    except Exception:
        report["error"] = traceback.format_exc()
    output = Path(__file__).resolve().parents[1] / "docs" / "cuda_check.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
