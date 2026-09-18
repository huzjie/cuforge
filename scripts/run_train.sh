#!/usr/bin/env bash
# RLVR 训练
set -e
python -m cuforge.cli.main train --episodes 64
