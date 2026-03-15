STRINGS: dict[str, str] = {
    # ── Nav / Chrome ──────────────────────────────────────────────────────
    "nav.home":  "Início",
    "nav.game":  "Jogar",
    "nav.about": "Sobre",
    "nav.title": "Onde Está o Waldo?",
    "footer.text": "Onde Está o Waldo? — Desafio de IA",

    # ── Home — Hero ───────────────────────────────────────────────────────
    "home.hero.title":    "Onde Está o Waldo?",
    "home.hero.accent":   " IA",
    "home.hero.subtitle": (
        "Gere uma cena, clique no Waldo e veja se você consegue "
        "achar antes do modelo YOLOv8 treinado do zero."
    ),

    # ── Home — Project card ───────────────────────────────────────────────
    "home.project.title":        "O Projeto",
    "home.project.body1_pre":    "Um pipeline completo de ",
    "home.project.body1_strong": "visão computacional",
    "home.project.body1_post": (
        " construído do zero: geração de dataset sintético, "
        "treinamento de YOLOv8 e inferência em tempo real via API."
    ),
    "home.project.body2": (
        "As cenas são geradas proceduralmente com sprites pixel-art. "
        "O modelo aprende a localizar o Waldo entre dezenas de "
        "personagens similares."
    ),

    # ── Home — Stats card ─────────────────────────────────────────────────
    "home.stats.title":        "Dataset",
    "home.stats.scenes":       "cenas de treino",
    "home.stats.difficulties": "dificuldades",
    "home.stats.sprites":      "sprites únicos",

    # ── Home — How it works ───────────────────────────────────────────────
    "home.how.label":       "COMO FUNCIONA",
    "home.how.step1.title": "1. Geração da cena",
    "home.how.step1.desc": (
        "Uma cena 640×640 é gerada proceduralmente com sprites pixel-art "
        "e um fundo aleatório. O Waldo é inserido em posição aleatória."
    ),
    "home.how.step2.title": "2. Seu palpite",
    "home.how.step2.desc": (
        "Clique na imagem onde você acha que o Waldo está. "
        "Você tem uma tentativa por cena."
    ),
    "home.how.step3.title": "3. IA detecta",
    "home.how.step3.desc": (
        "O modelo YOLOv8 analisa a mesma cena e tenta localizar o Waldo. "
        "Quem achou primeiro?"
    ),

    # ── Home — CTA ────────────────────────────────────────────────────────
    "home.cta.button":    "Jogar agora",
    "home.cta.prefix":    "ou veja os ",
    "home.cta.link_text": "detalhes técnicos",
    "home.cta.suffix":    " na página Sobre",

    # ── Game ──────────────────────────────────────────────────────────────
    "game.difficulty.label":  "Dificuldade",
    "game.difficulty.easy":   "Fácil (20 personagens)",
    "game.difficulty.medium": "Médio (80 personagens)",
    "game.difficulty.hard":   "Difícil (150 personagens)",
    "game.btn.generate":      "Gerar cena",
    "game.status.label":      "Status",
    "game.status.default":    "Gere uma cena para começar a jogar!",
    "game.btn.submit":        "Enviar palpite",
    "game.legend.label":      "Legenda",
    "game.legend.click":      "Seu clique",
    "game.legend.waldo":      "Aqui estava o Waldo",
    "game.legend.yolo":       "Detecção YOLO",
    "game.placeholder.title": "Nenhuma cena carregada",
    "game.placeholder.body": (
        "Selecione a dificuldade e clique em Gerar cena para começar."
    ),

    # ── Game — dynamic status messages ────────────────────────────────────
    "game.status.idle":    "Gere uma cena para começar a jogar!",
    "game.status.waiting": (
        "[{diff}] Clique na imagem onde você acha que o Waldo está escondido!"
    ),
    "game.status.guessed": (
        "[{diff}] Palpite definido em ({x}, {y}). "
        "Clique em Enviar palpite quando estiver pronto!"
    ),
    "game.status.done": (
        "[{diff}] Rodada encerrada! Gere uma nova cena para jogar de novo."
    ),
    "game.diff.easy":   "Fácil",
    "game.diff.medium": "Médio",
    "game.diff.hard":   "Difícil",

    # ── Results panel ─────────────────────────────────────────────────────
    "result.col.you":       "Você",
    "result.col.yolo":      "IA (YOLO)",
    "result.col.result":    "Resultado",
    "result.you.found":     "Encontrou o Waldo!",
    "result.you.missed":    "Errou o Waldo",
    "result.yolo.found":    "Encontrou! ({conf} conf.)",
    "result.yolo.found_nc": "Encontrou o Waldo!",
    "result.yolo.missed":   "Não encontrou o Waldo",
    "result.verdict.both":  "Você e a IA encontraram o Waldo!",
    "result.verdict.user":  "Você venceu a IA!",
    "result.verdict.yolo":  "A IA venceu esta rodada!",
    "result.verdict.none":  "Ninguém encontrou o Waldo desta vez.",

    # ── About ─────────────────────────────────────────────────────────────
    "about.title":    "Sobre o projeto",
    "about.subtitle": "Detalhes técnicos, arquitetura e pipeline de ML",

    "about.overview.label":        "Visão geral",
    "about.overview.body1_pre":    "O ",
    "about.overview.body1_strong": "Onde Está o Waldo? Desafio de IA",
    "about.overview.body1_suf": (
        " é um projeto end-to-end de visão computacional. "
        "Todo o pipeline — da geração de dados ao deploy — "
        "foi construído do zero."
    ),
    "about.overview.body2": (
        "Sprites pixel-art são gerados proceduralmente e compostos em "
        "cenas 640×640. Um modelo YOLOv8n é treinado nesse dataset "
        "sintético para detectar o Waldo em tempo real."
    ),

    "about.stack.label":        "Stack técnico",
    "about.tech.yolo.desc":     "detecção de objetos (Ultralytics)",
    "about.tech.fastapi.desc":  "API REST para cenas e inferência",
    "about.tech.dash.desc":     "interface interativa",
    "about.tech.pillow.desc":   "geração procedural de sprites",
    "about.tech.python.desc":   "linguagem principal",
    "about.tech.cloud.desc":    "deploy e armazenamento de artefatos",

    "about.pipeline.label":       "Pipeline de ML",
    "about.pipeline.step1.title": "Gerar sprites",
    "about.pipeline.step1.desc": (
        "Sprites pixel-art de personagens e Waldo gerados "
        "proceduralmente com temas (tourist / explorer / casual)."
    ),
    "about.pipeline.step2.title": "Gerar dataset",
    "about.pipeline.step2.desc": (
        "Cenas 640×640 compostas com plano de fundo + personagens + Waldo. "
        "Labels em formato YOLO (xywh normalizado)."
    ),
    "about.pipeline.step3.title": "Treinar modelo",
    "about.pipeline.step3.desc": (
        "Ajuste fino do YOLOv8n no conjunto de dados sintético. "
        "Pesos salvos em model/models/waldo_yolov8n/."
    ),
    "about.pipeline.step4.title": "Avaliar",
    "about.pipeline.step4.desc": (
        "mAP50 e métricas por divisão calculadas no conjunto de validação."
    ),
    "about.pipeline.footer": (
        "Pipeline completo: executado via pipelines de ML do projeto."
    ),

    "about.arch.label": "Arquitetura",
    "about.arch.box1":  "Interface\n(Dash)",
    "about.arch.box3":  "model/models\nYOLOv8n\ninferência",
    "about.arch.note": (
        "A interface nunca importa ML diretamente — toda inferência e "
        "geração de cenas passa pela API (arquitetura Opção B)."
    ),
    "about.back": "← Voltar para o jogo",
}
