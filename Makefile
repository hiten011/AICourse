.PHONY: 1 2 3 4 5 1s 2s 3s 4s 5s human benchmark help replay

# ── Visual runs (window opens) ────────────────────────────────────────────────

1:
	python my_agent.py --cave gold --show-window true

2:
	python my_agent.py --cave breeze_and_gold --show-window true

3:
	python my_agent.py --cave default --show-window true

4:
	python my_agent.py --cave siege --show-window true

5:
	python my_agent.py --cave large --show-window true

# ── Silent runs (no window, fast) ─────────────────────────────────────────────

1s:
	python my_agent.py --cave gold --show-window false

2s:
	python my_agent.py --cave breeze_and_gold --show-window false

3s:
	python my_agent.py --cave default --show-window false

4s:
	python my_agent.py --cave siege --show-window false

5s:
	python my_agent.py --cave large --show-window false

# ── Replay last saved layout ──────────────────────────────────────────────────
# 1. Set save_last_map: true in game_config.yaml
# 2. Run any cave — layout saved to maps/last.txt
# 3. make replay — reruns that exact cave

replay:
	python my_agent.py --cave last --show-window true

# ── Play it yourself ──────────────────────────────────────────────────────────
human:
	python human_agent.py --cave default --show-window true

# ── Benchmark your agent (100 runs) ──────────────────────────────────────────
# Edit assessor.py line 20: agent = MyAgent()

benchmark:
	python assessor.py

# ── Help ──────────────────────────────────────────────────────────────────────

help:
	@echo "Visual:  make 1-5          (each graded cave, window open)"
	@echo "Silent:  make 1s-5s        (no window, prints score)"
	@echo "Replay:  make replay       (rerun last saved map)"
	@echo "Human:   make human        (play yourself, default cave)"
	@echo "Assess:  make benchmark    (100-run benchmark)"
