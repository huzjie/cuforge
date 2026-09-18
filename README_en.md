# cuforge — Verifiable Task Synthesis for Online RL of Computer-Use Agents

An engineering-grade implementation of **ScaleCUA** (Tsinghua × Z.AI): scalable
verifiable task synthesis + online reinforcement learning for GUI agents
(9B model, open-source SOTA on OSWorld).

**Not a demo — a complete, runnable platform.** Fill in `config.yaml` and run.

## Highlights

- **VeriGen** — synthesize tasks *with* verifiable acceptance criteria (6 task
  templates + 7 deterministic verifiers).
- **Desktop Env** — isolated, deterministic GUI environment (filesystem,
  UI tree, processes, terminal, settings, browser).
- **Agent Runtime** — see → plan → click/type → observe loop, with vision
  context windowing (recent / summary / full).
- **RLVR** — sample → score → group-relative comparison (GRPO) → policy update,
  with frontier sampling to train efficiently.

## Quickstart

```bash
pip install -e .
python -m cuforge.cli.main doctor    # end-to-end smoke: synthesize -> run -> score
python -m cuforge.cli.main train --episodes 64
python -m cuforge.cli.main eval
python -m cuforge.cli.main serve --port 8000
```

## Benchmarks

| Benchmark | Note | ScaleCUA ref (Qwen3.5-9B) |
|---|---|---|
| mini (builtin) | end-to-end success rate | 100% (scripted baseline) |
| OSWorld | real-OS GUI (Docker) | 68.7% |
| ScienceBoard | scientific desktop tasks | 54.0% |

MIT License.
