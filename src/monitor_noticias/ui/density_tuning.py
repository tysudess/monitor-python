from __future__ import annotations

from PySide6.QtWidgets import QFrame, QLayout, QListWidget, QPushButton, QWidget


def _tighten_layout(layout: QLayout | None, spacing: int = 8) -> None:
    if layout is None:
        return
    current = layout.spacing()
    if current < 0 or current > spacing:
        layout.setSpacing(spacing)


def apply_density_tuning(window: QWidget) -> None:
    """Ajusta densidade visual sem tocar em dados, sinais ou motores das páginas."""
    pages = getattr(window, "pages", {})
    if not isinstance(pages, dict):
        return

    for page in pages.values():
        _tighten_layout(page.layout(), 8)
        root = getattr(page, "root", None)
        _tighten_layout(root, 8)

        for frame in page.findChildren(QFrame):
            _tighten_layout(frame.layout(), 7)
            name = frame.objectName()
            if name in {"filterCard", "statusCard"}:
                frame.setMinimumHeight(0)
            elif name in {"techCard", "resultCard"}:
                frame.setMinimumHeight(0)

        for button in page.findChildren(QPushButton):
            text = button.text().strip()
            if text and button.minimumHeight() > 42 and not text.startswith(("⇩   BAIXAR", "▤   GERAR PDF")):
                button.setMinimumHeight(38)

    home = next((p for p in pages.values() if p.__class__.__name__ == "HomeDashboard"), None)
    if home is not None:
        body_layout = getattr(home, "body_layout", None)
        _tighten_layout(body_layout, 10)
        if body_layout is not None:
            body_layout.setContentsMargins(14, 6, 14, 0)
        for frame in home.findChildren(QFrame):
            name = frame.objectName()
            if name == "metricCard":
                frame.setMinimumHeight(88)
            elif name == "dashboardCard":
                if frame.minimumHeight() > 240:
                    frame.setMinimumHeight(240)
            elif name == "miniCard":
                frame.setMinimumHeight(76)

    sources = next((p for p in pages.values() if p.__class__.__name__ == "SourcesPage"), None)
    if sources is not None:
        lst = getattr(sources, "list", None)
        if isinstance(lst, QListWidget):
            lst.setSpacing(2)

    settings = next((p for p in pages.values() if p.__class__.__name__ == "SettingsPage"), None)
    if settings is not None:
        for frame in settings.findChildren(QFrame):
            if frame.minimumWidth() > 500:
                frame.setMinimumWidth(0)

    pdf = next((p for p in pages.values() if p.__class__.__name__ == "RefinedPdfEditorPage"), None)
    if pdf is not None:
        for frame in pdf.findChildren(QFrame):
            _tighten_layout(frame.layout(), 6)

    extractor = next((p for p in pages.values() if p.__class__.__name__ == "RefinedExtractorPage"), None)
    if extractor is not None:
        for frame in extractor.findChildren(QFrame):
            _tighten_layout(frame.layout(), 7)
