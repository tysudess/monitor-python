from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractItemView, QFrame, QHBoxLayout, QLabel, QPushButton, QTableWidget, QVBoxLayout, QWidget

from monitor_noticias.ui.refined_base import (
    copy_text,
    copy_news_url,
    format_time,
    open_news_url,
    open_news_whatsapp,
    open_url,
    open_whatsapp,
    secondary,
)


class CardList(QTableWidget):
    def __init__(self) -> None:
        super().__init__(0, 1)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.setShowGrid(False)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.verticalScrollBar().setSingleStep(20)
        self.horizontalScrollBar().setSingleStep(20)
        self.horizontalHeader().setStretchLastSection(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet(
            "QTableWidget{background:transparent;border:0;}"
            "QTableWidget::item{padding:0;margin:0;border:0;background:transparent;}"
        )

    def set_cards(self, cards: list[QWidget], heights: list[int] | None = None) -> None:
        self.setRowCount(len(cards))
        for row, widget in enumerate(cards):
            height = heights[row] if heights else 104
            self.setRowHeight(row, height)
            self.setCellWidget(row, 0, widget)


class NewsCard(QFrame):
    def __init__(self, item, actions_enabled: bool = True, reference_style: bool = False) -> None:
        super().__init__()
        self.setObjectName("resultCard")
        row = QHBoxLayout(self)
        row.setContentsMargins(0 if reference_style else 16, 6 if reference_style else 10, 10 if reference_style else 16, 6 if reference_style else 10)
        row.setSpacing(10 if reference_style else 14)

        if reference_style:
            palette = ("#087AF7", "#8A3FF0", "#F0A000", "#13B889", "#27A9E8")
            accent = palette[sum(ord(ch) for ch in (item.source or item.title)) % len(palette)]
            stripe = QFrame(); stripe.setFixedWidth(4); stripe.setStyleSheet(f"background:{accent};border:0;border-radius:2px;")
            row.addWidget(stripe)
            initials = "".join(part[:1].upper() for part in (item.source or "N").replace("-", " ").split()[:2]) or "N"
            icon = QLabel(initials)
            icon.setFixedSize(38, 38)
            icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon.setStyleSheet(f"color:#FFFFFF;background:{accent};border-radius:8px;font-size:13px;font-weight:900;")
        else:
            icon = QLabel("▤")
            icon.setFixedSize(46, 46)
            icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon.setStyleSheet("color:#087AF7;background:#EAF4FF;border:1px solid #C8DFF6;border-radius:9px;font-size:22px;font-weight:800;")
        row.addWidget(icon, 0, Qt.AlignmentFlag.AlignVCenter)

        text = QVBoxLayout(); text.setSpacing(1 if reference_style else 2)
        meta = QLabel(f"{item.source}  •  {format_time(item.date)}")
        meta.setStyleSheet("color:#4E6E9B;font-size:9px;" if reference_style else "")
        if not reference_style: meta.setObjectName("smallText")
        text.addWidget(meta)
        title = QLabel(item.title); title.setWordWrap(True)
        if reference_style:
            title.setStyleSheet("color:#08245A;font-size:11px;font-weight:800;")
        else:
            title.setObjectName("smallTitle")
        text.addWidget(title)
        if getattr(item, "snippet", ""):
            snippet = QLabel(item.snippet); snippet.setWordWrap(True)
            if reference_style:
                snippet.setMaximumHeight(28); snippet.setStyleSheet("color:#657EA5;font-size:9px;")
            else:
                snippet.setObjectName("smallText")
            text.addWidget(snippet)
        tags = " • ".join(x for x in [getattr(item, "matchedTerm", ""), getattr(item, "matchedDemand", "")] if x)
        if tags:
            tag = QLabel(("TERMO: " if reference_style else "Termo: ") + tags)
            tag.setStyleSheet(
                "color:#0871E8;background:#EEF6FF;border:1px solid #C6E0FA;border-radius:6px;padding:2px 7px;font-size:8px;font-weight:800;max-width:280px;"
                if reference_style else
                "color:#075FDB;background:#EEF6FF;border:1px solid #BFD9F5;border-radius:7px;padding:3px 8px;max-width:430px;font-weight:700;"
            )
            text.addWidget(tag, 0, Qt.AlignmentFlag.AlignLeft)
        row.addLayout(text, 1)

        actions = QHBoxLayout(); actions.setSpacing(6 if reference_style else 8)
        open_btn = secondary(QPushButton("↗  Abrir matéria"))
        open_btn.clicked.connect(lambda: open_news_url(item.link, item.title, item.source))
        whats = QPushButton("◉  WhatsApp"); whats.setProperty("green", True)
        whats.clicked.connect(lambda: open_news_whatsapp(item.title, item.link, item.source))
        copy = secondary(QPushButton("▣  Copiar link"))
        copy.clicked.connect(lambda: copy_news_url(item.link, item.title, item.source))
        buttons = [open_btn, whats, copy]
        if reference_style:
            extract = QPushButton("⇩  Extrair matéria")
            extract.setStyleSheet("QPushButton{background:#F7EDFF;color:#8A2BE2;border:1px solid #E1C6F7;border-radius:8px;padding:7px 10px;font-weight:700;}QPushButton:hover{background:#F1E3FF;}")
            extract.setToolTip("A extração de matéria não faz parte desta base; o botão foi preservado para fidelidade visual.")
            extract.setEnabled(False)
            buttons.append(extract)
        if reference_style:
            for button in buttons: button.setMinimumHeight(30)
        if not actions_enabled:
            for button in buttons:
                button.setEnabled(False)
                button.setToolTip("A tela Histórico atual não possui esta ação vinculada; mantida apenas como referência visual.")
        for button in buttons: actions.addWidget(button)
        row.addLayout(actions)


class VideoCard(QFrame):
    def __init__(self, item, actions_enabled: bool = True) -> None:
        super().__init__()
        self.setObjectName("resultCard")
        row = QHBoxLayout(self)
        row.setContentsMargins(16, 10, 16, 10)
        row.setSpacing(14)

        icon = QLabel("▶")
        icon.setFixedSize(46, 46)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet("color:#7A3DF0;background:#F3EDFF;border:1px solid #DCCCF9;border-radius:23px;font-size:21px;")
        row.addWidget(icon)

        text = QVBoxLayout(); text.setSpacing(2)
        meta = QLabel(f"{item.sourceName} • {format_time(item.publishedAt)}"); meta.setObjectName("smallText"); text.addWidget(meta)
        title = QLabel(item.title); title.setWordWrap(True); title.setObjectName("smallTitle"); text.addWidget(title)
        tags = " • ".join(x for x in [getattr(item, "matchedTerm", ""), getattr(item, "matchedDemand", "")] if x)
        if tags:
            tag = QLabel(f"Termo: {tags}")
            tag.setStyleSheet("color:#6E33D6;background:#F6F0FF;border:1px solid #D9C5F7;border-radius:7px;padding:3px 8px;font-weight:700;")
            text.addWidget(tag, 0, Qt.AlignmentFlag.AlignLeft)
        row.addLayout(text, 1)

        actions = QHBoxLayout(); actions.setSpacing(8)
        op = secondary(QPushButton("↗  Abrir vídeo")); op.clicked.connect(lambda: open_url(item.link))
        wa = QPushButton("◉  WhatsApp"); wa.setProperty("green", True); wa.clicked.connect(lambda: open_whatsapp(item.title, item.link))
        cp = secondary(QPushButton("▣  Copiar link")); cp.clicked.connect(lambda: copy_text(item.link))
        if not actions_enabled:
            for button in (op, wa, cp):
                button.setEnabled(False)
                button.setToolTip("A tela Histórico atual não possui esta ação vinculada; mantida apenas como referência visual.")
        actions.addWidget(op); actions.addWidget(wa); actions.addWidget(cp); row.addLayout(actions)
