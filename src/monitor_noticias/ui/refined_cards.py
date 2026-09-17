from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QAbstractItemView, QFrame, QHBoxLayout, QLabel, QPushButton, QTableWidget, QVBoxLayout, QWidget

from monitor_noticias.ui.refined_base import copy_text, format_time, open_url, open_whatsapp, secondary


class CardList(QTableWidget):
    def __init__(self) -> None:
        super().__init__(0, 1)
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.setShowGrid(False)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
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
    def __init__(self, item, actions_enabled: bool = True) -> None:
        super().__init__()
        self.setObjectName("resultCard")
        row = QHBoxLayout(self)
        row.setContentsMargins(16, 10, 16, 10)
        row.setSpacing(14)

        icon = QLabel("▤")
        icon.setFixedSize(46, 46)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setStyleSheet(
            "color:#087AF7;background:#EAF4FF;border:1px solid #C8DFF6;"
            "border-radius:9px;font-size:22px;font-weight:800;"
        )
        row.addWidget(icon, 0, Qt.AlignmentFlag.AlignVCenter)

        text = QVBoxLayout()
        text.setSpacing(2)
        meta = QLabel(f"{item.source} • {format_time(item.date)}")
        meta.setObjectName("smallText")
        text.addWidget(meta)
        title = QLabel(item.title)
        title.setWordWrap(True)
        title.setObjectName("smallTitle")
        text.addWidget(title)
        if getattr(item, "snippet", ""):
            snippet = QLabel(item.snippet)
            snippet.setWordWrap(True)
            snippet.setObjectName("smallText")
            text.addWidget(snippet)
        tags = " • ".join(
            x for x in [getattr(item, "matchedTerm", ""), getattr(item, "matchedDemand", "")] if x
        )
        if tags:
            tag = QLabel(f"Termo: {tags}")
            tag.setStyleSheet(
                "color:#075FDB;background:#EEF6FF;border:1px solid #BFD9F5;"
                "border-radius:7px;padding:3px 8px;max-width:430px;font-weight:700;"
            )
            text.addWidget(tag, 0, Qt.AlignmentFlag.AlignLeft)
        row.addLayout(text, 1)

        actions = QHBoxLayout()
        actions.setSpacing(8)
        open_btn = secondary(QPushButton("↗  Abrir matéria"))
        open_btn.clicked.connect(lambda: open_url(item.link))
        whats = QPushButton("◉  WhatsApp")
        whats.setProperty("green", True)
        whats.clicked.connect(lambda: open_whatsapp(item.title, item.link))
        copy = secondary(QPushButton("▣  Copiar link"))
        copy.clicked.connect(lambda: copy_text(item.link))
        if not actions_enabled:
            for button in (open_btn, whats, copy):
                button.setEnabled(False)
                button.setToolTip(
                    "A tela Histórico atual não possui esta ação vinculada; mantida apenas como referência visual."
                )
        actions.addWidget(open_btn)
        actions.addWidget(whats)
        actions.addWidget(copy)
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
        icon.setStyleSheet(
            "color:#7A3DF0;background:#F3EDFF;border:1px solid #DCCCF9;"
            "border-radius:23px;font-size:21px;"
        )
        row.addWidget(icon)

        text = QVBoxLayout()
        text.setSpacing(2)
        meta = QLabel(f"{item.sourceName} • {format_time(item.publishedAt)}")
        meta.setObjectName("smallText")
        text.addWidget(meta)
        title = QLabel(item.title)
        title.setWordWrap(True)
        title.setObjectName("smallTitle")
        text.addWidget(title)
        tags = " • ".join(
            x for x in [getattr(item, "matchedTerm", ""), getattr(item, "matchedDemand", "")] if x
        )
        if tags:
            tag = QLabel(f"Termo: {tags}")
            tag.setStyleSheet(
                "color:#6E33D6;background:#F6F0FF;border:1px solid #D9C5F7;"
                "border-radius:7px;padding:3px 8px;font-weight:700;"
            )
            text.addWidget(tag, 0, Qt.AlignmentFlag.AlignLeft)
        row.addLayout(text, 1)

        actions = QHBoxLayout()
        actions.setSpacing(8)
        op = secondary(QPushButton("↗  Abrir vídeo"))
        op.clicked.connect(lambda: open_url(item.link))
        wa = QPushButton("◉  WhatsApp")
        wa.setProperty("green", True)
        wa.clicked.connect(lambda: open_whatsapp(item.title, item.link))
        cp = secondary(QPushButton("▣  Copiar link"))
        cp.clicked.connect(lambda: copy_text(item.link))
        if not actions_enabled:
            for button in (op, wa, cp):
                button.setEnabled(False)
                button.setToolTip(
                    "A tela Histórico atual não possui esta ação vinculada; mantida apenas como referência visual."
                )
        actions.addWidget(op)
        actions.addWidget(wa)
        actions.addWidget(cp)
        row.addLayout(actions)
