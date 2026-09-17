from __future__ import annotations

from PySide6.QtCore import QDate, Qt, QTime
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDateEdit,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QTimeEdit,
    QVBoxLayout,
)

from monitor_noticias.ui.controller import MainUiController
from monitor_noticias.ui.refined_base import BasePage, ExecutionPanel, card, dangerous, duration, secondary
from monitor_noticias.ui.refined_cards import CardList, NewsCard, VideoCard


class NewsPage(BasePage):
    PAGE_SIZE = 5

    def __init__(self, controller: MainUiController) -> None:
        super().__init__(controller)
        self._signature = None
        self._page = 0
        self._period_buttons: list[QPushButton] = []
        self.root.setSpacing(9)

        self.setStyleSheet(
            "QFrame#newsHero{background:#FFFFFF;border:1px solid #D9E8F7;border-radius:13px;}"
            "QLabel#newsHeroKicker{color:#147BF3;font-size:10px;font-weight:800;letter-spacing:1px;}"
            "QLabel#newsHeroTitle{color:#08245A;font-size:29px;font-weight:900;}"
            "QLabel#newsHeroSub{color:#5F77A1;font-size:12px;}"
            "QLabel#newsHeroArt{color:#DCEBFA;font-size:43px;font-weight:800;}"
            "QFrame#newsStatusCard,QFrame#newsMetricsCard{background:#FFFFFF;border:1px solid #D9E8F7;border-radius:12px;}"
            "QLabel#newsStatusTitle{color:#08245A;font-size:16px;font-weight:900;}"
            "QLabel#newsStatusSub{color:#637AA0;font-size:10px;}"
            "QLabel#newsSuccessStrip{color:#087B57;background:#EEFAF5;border:1px solid #B8E7D5;border-radius:6px;padding:5px 9px;}"
            "QComboBox#newsSort{min-width:118px;max-width:138px;min-height:28px;}"
            "QPushButton#newsPager{min-width:32px;max-width:38px;padding:5px 8px;}"
        )

        hero = QFrame(); hero.setObjectName("newsHero"); hero.setFixedHeight(118)
        hl = QHBoxLayout(hero); hl.setContentsMargins(18, 11, 18, 11); hl.setSpacing(12)
        hero_text = QVBoxLayout(); hero_text.setSpacing(1)
        kicker = QLabel("CENTRAL DE INTELIGÊNCIA DE MÍDIA"); kicker.setObjectName("newsHeroKicker")
        title = QLabel("Notícias"); title.setObjectName("newsHeroTitle")
        subtitle = QLabel("Acompanhe matérias em tempo real e transforme\ninformação em decisões estratégicas."); subtitle.setObjectName("newsHeroSub")
        hero_text.addWidget(kicker); hero_text.addWidget(title); hero_text.addWidget(subtitle); hero_text.addStretch()
        hl.addLayout(hero_text, 1)
        art = QLabel("◯     ▤"); art.setObjectName("newsHeroArt"); art.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        hl.addWidget(art)
        self.root.addWidget(hero)

        top, tl = card("filterCard", (10, 9, 10, 9), 7)
        first = QHBoxLayout(); first.setSpacing(8)
        self.query = QLineEdit(); self.query.setPlaceholderText("⌕   Buscar nas notícias (título, fonte, termo...)"); self.query.setMinimumHeight(36)
        self.only_demands = QCheckBox("Só demandas")
        self.search24 = QPushButton("⟳  Buscar últimas 24h"); self.search24.setMinimumHeight(36)
        self.search24.clicked.connect(lambda: controller.search_news(*controller.period_last_hours(24)))
        first.addWidget(self.query, 1); first.addWidget(self.search24); first.addWidget(self.only_demands)
        tl.addLayout(first)

        periods = QHBoxLayout(); periods.setSpacing(7)
        for index, (label, hours) in enumerate((("Hoje", None), ("24 horas", 24), ("7 dias", 168), ("30 dias", 720))):
            button = secondary(QPushButton(label)); button.setCheckable(True); button.setMinimumHeight(30)
            button.setChecked(index == 0)
            button.clicked.connect(lambda _=False, h=hours, b=button: self._run_period(h, b))
            self._period_buttons.append(button); periods.addWidget(button)
        self.custom = secondary(QPushButton("▣  Período personalizado")); self.custom.setCheckable(True); self.custom.setMinimumHeight(30)
        self.custom.toggled.connect(self._toggle_custom); periods.addWidget(self.custom); periods.addStretch(); tl.addLayout(periods)

        self.period_box = QFrame(); form = QHBoxLayout(self.period_box); form.setContentsMargins(0, 2, 0, 0); form.setSpacing(7)
        today = QDate.currentDate(); self.start_date = QDateEdit(today.addDays(-1)); self.start_time = QTimeEdit(QTime(0, 0)); self.end_date = QDateEdit(today); self.end_time = QTimeEdit(QTime(23, 59)); self.period_go = QPushButton("Buscar período")
        for widget in (self.start_date, self.start_time, self.end_date, self.end_time, self.period_go): form.addWidget(widget)
        self.period_box.hide(); self.period_go.clicked.connect(self._period); tl.addWidget(self.period_box)
        self.root.addWidget(top)

        execution_row = QHBoxLayout(); execution_row.setSpacing(9)
        status_card = QFrame(); status_card.setObjectName("newsStatusCard")
        sl = QVBoxLayout(status_card); sl.setContentsMargins(13, 10, 13, 10); sl.setSpacing(6)
        srow = QHBoxLayout(); srow.setSpacing(9)
        self.status_icon = QLabel("✓"); self.status_icon.setFixedSize(44, 44); self.status_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_icon.setStyleSheet("color:#079C69;background:#E7F8F1;border:1px solid #B7E7D4;border-radius:22px;font-size:25px;font-weight:900;")
        srow.addWidget(self.status_icon)
        st = QVBoxLayout(); st.setSpacing(0)
        self.status_title = QLabel("Busca concluída com sucesso"); self.status_title.setObjectName("newsStatusTitle")
        self.status_sub = QLabel("Pronto"); self.status_sub.setObjectName("newsStatusSub")
        st.addWidget(self.status_title); st.addWidget(self.status_sub); srow.addLayout(st, 1)
        self.status_pct = QLabel("100%"); self.status_pct.setStyleSheet("color:#08A86F;font-size:18px;font-weight:900;")
        srow.addWidget(self.status_pct, 0, Qt.AlignmentFlag.AlignTop)
        sl.addLayout(srow)
        self.progress = QProgressBar(); self.progress.setRange(0, 100); self.progress.setTextVisible(False); self.progress.setValue(100); sl.addWidget(self.progress)
        self.detail = QLabel("A busca foi concluída."); self.detail.setObjectName("newsSuccessStrip"); sl.addWidget(self.detail)
        execution_row.addWidget(status_card, 58)

        metrics_card = QFrame(); metrics_card.setObjectName("newsMetricsCard")
        ml = QHBoxLayout(metrics_card); ml.setContentsMargins(8, 13, 8, 11); ml.setSpacing(0)
        self.metric_labels: dict[str, QLabel] = {}
        colors = {"pct":"#08A86F","found":"#E09500","fresh":"#8B3FF0","errors":"#E13650","steps":"#087AF7","time":"#087AF7"}
        for i, (key, caption, glyph) in enumerate((("pct","Conclusão","◎"),("found","Encontradas","▤"),("fresh","Novas","✦"),("errors","Falhas","!"),("steps","Etapas","☷"),("time","Tempo","◷"))):
            if i:
                sep = QFrame(); sep.setFixedWidth(1); sep.setStyleSheet("background:#E5EDF6;border:0;"); ml.addWidget(sep)
            col = QVBoxLayout(); col.setSpacing(1)
            icon = QLabel(glyph); icon.setAlignment(Qt.AlignmentFlag.AlignCenter); icon.setStyleSheet(f"color:{colors[key]};font-size:15px;font-weight:900;")
            value = QLabel("0"); value.setAlignment(Qt.AlignmentFlag.AlignCenter); value.setStyleSheet(f"color:{colors[key]};font-size:16px;font-weight:900;")
            cap = QLabel(caption); cap.setAlignment(Qt.AlignmentFlag.AlignCenter); cap.setObjectName("smallText")
            col.addWidget(icon); col.addWidget(value); col.addWidget(cap); ml.addLayout(col, 1); self.metric_labels[key] = value
        execution_row.addWidget(metrics_card, 42)
        self.root.addLayout(execution_row)

        self.stop = dangerous(QPushButton("■  Parar busca")); self.stop.clicked.connect(controller.stop_news_search); self.root.addWidget(self.stop, 0, Qt.AlignmentFlag.AlignLeft)

        results_head = QHBoxLayout(); results_head.setSpacing(8)
        results_title = QLabel("▤  Notícias encontradas"); results_title.setObjectName("sectionTitle")
        self.count = QLabel(); self.count.setObjectName("smallText")
        results_head.addWidget(results_title); results_head.addWidget(self.count); results_head.addStretch()
        self.sort = QComboBox(); self.sort.setObjectName("newsSort"); self.sort.addItems(["Mais recentes", "Mais antigas"]); self.sort.currentIndexChanged.connect(self._sort_changed); results_head.addWidget(self.sort)
        self.prev = secondary(QPushButton("‹")); self.prev.setObjectName("newsPager"); self.prev.clicked.connect(lambda: self._change_page(-1)); results_head.addWidget(self.prev)
        self.page_label = QLabel("1 de 1"); self.page_label.setObjectName("smallText"); results_head.addWidget(self.page_label)
        self.next = secondary(QPushButton("›")); self.next.setObjectName("newsPager"); self.next.clicked.connect(lambda: self._change_page(1)); results_head.addWidget(self.next)
        self.root.addLayout(results_head)

        self.list = CardList(); self.root.addWidget(self.list, 1)
        self.query.textChanged.connect(self._filters_changed); self.only_demands.toggled.connect(self._filters_changed)

    def _toggle_custom(self, checked: bool) -> None:
        if checked:
            for button in self._period_buttons: button.setChecked(False)
        self.period_box.setVisible(checked)

    def _run_period(self, hours, button: QPushButton) -> None:
        for item in self._period_buttons: item.setChecked(item is button)
        self.custom.setChecked(False)
        self.controller.search_news(*(self.controller.period_today() if hours is None else self.controller.period_last_hours(hours)))

    def _period(self) -> None:
        p = self.controller.parse_period(self.start_date.date().toString("yyyy-MM-dd"), self.start_time.time().toString("HH:mm"), self.end_date.date().toString("yyyy-MM-dd"), self.end_time.time().toString("HH:mm"))
        if p: self.controller.search_news(*p)

    def _filters_changed(self, *_args) -> None:
        self._page = 0; self._signature = None; self.refresh(self.controller.state)

    def _sort_changed(self, *_args) -> None:
        self._page = 0; self._signature = None; self.refresh(self.controller.state)

    def _change_page(self, delta: int) -> None:
        self._page = max(0, self._page + delta); self._signature = None; self.refresh(self.controller.state)

    def _rows(self, state):
        q = self.query.text().strip().lower()
        rows = [n for n in state.news if (not self.only_demands.isChecked() or n.demand) and (not q or q in f"{n.title} {n.source} {n.matchedTerm} {n.matchedDemand}".lower())]
        rows.sort(key=lambda n: n.date, reverse=self.sort.currentIndex() == 0)
        return rows

    def refresh(self, state) -> None:
        rows = self._rows(state)
        found = int(getattr(state.news_progress, "found", 0)); fresh = len(state.new_news_links); errors = int(getattr(state.news_progress, "errors", 0)); completed = int(getattr(state.news_progress, "completed", 0)); total = int(getattr(state.news_progress, "total", 0))
        fraction = max(0.0, min(1.0, float(getattr(state.news_progress, "fraction", 0.0)))) if state.news_busy else 1.0
        pct = round(fraction * 100)
        self.search24.setEnabled(not state.news_busy and self.controller.search_available); self.period_go.setEnabled(not state.news_busy and self.controller.search_available); self.stop.setVisible(state.news_busy)
        self.progress.setValue(pct); self.status_pct.setText(f"{pct}%")
        self.metric_labels["pct"].setText(f"{pct}%"); self.metric_labels["found"].setText(str(found)); self.metric_labels["fresh"].setText(str(fresh)); self.metric_labels["errors"].setText(str(errors)); self.metric_labels["steps"].setText(f"{completed}/{total}"); self.metric_labels["time"].setText(duration(state.last_news_duration_ms))
        if state.news_busy:
            self.status_title.setText("Busca de notícias em andamento"); self.status_sub.setText(state.status or "Buscando..."); self.detail.setText(f"{getattr(state.news_progress, 'currentSource', '') or 'Preparando'} • {getattr(state.news_progress, 'currentQuery', '') or 'Consultando fontes'}")
        else:
            self.status_title.setText("Busca concluída com sucesso"); self.status_sub.setText(f"{len(rows)} resultado(s) • {fresh} novo(s)"); self.detail.setText(f"A busca foi concluída. {found or len(rows)} notícia(s) encontrada(s) nesta execução.")

        pages = max(1, (len(rows) + self.PAGE_SIZE - 1) // self.PAGE_SIZE)
        self._page = min(self._page, pages - 1)
        start = self._page * self.PAGE_SIZE; visible = rows[start:start + self.PAGE_SIZE]
        self.count.setText(f"{len(rows)} resultado(s) para o período selecionado")
        self.page_label.setText(f"{self._page + 1} de {pages}"); self.prev.setEnabled(self._page > 0); self.next.setEnabled(self._page + 1 < pages)
        signature = (self.query.text(), self.only_demands.isChecked(), self.sort.currentIndex(), self._page, tuple((getattr(n, "id", 0), n.link, n.title, n.date, n.matchedTerm, n.matchedDemand, getattr(n, "snippet", "")) for n in visible))
        if signature != self._signature:
            self._signature = signature
            cards = [NewsCard(n, reference_style=True) for n in visible]
            heights = [82 if not getattr(n, "snippet", "") else 96 for n in visible]
            self.list.set_cards(cards, heights)


class VideosPage(BasePage):
    def __init__(self,controller):
        super().__init__(controller); self._signature=None
        top,tl=card("filterCard",(16,12,16,12),9); row=QHBoxLayout(); row.setSpacing(12)
        self.query=QLineEdit(); self.query.setPlaceholderText("⌕   Buscar nos vídeos (título, fonte, termo...)"); row.addWidget(self.query,1)
        self.run=QPushButton("⟳  Buscar vídeos agora"); self.run.clicked.connect(controller.search_videos); row.addWidget(self.run); tl.addLayout(row)
        prow=QHBoxLayout(); prow.setSpacing(9)
        for label,h in (("24 horas",24),("7 dias",168),("30 dias",720)):
            b=secondary(QPushButton(label)); b.clicked.connect(lambda _=False,h=h: controller.search_videos(*controller.period_last_hours(h))); prow.addWidget(b)
        custom=secondary(QPushButton("Período personalizado")); custom.setEnabled(False); custom.setToolTip("O motor atual de vídeos não expõe período personalizado nesta tela."); prow.addWidget(custom); prow.addStretch(); tl.addLayout(prow); self.root.addWidget(top)
        self.exec=ExecutionPanel("Vídeos"); self.root.addWidget(self.exec)
        self.stop=dangerous(QPushButton("■  Parar busca")); self.stop.clicked.connect(controller.stop_video_search); self.root.addWidget(self.stop,0,Qt.AlignmentFlag.AlignLeft)
        self.warning=QLabel(); self.warning.setWordWrap(True); self.warning.setStyleSheet("color:#ffd34d;background:#3a3215;border:1px solid #9b7e0a;border-radius:7px;padding:6px 9px;"); self.warning.hide(); self.root.addWidget(self.warning)
        hr=QHBoxLayout(); title=QLabel("Vídeos encontrados"); title.setObjectName("sectionTitle"); self.count=QLabel(); self.count.setObjectName("smallText"); hr.addWidget(title); hr.addStretch(); hr.addWidget(self.count); self.root.addLayout(hr)
        self.list=CardList(); self.root.addWidget(self.list,1)
        self.empty=QFrame(); self.empty.setObjectName("emptyPanel"); el=QVBoxLayout(self.empty); el.addStretch(); play=QLabel("▶"); play.setAlignment(Qt.AlignmentFlag.AlignCenter); play.setStyleSheet("color:#b45cff;font-size:38px;"); el.addWidget(play); et=QLabel("Nenhum vídeo nesta visualização"); et.setAlignment(Qt.AlignmentFlag.AlignCenter); et.setObjectName("sectionTitle"); el.addWidget(et); es=QLabel("Execute uma busca manual ou selecione outras fontes de vídeo."); es.setAlignment(Qt.AlignmentFlag.AlignCenter); es.setObjectName("smallText"); el.addWidget(es); el.addStretch(); self.root.addWidget(self.empty,1)
        self.query.textChanged.connect(lambda _:self.refresh(controller.state))

    def refresh(self,state):
        q=self.query.text().strip().lower(); rows=[v for v in state.videos if not q or q in f"{v.title} {v.sourceName} {v.matchedTerm} {v.matchedDemand}".lower()]
        self.count.setText(f"{len(rows)} exibido(s)"); self.run.setEnabled(not state.video_busy and self.controller.search_available); self.stop.setVisible(state.video_busy); self.exec.set_state(state.video_busy,state.video_progress,state.video_status,len(state.new_video_links),state.last_video_duration_ms)
        if state.unstable_video_sources: self.warning.setText("Fontes com instabilidade: "+" • ".join(str(getattr(x,"sourceName",x)) for x in state.unstable_video_sources)); self.warning.show()
        else: self.warning.hide()
        self.list.setVisible(bool(rows)); self.empty.setVisible(not rows)
        signature=(self.query.text(),tuple((getattr(v,"id",0),v.link,v.title,v.publishedAt,v.matchedTerm,v.matchedDemand) for v in rows))
        if signature!=self._signature:
            self._signature=signature; self.list.set_cards([VideoCard(v) for v in rows],[106]*len(rows))
