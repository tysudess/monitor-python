from __future__ import annotations

from datetime import datetime
from os import environ
from time import monotonic

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout

from monitor_noticias.ui.home_runtime_features import WEATHER_REFRESH_SECONDS, WeatherThread


SECTION_ACCENTS = {
    "Início": ("⌂", "#167CF2"),
    "Notícias": ("▤", "#167CF2"),
    "Vídeos": ("▶", "#6F45E8"),
    "Demandas": ("▣", "#167CF2"),
    "Fontes": ("▤", "#167CF2"),
    "Histórico": ("↺", "#167CF2"),
    "Termos": ("⌕", "#167CF2"),
    "Parar buscas": ("■", "#E44259"),
    "Configurações": ("⚙", "#167CF2"),
    "Editor de PDF": ("▣", "#167CF2"),
    "Extrator de Vídeos": ("⇩", "#D99300"),
    "Editor de Vídeo": ("▰", "#6F45E8"),
}


class RadarHeader(QFrame):
    """Cabeçalho compartilhado; Notícias usa o modo de barra de busca da referência."""

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("pageHeader")
        self.setMinimumHeight(72)
        self.setMaximumHeight(82)
        self._weather_thread: WeatherThread | None = None
        self._weather_last_started = 0.0
        self._weather_value: float | None = None

        root = QHBoxLayout(self)
        root.setContentsMargins(12, 6, 10, 6)
        root.setSpacing(9)

        self.icon = QLabel("▤")
        self.icon.setObjectName("pageIcon")
        self.icon.setFixedWidth(38)
        self.icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        root.addWidget(self.icon)

        self.identity = QFrame()
        self.identity.setStyleSheet("background:transparent;border:0;")
        text = QVBoxLayout(self.identity)
        text.setContentsMargins(0,0,0,0)
        text.setSpacing(1)
        kicker_row = QHBoxLayout(); kicker_row.setSpacing(6)
        self.gold = QLabel("▌"); self.gold.setStyleSheet("color:#F2B715;font-size:18px;font-weight:900;")
        kicker_row.addWidget(self.gold)
        self.kicker = QLabel("CENTRAL DE INTELIGÊNCIA DE MÍDIA"); self.kicker.setObjectName("pageKicker"); kicker_row.addWidget(self.kicker); kicker_row.addStretch(); text.addLayout(kicker_row)
        self.title = QLabel(); self.title.setObjectName("pageTitle"); text.addWidget(self.title)
        self.subtitle = QLabel(); self.subtitle.setObjectName("pageSubtitle"); text.addWidget(self.subtitle)
        root.addWidget(self.identity, 4)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("⌕   Buscar notícias, fontes, demandas... ou digite um comando (Ctrl + K)")
        self.search_box.setMinimumHeight(40)
        self.search_box.setMinimumWidth(470)
        self.search_box.setMaximumWidth(640)
        self.search_box.hide()
        root.addWidget(self.search_box, 5)

        root.addStretch(1)

        self.proxy_pill, self.proxy_label = self._pill("pillGreen", "●", "Proxy pronto", "#0BAA73")
        root.addWidget(self.proxy_pill, 0, Qt.AlignmentFlag.AlignVCenter)
        self.auto_pill, self.auto_label = self._pill("pillGreen", "●", "Automação ativa", "#0BAA73")
        root.addWidget(self.auto_pill, 0, Qt.AlignmentFlag.AlignVCenter)

        action = QFrame(); action.setObjectName("pillBlue")
        al = QHBoxLayout(action); al.setContentsMargins(10, 6, 10, 6)
        diamond = QLabel("◇"); diamond.setStyleSheet("color:#117AF0;font-size:17px;font-weight:900;"); diamond.setAlignment(Qt.AlignmentFlag.AlignCenter); al.addWidget(diamond)
        root.addWidget(action, 0, Qt.AlignmentFlag.AlignVCenter)

        clock = QFrame(); clock.setObjectName("pillBlue")
        clock_box = QHBoxLayout(clock); clock_box.setContentsMargins(10, 5, 10, 5); clock_box.setSpacing(9)
        date_time = QVBoxLayout(); date_time.setSpacing(0)
        self.date_label = QLabel(); self.date_label.setObjectName("smallText")
        self.clock_label = QLabel(); self.clock_label.setStyleSheet("color:#08245A;font-size:15px;font-weight:800;")
        date_time.addWidget(self.date_label); date_time.addWidget(self.clock_label); clock_box.addLayout(date_time)
        divider = QFrame(); divider.setFixedWidth(1); divider.setMinimumHeight(34); divider.setStyleSheet("background:#D9E6F3;border:0;"); clock_box.addWidget(divider)
        sun = QLabel("☀"); sun.setStyleSheet("color:#F6B700;font-size:23px;font-weight:800;"); clock_box.addWidget(sun)
        wt = QVBoxLayout(); wt.setSpacing(0)
        city = QLabel("Brasília - DF"); city.setObjectName("smallText")
        self.weather_temp = QLabel("--°C"); self.weather_temp.setStyleSheet("color:#08245A;font-size:13px;font-weight:800;")
        wt.addWidget(city); wt.addWidget(self.weather_temp); clock_box.addLayout(wt)
        root.addWidget(clock, 0, Qt.AlignmentFlag.AlignVCenter)

    @staticmethod
    def _pill(name: str, glyph: str, text: str, color: str):
        frame = QFrame(); frame.setObjectName(name)
        lay = QHBoxLayout(frame); lay.setContentsMargins(9, 6, 9, 6); lay.setSpacing(6)
        icon = QLabel(glyph); icon.setStyleSheet(f"color:{color};font-size:11px;font-weight:900;")
        label = QLabel(text); label.setStyleSheet("color:#11386D;font-weight:700;")
        lay.addWidget(icon); lay.addWidget(label)
        return frame, label

    def set_section(self, title: str, subtitle: str) -> None:
        news_mode = title == "Notícias"
        self.identity.setVisible(not news_mode)
        self.icon.setVisible(not news_mode)
        self.search_box.setVisible(news_mode)
        self.title.setText(title)
        self.subtitle.setText(subtitle)
        glyph, color = SECTION_ACCENTS.get(title, ("▤", "#167CF2"))
        self.icon.setText(glyph)
        self.icon.setStyleSheet(f"color:{color};font-size:25px;font-weight:800;background:#EEF6FF;border:1px solid #D9E9F8;border-radius:10px;padding:4px;")

    def update_runtime(self, controller) -> None:
        now = datetime.now()
        self.date_label.setText(now.strftime("%d/%m/%Y"))
        self.clock_label.setText(now.strftime("%H:%M:%S"))
        cfg = controller.proxy_config; auto = controller.automation_settings
        status = cfg.status_label.strip() or "Proxy"
        self.proxy_label.setText(status)
        self.auto_label.setText(f"Automação {'ativa' if auto.automatic_monitoring else 'pausada'}")
        self._maybe_weather()

    def _maybe_weather(self) -> None:
        if self._weather_value is not None:
            self.weather_temp.setText(f"{round(self._weather_value)}°C")
        if environ.get("QT_QPA_PLATFORM", "").strip().lower() == "offscreen": return
        if environ.get("MONITOR_DISABLE_WEATHER", "").strip().lower() in {"1", "true", "yes"}: return
        if self._weather_thread is not None and self._weather_thread.isRunning(): return
        now = monotonic()
        if self._weather_last_started and now - self._weather_last_started < WEATHER_REFRESH_SECONDS: return
        self._weather_last_started = now
        worker = WeatherThread(self); self._weather_thread = worker
        worker.succeeded.connect(self._weather_ok)
        worker.failed.connect(lambda detail: self.weather_temp.setToolTip(f"Temperatura indisponível: {detail}"))
        worker.finished.connect(lambda: setattr(self, "_weather_thread", None))
        worker.start()

    def _weather_ok(self, value: float) -> None:
        self._weather_value = float(value)
        self.weather_temp.setText(f"{round(value)}°C")
        self.weather_temp.setToolTip("Temperatura atual de Brasília - DF")


class TechFooter(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("footerFrame")
        self.setFixedHeight(34)
        row = QHBoxLayout(self); row.setContentsMargins(2, 3, 2, 3); row.setSpacing(9)
        self.left = QLabel("Monitor de Notícias v4.0.2   •   Inteligência de mídia"); self.left.setObjectName("smallText"); row.addWidget(self.left)
        row.addStretch()
        self.status = QLabel("●  Sistema operacional"); self.status.setStyleSheet("color:#4F6E98;font-size:9px;"); row.addWidget(self.status)

    def set_busy(self, busy: bool) -> None:
        self.status.setText("●  Busca em andamento" if busy else "●  Sistema operacional")
        self.status.setStyleSheet("color:#C78900;font-size:9px;" if busy else "color:#078C63;font-size:9px;")
