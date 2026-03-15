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

    # ── Competition ───────────────────────────────────────────────────────
    "comp.nav":             "Competição",
    "comp.title":           "Competição: Você vs IA",
    "comp.subtitle":        "5 rodadas difíceis — prove que você é melhor que o modelo",
    "comp.rules.label":     "Regras",
    "comp.rules.rule1":     "5 rodadas em dificuldade Difícil (160 personagens por cena)",
    "comp.rules.rule2":     "Você tem uma tentativa por rodada — clique e envie",
    "comp.rules.rule3":     "O modelo YOLO tenta encontrar o Waldo na mesma cena",
    "comp.rules.rule4":     "Quem acertar mais rodadas ao final vence",
    "comp.btn.start":       "Iniciar Competicao",
    "comp.btn.submit":      "Enviar palpite",
    "comp.btn.next":        "Proxima rodada",
    "comp.btn.finish":      "Ver resultado final",
    "comp.btn.play_again":  "Jogar novamente",
    "comp.score.you":       "Você",
    "comp.score.ai":        "IA (YOLO)",
    "comp.round.header":    "Rodada {n} de {total}",
    "comp.round.waiting":   "Clique em Waldo e envie seu palpite!",
    "comp.round.guessed":   "Palpite em ({x}, {y}). Clique em Enviar quando estiver pronto!",
    "comp.round.done":      "Rodada encerrada — veja o resultado abaixo.",
    "comp.placeholder.title": "Gerando cena difícil...",
    "comp.final.title":     "Resultado Final",
    "comp.final.you_win":   "Voce venceu a IA!",
    "comp.final.ai_win":    "A IA venceu!",
    "comp.final.draw":      "Empate!",
    "comp.final.score":     "{user} × {ai}",
    "comp.timer.label":     "Tempo",
    "comp.timer.expired":   "Tempo esgotado!",
    "comp.final.round_label": "Rod.",

    # ── Model page strings
    "nav.model":            "Modelo",
    "model.title":          "Modelo (YOLOv8n)",
    "model.description":    "O modelo utilizado é o YOLOv8n (nano), uma rede neural convolucional de detecção de objetos em tempo real desenvolvida pela Ultralytics. O treinamento partiu dos pesos pré-treinados no COCO e foi ajustado (fine-tuning) exclusivamente para localizar o Waldo em cenas sintéticas geradas pelo próprio app — onde cada cena possui exatamente uma instância do Waldo posicionada aleatoriamente entre dezenas de personagens distratores. As métricas abaixo refletem o desempenho do melhor checkpoint salvo ao final do treinamento.",
    "model.metrics.title":  "Métricas de Treino",
    "model.loss.title":     "Curvas de Loss",
    "model.epoch":          "Época",
    "model.metrics":        "Score",
    "model.loss":           "Loss",
    "model.series.map50":       "mAP50",
    "model.series.map5095":     "mAP50-95",
    "model.series.precision":   "Precisão",
    "model.series.recall":      "Recall",
    "model.series.train_box":   "Treino — Box",
    "model.series.train_cls":   "Treino — Cls",
    "model.series.train_dfl":   "Treino — DFL",
    "model.series.val_box":     "Valid. — Box",
    "model.series.val_cls":     "Valid. — Cls",
    "model.series.val_dfl":     "Valid. — DFL",
    "model.error":              "Erro ao carregar os dados de treinamento: {e}",
    # ── Model guide card
    "model.guide.title":            "Guia das Métricas",
    "model.guide.eval.heading":     "Métricas de Avaliação",
    "model.guide.loss.heading":     "Curvas de Loss",
    "model.guide.map50.desc":       "Precisão média com limiar de sobreposição (IoU) ≥ 50%. Mede se o modelo localiza o Waldo no lugar certo — um bounding box conta como correto se cobrir pelo menos metade da área real.",
    "model.guide.map5095.desc":     "Média do mAP sobre limiares de IoU de 0,50 a 0,95. Critério mais rigoroso: exige que o bounding box predito seja bem preciso, não apenas próximo.",
    "model.guide.precision.desc":   "Dos bounding boxes preditos, qual fração de fato contém o Waldo. Alta precisão significa poucos falsos positivos.",
    "model.guide.recall.desc":      "Dos Waldos presentes nas imagens, qual fração foi detectada. Alto recall significa poucas detecções perdidas.",
    "model.guide.box.desc":         "Erro na predição das coordenadas do bounding box (posição central e dimensões). Cai à medida que o modelo aprende a enquadrar o Waldo com mais precisão.",
    "model.guide.cls.desc":         "Erro de classificação — quão confiante o modelo está em identificar a classe correta (Waldo vs. fundo). Tende a cair rapidamente nas primeiras épocas.",
    "model.guide.dfl.desc":         "Distribution Focal Loss — mede a precisão dos limites do bounding box. Específico da arquitetura anchor-free do YOLOv8.",
    "model.guide.trainval.name":    "Treino vs. Validação",
    "model.guide.trainval.desc":    "Linhas sólidas = conjunto de treino; tracejadas = validação. As duas devem cair juntas e convergir. Uma diferença crescente indica overfitting.",
}

