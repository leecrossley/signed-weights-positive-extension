from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent
GROUPS = [
    ["PaperFourier", "Orthogonality", "FourierWindow", "RademacherBound"],
    ["PrimeWindow", "PrimeEndpoint", "PrincipalMass", "WindowObstruction", "CharacterLowerBound"],
    ["Blocks"],
]
ACCEPTED = {"propext", "Classical.choice", "Quot.sound"}
EXTRA_AUDITS = {
    "RademacherBound": ["RademacherBound." + name for name in
        ("mass_bound_of_signs","exists_signs_with_correlation_bound","exists_signs_mass_lower_bound")],
    "PaperFourier": ["PaperFourier." + name for name in
        ("ramp_endpoint","weighted_ramp_endpoint","centered_endpoint","centered_ramp_endpoint")],
}

def main():
    parser = argparse.ArgumentParser(description="Rebuild each paper module, then audit its public theorems.")
    parser.add_argument("--mathlib-project", type=Path, default=ROOT)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    lake = shutil.which("lake")
    lean = shutil.which("lean")
    if not lean or not lake:
        parser.error("Use Lean 4.13.0 and its matching lake executable on PATH.")
    import re
    resolved = args.mathlib_project.resolve()
    version = subprocess.check_output([lean, "--version"], encoding="utf-8").strip()
    if "version 4.13.0," not in version:
        parser.error("Expected the toolchain pinned in lean-toolchain.")
    lookup = subprocess.check_output(
        [lake, "env", sys.executable, "-c", "import os; print(os.environ['LEAN_PATH'])"],
        cwd=resolved, encoding="utf-8",
    ).strip()
    roots = [str((resolved / path).resolve()) for path in lookup.split(os.pathsep) if path]
    module = Path("Mathlib/NumberTheory/DirichletCharacter/Basic.olean")
    library = next((Path(root) for root in roots if (Path(root) / module).is_file()), None)
    if library is None:
        parser.error(f"Could not find {module} in the selected project's Lean search path.")
    revision = subprocess.run(
        ["git", "-C", str(library), "rev-parse", "HEAD"], capture_output=True, text=True,
    )
    if revision.returncode:
        parser.error(f"Could not determine the Mathlib Git revision for {library}.")
    actual = revision.stdout.strip()
    packages = json.loads((ROOT / "lake-manifest.json").read_text(encoding="utf-8"))["packages"]
    expected = next(package["rev"] for package in packages if package["name"] == "mathlib")
    if actual != expected:
        parser.error(f"The selected Mathlib is at {actual}. This paper uses {expected}.")
    report = {"lean": version, "mathlib": actual, "modules": {}}
    with TemporaryDirectory(prefix="paper-mathlib-") as temp:
        env = dict(os.environ, LEAN_PATH=os.pathsep.join([temp, *roots]))
        def verify_one(name):
            file = ROOT / (name + ".lean")
            data = file.read_bytes()
            proc = subprocess.run([lean,"-o",str(Path(temp)/(name+".olean")),file.name],
                cwd=ROOT,env=env,text=True,encoding="utf-8",capture_output=True)
            output = proc.stdout + proc.stderr
            if proc.returncode or "sorryAx" in output:
                raise RuntimeError(output)
            extra = EXTRA_AUDITS.get(name, [])
            if extra:
                audit = Path(temp)/(name + "Audit.lean")
                audit.write_text("import " + name + "\n" + "".join("#print axioms "+v+"\n" for v in extra),encoding="utf-8")
                run = subprocess.run([lean,str(audit)], cwd=ROOT,env=env,text=True,encoding="utf-8",capture_output=True)
                output += run.stdout + run.stderr
                if run.returncode:
                    raise RuntimeError(output)
            expected = len(extra) + len(re.findall(rb"(?m)^#print axioms ",data))
            audit_sets = re.findall(r"depends on axioms:\s*\[([^\]]*)\]",output)
            checked = len(audit_sets) + output.count("does not depend on any axioms")
            used = {a.strip() for row in audit_sets for a in row.split(",") if a.strip()}
            if not expected or checked != expected or used - ACCEPTED or "sorryAx" in output or "warning:" in output:
                raise RuntimeError(f"Unexpected axiom audit in {name}:\n{output}")
            record = {"sha256":hashlib.sha256(data).hexdigest(),"checked":checked,
                "axioms":sorted(used),"output":output.strip()}
            print(f"{name}: passed ({checked} audits)",flush=True)
            return name, record

        with ThreadPoolExecutor(max_workers=3) as pool:
            for group in GROUPS:
                report["modules"].update(pool.map(verify_one, group))
    report["status"] = "passed"
    if args.out:
        args.out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

if __name__ == "__main__":
    main()
