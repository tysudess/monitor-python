from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QUrl, Qt, Signal
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from monitor_noticias.video_editor.window import VideoEditorWindow


LIGHT_EDITOR_STYLESHEET = """
QMainWindow { background:#F6FAFF; color:#0B2860; }
QWidget { color:#0B2860; font-family:'Segoe UI'; font-size:12px; }
QFrame#panel { background:#FFFFFF; border:1px solid #D7E6F7; border-radius:12px; }
QPushButton { background:#FFFFFF; color:#12336D; border:1px solid #D4E3F5; border-radius:9px; padding:9px 13px; font-weight:700; }
QPushButton:hover { background:#F0F7FF; border-color:#85B9F2; }
QPushButton:disabled { color:#91A5C1; background:#F4F7FB; border-color:#E3EAF3; }
QListWidget { background:#FFFFFF; color:#0B2860; border:1px solid #D7E6F7; border-radius:9px; padding:6px; }
QListWidget::item { padding:8px; border-radius:7px; }
QListWidget::item:selected { background:#EAF4FF; color:#075FDB; border:1px solid #83B9F5; }
QSlider::groove:horizontal { height:8px; background:#DCE9F7; border-radius:4px; }
QSlider::handle:horizontal { width:16px; height:16px; background:#168FFF; margin:-4px 0; border-radius:8px; }
QSlider::sub-page:horizontal { background:#168FFF; border-radius:4px; }
QStatusBar { background:#FFFFFF; color:#5E7397; border-top:1px solid #D7E6F7; }
QToolTip { background:#FFFFFF; color:#0B2860; border:1px solid #BCD4EE; }
"""


class VideoEditorPage(QWidget):
    """Hospeda o editor PySide6 dentro do QStackedWidget principal do Monitor.

    O motor do VideoEditorWindow (QMediaPlayer, QVideoWidget, timeline e FFmpeg)
    permanece intacto. A mudança é somente de hospedagem visual: o QMainWindow do
    editor vira um widget filho da página, portanto não abre outra janela.
    """

    back_requested = Signal()

    def __init__(self, app_root: Path) -> None:
        super().__init__()
        self.app_root = Path(app_root)
        self._build()

    def _build(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(8)

        toolbar = QFrame()
        toolbar.setObjectName("filterCard")
        tl = QHBoxLayout(toolbar)
        tl.setContentsMargins(14, 8, 14, 8)
        titles = QVBoxLayout()
        titles.setSpacing(1)
        title = QLabel("EDITOR DE VÍDEO")
        title.setObjectName("sectionTitle")
        subtitle = QLabel("Nenhum vídeo selecionado")
        subtitle.setObjectName("smallText")
        subtitle.setWordWrap(True)
        titles.addWidget(title)
        titles.addWidget(subtitle)
        tl.addLayout(titles, 1)
        integrated = QLabel("●  Integrado")
        integrated.setStyleSheet(
            "color:#09875d;border:1px solid #AEEBD4;background:#ECFBF5;"
            "border-radius:8px;padding:6px 10px;font-weight:700;"
        )
        tl.addWidget(integrated)
        back = QPushButton("←  Voltar ao Monitor")
        back.setProperty("secondary", True)
        back.clicked.connect(self.back_requested.emit)
        tl.addWidget(back)
        root.addWidget(toolbar)

        self.editor = VideoEditorWindow(self.app_root)
        self.editor.setWindowFlags(Qt.WindowType.Widget)
        self.editor.setParent(self)
        self.editor.setMinimumSize(0, 0)
        self.editor.setStyleSheet(LIGHT_EDITOR_STYLESHEET)

        # Mantém a compatibilidade com testes e chamadas antigas.
        self._windows = [self.editor]

        # A navegação principal do Monitor já ocupa a lateral; ocultamos apenas
        # a barra duplicada do editor, preservando preview, timeline e exportação.
        for frame in self.editor.findChildren(QFrame):
            if frame.minimumWidth() == 210 and frame.maximumWidth() == 210:
                frame.hide()

        # Ajustes de contraste de widgets que recebem estilo inline do motor.
        self.editor.video_widget.setStyleSheet(
            "background:black;border:1px solid #CFDFF1;border-radius:8px;"
        )
        root.addWidget(self.editor, 1)
        self.editor.show()

    def refresh(self, _state=None) -> None:
        pass

    def open_editor(self) -> None:
        self.editor.setFocus(Qt.FocusReason.OtherFocusReason)

    def shutdown(self) -> bool:
        try:
            self.editor.player.stop()
            self.editor.player.setSource(QUrl())
        except RuntimeError:
            return True
        return True
