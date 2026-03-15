STRINGS: dict[str, str] = {
    # ── Nav / Chrome ──────────────────────────────────────────────────────
    "nav.home":  "Home",
    "nav.game":  "Play",
    "nav.about": "About",
    "nav.title": "Where is Waldo?",
    "footer.text": "Where is Waldo? — AI Challenge",

    # ── Home — Hero ───────────────────────────────────────────────────────
    "home.hero.title":    "Where is Waldo?",
    "home.hero.accent":   " AI",
    "home.hero.subtitle": (
        "Generate a scene, click on Waldo and see if you can find him "
        "before the YOLOv8 model trained from scratch."
    ),

    # ── Home — Project card ───────────────────────────────────────────────
    "home.project.title":        "The Project",
    "home.project.body1_pre":    "A complete ",
    "home.project.body1_strong": "computer vision",
    "home.project.body1_post": (
        " pipeline built from scratch: synthetic dataset generation, "
        "YOLOv8 training and real-time inference via API."
    ),
    "home.project.body2": (
        "Scenes are generated procedurally with pixel-art sprites. "
        "The model learns to locate Waldo among dozens of similar characters."
    ),

    # ── Home — Stats card ─────────────────────────────────────────────────
    "home.stats.title":        "Dataset",
    "home.stats.scenes":       "training scenes",
    "home.stats.difficulties": "difficulties",
    "home.stats.sprites":      "unique sprites",

    # ── Home — How it works ───────────────────────────────────────────────
    "home.how.label":       "HOW IT WORKS",
    "home.how.step1.title": "1. Scene generation",
    "home.how.step1.desc": (
        "A 640×640 scene is generated procedurally with pixel-art sprites "
        "and a random background. Waldo is placed at a random position."
    ),
    "home.how.step2.title": "2. Your guess",
    "home.how.step2.desc": (
        "Click on the image where you think Waldo is. "
        "You have one attempt per scene."
    ),
    "home.how.step3.title": "3. AI detects",
    "home.how.step3.desc": (
        "The YOLOv8 model analyzes the same scene and tries to locate Waldo. "
        "Who found him first?"
    ),

    # ── Home — CTA ────────────────────────────────────────────────────────
    "home.cta.button":    "Play now",
    "home.cta.prefix":    "or see the ",
    "home.cta.link_text": "technical details",
    "home.cta.suffix":    " on the About page",

    # ── Game ──────────────────────────────────────────────────────────────
    "game.difficulty.label":  "Difficulty",
    "game.difficulty.easy":   "Easy (20 characters)",
    "game.difficulty.medium": "Medium (80 characters)",
    "game.difficulty.hard":   "Hard (150 characters)",
    "game.btn.generate":      "Generate Scene",
    "game.status.label":      "Status",
    "game.status.default":    "Generate a scene to start playing!",
    "game.btn.submit":        "Submit Guess",
    "game.legend.label":      "Legend",
    "game.legend.click":      "Your click",
    "game.legend.waldo":      "Where Waldo was",
    "game.legend.yolo":       "YOLO detection",
    "game.placeholder.title": "No scene loaded",
    "game.placeholder.body":  (
        "Select difficulty and click Generate Scene to begin."
    ),

    # ── Game — dynamic status messages ────────────────────────────────────
    "game.status.idle":    "Generate a scene to start playing!",
    "game.status.waiting": (
        "[{diff}] Click on the image where you think Waldo is hiding!"
    ),
    "game.status.guessed": (
        "[{diff}] Guess set at ({x}, {y}). Click Submit Guess when ready!"
    ),
    "game.status.done": (
        "[{diff}] Round over! Generate a new scene to play again."
    ),
    "game.diff.easy":   "Easy",
    "game.diff.medium": "Medium",
    "game.diff.hard":   "Hard",

    # ── Results panel ─────────────────────────────────────────────────────
    "result.col.you":       "You",
    "result.col.yolo":      "AI (YOLO)",
    "result.col.result":    "Result",
    "comp.result.placeholder": "Round Result",
    "result.you.found":     "Found Waldo!",
    "result.you.missed":    "Missed Waldo",
    "result.yolo.found":    "Found it! ({conf} conf.)",
    "result.yolo.found_nc": "Found Waldo!",
    "result.yolo.missed":   "Didn't find Waldo",
    "result.verdict.both":  "You and the AI both found Waldo!",
    "result.verdict.user":  "You beat the AI!",
    "result.verdict.yolo":  "AI wins this round!",
    "result.verdict.none":  "Nobody found Waldo this time.",

    # ── About ─────────────────────────────────────────────────────────────
    "about.title":    "About the project",
    "about.subtitle": "Technical details, architecture and ML pipeline",

    "about.overview.label":        "Overview",
    "about.overview.body1_pre":    "",
    "about.overview.body1_strong": "Where is Waldo? AI Challenge",
    "about.overview.body1_suf": (
        " is an end-to-end computer vision project. "
        "The entire pipeline — from data generation to deployment — "
        "was built from scratch."
    ),
    "about.overview.body2": (
        "Pixel-art sprites are generated procedurally and composited into "
        "640×640 scenes. A YOLOv8n model is trained on this synthetic "
        "dataset to detect Waldo in real time."
    ),

    "about.stack.label":        "Tech stack",
    "about.tech.yolo.desc":     "object detection (Ultralytics)",
    "about.tech.fastapi.desc":  "REST API for scenes and inference",
    "about.tech.dash.desc":     "interactive interface",
    "about.tech.pillow.desc":   "procedural sprite generation",
    "about.tech.python.desc":   "main language",
    "about.tech.cloud.desc":    "deployment and artifact storage",

    "about.pipeline.label":       "ML Pipeline",
    "about.pipeline.step1.title": "Generate sprites",
    "about.pipeline.step1.desc": (
        "Pixel-art character and Waldo sprites generated procedurally "
        "with themes (tourist / explorer / casual)."
    ),
    "about.pipeline.step2.title": "Generate dataset",
    "about.pipeline.step2.desc": (
        "640×640 scenes composed with background + characters + Waldo. "
        "Labels in YOLO format (normalized xywh)."
    ),
    "about.pipeline.step3.title": "Train model",
    "about.pipeline.step3.desc": (
        "Fine-tuning of YOLOv8n on the synthetic dataset. "
        "Weights saved in model/models/waldo_yolov8n/."
    ),
    "about.pipeline.step4.title": "Evaluate",
    "about.pipeline.step4.desc": (
        "mAP50 and per-split metrics computed on the validation set."
    ),
    "about.pipeline.footer": (
        "Full pipeline: run via the project's ML pipelines."
    ),

    "about.arch.label": "Architecture",
    "about.arch.box1":  "Interface\n(Dash)",
    "about.arch.box3":  "model/models\nYOLOv8n\ninference",
    "about.arch.note": (
        "The interface never imports ML directly — all inference and "
        "scene generation goes through the API (Option B architecture)."
    ),
    "about.back": "← Back to game",

    # ── Competition ───────────────────────────────────────────────────────
    "comp.nav":             "Competition",
    "comp.title":           "Competition: You vs AI",
    "comp.subtitle":        "5 hard rounds — prove you're better than the model",
    "comp.rules.label":     "Rules",
    "comp.rules.rule1":     "5 rounds in Hard difficulty (160 characters per scene)",
    "comp.rules.rule2":     "One guess per round — click and submit",
    "comp.rules.rule3":     "The YOLO model tries to find Waldo in the same scene",
    "comp.rules.rule4":     "Most correct rounds at the end wins",
    "comp.btn.start":       "Start Competition",
    "comp.btn.submit":      "Submit Guess",
    "comp.btn.next":        "Next round",
    "comp.btn.finish":      "See final result",
    "comp.btn.play_again":  "Play again",
    "comp.score.you":       "You",
    "comp.score.ai":        "AI (YOLO)",
    "comp.round.header":    "Round {n} of {total}",
    "comp.round.waiting":   "Click on Waldo and submit your guess!",
    "comp.round.guessed":   "Guess at ({x}, {y}). Click Submit when ready!",
    "comp.round.done":      "Round over — see the result below.",
    "comp.placeholder.title": "Generating hard scene...",
    "comp.final.title":     "Final Result",
    "comp.final.you_win":   "You beat the AI!",
    "comp.final.ai_win":    "AI wins!",
    "comp.final.draw":      "Draw!",
    "comp.final.score":     "{user} × {ai}",
    "comp.timer.label":     "Time",
    "comp.timer.expired":   "Time expired!",
    "comp.final.round_label": "Rnd.",
    # ── Model page strings
    "nav.model":            "Model",
    "model.title":          "Model (YOLOv8n)",
    "model.description":    "The model used is YOLOv8n (nano), a real-time convolutional object detection network developed by Ultralytics. Training started from COCO pretrained weights and was fine-tuned exclusively to locate Waldo in synthetic scenes generated by the app — each scene contains exactly one Waldo instance placed randomly among dozens of distractor characters. The metrics below reflect the performance of the best checkpoint saved at the end of training.",
    "model.metrics.title":  "Training Metrics",
    "model.loss.title":     "Loss Curves",
    "model.epoch":          "Epoch",
    "model.metrics":        "Score",
    "model.loss":           "Loss",
    "model.series.map50":       "mAP50",
    "model.series.map5095":     "mAP50-95",
    "model.series.precision":   "Precision",
    "model.series.recall":      "Recall",
    "model.series.train_box":   "Train — Box",
    "model.series.train_cls":   "Train — Cls",
    "model.series.train_dfl":   "Train — DFL",
    "model.series.val_box":     "Val. — Box",
    "model.series.val_cls":     "Val. — Cls",
    "model.series.val_dfl":     "Val. — DFL",
    "model.error":              "Error loading training data: {e}",
    # ── Model guide card
    "model.guide.title":            "Metrics Guide",
    "model.guide.eval.heading":     "Evaluation Metrics",
    "model.guide.loss.heading":     "Loss Curves",
    "model.guide.map50.desc":       "Mean Average Precision at IoU ≥ 50%. A predicted box counts as correct if it overlaps the ground-truth box by at least half. The main benchmark for detection quality.",
    "model.guide.map5095.desc":     "mAP averaged over IoU thresholds from 0.50 to 0.95. A stricter criterion: the predicted box must be well-aligned, not just roughly in the right area.",
    "model.guide.precision.desc":   "Of all predicted bounding boxes, what fraction actually contains Waldo. High precision = few false positives.",
    "model.guide.recall.desc":      "Of all Waldo instances in the images, what fraction were detected. High recall = few missed detections.",
    "model.guide.box.desc":         "Error in predicting bounding box coordinates (center and dimensions). Decreases as the model learns to frame Waldo more accurately.",
    "model.guide.cls.desc":         "Classification loss — how confident the model is in predicting the correct class (Waldo vs. background). Tends to drop quickly in early epochs.",
    "model.guide.dfl.desc":         "Distribution Focal Loss — measures the precision of bounding box boundary prediction. Specific to YOLOv8's anchor-free architecture.",
    "model.guide.trainval.name":    "Train vs. Validation",
    "model.guide.trainval.desc":    "Solid lines = training set; dashed = validation. Both should decrease and stay close. A growing gap indicates overfitting.",
}

