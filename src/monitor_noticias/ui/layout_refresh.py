from __future__ import annotations

from PySide6.QtWidgets import QFrame, QLabel, QListWidget, QPushButton, QWidget


HOME_LIGHT_OVERRIDE = """
QWidget#homeDashboard, QWidget#homeBody { background:#F6FAFF; color:#0B2860; }
QScrollArea#homeScroll, QScrollArea#homeScroll QWidget#qt_scrollarea_viewport { background:#F6FAFF; }
QLabel { color:#0B2860; background:transparent; }
QLabel#homeWelcome, QLabel#heroTitle, QLabel#metricValue, QLabel#cardTitle { color:#0A225B; }
QLabel#homeSubtitle, QLabel#cardSubtitle, QLabel#heroBody, QLabel#summaryName,
QLabel#smallContent, QLabel#footerText, QLabel#footerStatus { color:#5A7197; }
QLabel#homeSlogan, QLabel#kicker, QLabel#heroRail { color:#087AF7; }
QLabel#homeDate { color:#6A80A4; }
QLabel#homeClock, QLabel#homeWeatherTemp { color:#0A225B; }
QLabel#homeWeatherCity { color:#60779D; }
QLineEdit#homeSearch { background:#FFFFFF; color:#0B2860; border:1px solid #CFE0F4; border-radius:10px; padding:10px 14px; }
QLineEdit#homeSearch:focus { border:1px solid #69A9F1; }
QFrame#metricCard, QFrame#dashboardCard, QFrame#miniCard { background:#FFFFFF; border:1px solid #D7E6F7; border-radius:12px; }
QFrame#metricCard:hover, QFrame#dashboardCard:hover { border-color:#9FC6F2; }
QLabel#metricTitle { color:#4F678E; }
QFrame#statusPanel { background:#ECFBF5; border:1px solid #A9E9D1; }
QLabel#statusReady { color:#07865F; }
QLabel#statusPct { color:#0A225B; }
QProgressBar#homeProgress { background:#E1ECF7; border:0; border-radius:3px; }
QProgressBar#homeProgress::chunk { background:#12B981; border-radius:3px; }
QFrame#scheduleBox { background:#F8FBFF; border:1px solid #D9E7F6; border-radius:8px; }
QLabel#scheduleName { color:#19376C; }
QLabel#summaryBlue { color:#087AF7; }
QLabel#summaryPurple { color:#7A3DF0; }
QLabel#summaryOrange { color:#E89400; }
QPushButton#quickBlue { background:#087AF7; color:#FFFFFF; border:1px solid #0B74E5; border-radius:10px; }
QPushButton#quickPurple { background:#7A3DF0; color:#FFFFFF; border:1px solid #6B35DA; border-radius:10px; }
QPushButton#quickOrange { background:#F4A000; color:#FFFFFF; border:1px solid #DF9200; border-radius:10px; }
QPushButton#quickGreen { background:#0AA875; color:#FFFFFF; border:1px solid #079466; border-radius:10px; }
"""


def _polish_shell(window: QWidget) -> None:
    """Ajusta proporções da casca principal sem alterar navegação ou lógica."""
    sidebar = getattr(window, "sidebar", None)
    if sidebar is not None:
        sidebar.setFixedWidth(236)
        layout = sidebar.layout()
        if layout is not None:
            layout.setContentsMargins(12, 11, 12, 9)
            layout.setSpacing(3)

    nav_buttons = getattr(window, "nav_buttons", {})
    if isinstance(nav_buttons, dict):
        for button in nav_buttons.values():
            button.setMinimumHeight(39)
            button.setMaximumHeight(42)

    status_card = getattr(window, "side_status_card", None)
    if status_card is not None:
        status_card.setMinimumHeight(136)
        status_card.setMaximumHeight(150)

    for child in window.findChildren(QWidget):
        if child.__class__.__name__ == "SidebarShipArt":
            child.setMinimumHeight(54)
            child.setMaximumHeight(62)

    header = getattr(window, "header_widget", None)
    if header is not None:
        header.setMinimumHeight(82)
        header.setMaximumHeight(90)

    footer = getattr(window, "footer_widget", None)
    if footer is not None:
        footer.setFixedHeight(34)

    content_layout = getattr(window, "content_layout", None)
    if content_layout is not None:
        if header is not None and header.isVisible():
            content_layout.setContentsMargins(14, 4, 14, 0)
            content_layout.setSpacing(8)
        else:
            content_layout.setContentsMargins(0, 0, 0, 0)
            content_layout.setSpacing(0)

    pages = getattr(window, "pages", {})
    if isinstance(pages, dict):
        for page in pages.values():
            root = getattr(page, "root", None)
            if root is not None:
                root.setSpacing(10)


def _polish_home(window: QWidget) -> None:
    home = window.findChild(QWidget, "homeDashboard")
    if home is None:
        return

    # Substitui o tema escuro nativo em vez de apenas anexar regras. Isso evita
    # que seletores do stylesheet antigo continuem vencendo em widgets filhos.
    home.setStyleSheet(HOME_LIGHT_OVERRIDE)

    for frame in home.findChildren(QFrame):
        name = frame.objectName()
        if name in {"metricCard", "dashboardCard", "miniCard"}:
            frame.setStyleSheet(
                "QFrame{background:#FFFFFF;border:1px solid #D7E6F7;border-radius:12px;}"
            )
        elif name == "statusPanel":
            frame.setStyleSheet(
                "QFrame{background:#ECFBF5;border:1px solid #A9E9D1;border-radius:9px;}"
            )
        elif name == "scheduleBox":
            frame.setStyleSheet(
                "QFrame{background:#F8FBFF;border:1px solid #D9E7F6;border-radius:8px;}"
            )
        else:
            style = frame.styleSheet().lower()
            if any(token in style for token in ("#04223c", "#031a2e", "#052d4d", "#052d42", "#06375c", "#05304e", "#031f39")):
                frame.setStyleSheet(
                    "QFrame{background:#FFFFFF;border:1px solid #D7E6F7;border-radius:10px;}"
                )


def _polish_pdf(page: QWidget) -> None:
    preview = getattr(page, "preview", None)
    if preview is not None:
        preview.setStyleSheet("border:1px dashed #BFD5EF;border-radius:10px;background:#FFFFFF;")
    thumbs = getattr(page, "thumbs", None)
    if thumbs is not None:
        thumbs.setStyleSheet(
            "QListWidget{background:#F8FBFF;border:1px solid #D5E4F3;border-radius:9px;padding:5px;}"
            "QListWidget::item{background:#FFFFFF;border:1px solid #DCE8F5;border-radius:8px;padding:5px;color:#17376D;}"
            "QListWidget::item:selected{background:#EAF4FF;border:2px solid #4A9DF0;color:#075FDB;}"
        )
    for button in page.findChildren(QPushButton):
        if button.text().strip().startswith(("▣  Arquivos", "PDF", "✂  Cortar", "▧  Redimensionar", "▤  Criar", "▣  Excluir", "▨  Capa", "↕  Ordenar")):
            button.setStyleSheet(
                "QPushButton{background:#FFFFFF;color:#16376E;border:1px solid #D5E4F3;border-left:3px solid #2C8BEF;"
                "border-radius:8px;padding:8px 10px;text-align:left;font-weight:700;}"
                "QPushButton:hover{background:#F2F8FF;border-color:#8AB9EC;}"
            )
    for frame in page.findChildren(QFrame):
        style = frame.styleSheet()
        if "background:#052844" in style or "background:#073252" in style:
            frame.setStyleSheet("QFrame{background:#FFFFFF;border:1px solid #D7E6F7;border-radius:9px;}")


def _polish_extractor(page: QWidget) -> None:
    for radio in getattr(page, "quality_buttons", []):
        radio.setStyleSheet(
            "QRadioButton{background:#FFFFFF;border:1px solid #D5E4F3;border-radius:8px;padding:8px 12px;color:#17376D;}"
            "QRadioButton:checked{background:#EAF4FF;border:1px solid #2D8FF0;color:#075FDB;font-weight:700;}"
        )
    download = getattr(page, "download_button", None)
    if download is not None:
        download.setStyleSheet(
            "QPushButton{background:#FFD326;color:#0B2860;border:1px solid #E9B900;border-radius:10px;"
            "font-size:17px;font-weight:900;min-height:50px;}"
            "QPushButton:hover{background:#FFDD4D;}"
            "QPushButton:disabled{background:#F1E7B2;color:#9A8B48;border-color:#E3D597;}"
        )
    for label in page.findChildren(QLabel):
        if label.text().startswith("MP4"):
            label.setStyleSheet(
                "color:#8B5A00;border:1px solid #F1CF76;background:#FFF7DE;"
                "border-radius:7px;padding:6px 10px;font-weight:700;"
            )


def _polish_demands(page: QWidget) -> None:
    for frame in page.findChildren(QFrame):
        if frame.objectName() == "statusCard":
            frame.setStyleSheet(
                "QFrame#statusCard{background:#ECFBF5;border:1px solid #A9E9D1;border-radius:12px;}"
            )
    for label in page.findChildren(QLabel):
        text = label.text().strip()
        if text == "▣":
            label.setStyleSheet(
                "color:#E7A800;background:#FFF7DE;border:1px solid #F0D487;"
                "border-radius:9px;font-size:24px;"
            )
        elif text.startswith("Status:"):
            label.setStyleSheet("color:#07865F;font-size:12px;font-weight:800;")


def _polish_settings(page: QWidget) -> None:
    for label in page.findChildren(QLabel):
        text = label.text().strip()
        style = label.styleSheet()
        if text in {"▣", "▤", "▶"} and ("background:#" in style or "border:1px" in style):
            if text == "▶":
                label.setStyleSheet(
                    "color:#7A3DF0;background:#F3EDFF;border:1px solid #DCCCF9;"
                    "border-radius:10px;font-size:22px;font-weight:800;"
                )
            elif text == "▣":
                label.setStyleSheet(
                    "color:#E7A800;background:#FFF7DE;border:1px solid #F0D487;"
                    "border-radius:10px;font-size:22px;font-weight:800;"
                )
            else:
                label.setStyleSheet(
                    "color:#087AF7;background:#EAF4FF;border:1px solid #C8DFF6;"
                    "border-radius:10px;font-size:22px;font-weight:800;"
                )
        if text in {"Automático ativo", "Proxy salvo", "Automação salva", "Configurações carregadas"}:
            label.setStyleSheet(
                "color:#07865F;background:#ECFBF5;border:1px solid #A9E9D1;"
                "border-radius:8px;padding:6px 10px;font-weight:700;"
            )
    for frame in page.findChildren(QFrame):
        style = frame.styleSheet()
        if "background:#0b5f85" in style:
            frame.setStyleSheet("background:#D9E7F6;border:0;")


def _polish_search_pages(page: QWidget) -> None:
    for label in page.findChildren(QLabel):
        style = label.styleSheet()
        if "background:#3a3215" in style:
            label.setStyleSheet(
                "color:#8A6300;background:#FFF8DE;border:1px solid #F0D889;"
                "border-radius:7px;padding:6px 9px;"
            )


def _polish_sources(page: QWidget) -> None:
    source_list = getattr(page, "list", None)
    if isinstance(source_list, QListWidget):
        source_list.setSpacing(2)
        source_list.setStyleSheet(
            "QListWidget{background:transparent;border:0;padding:2px;}"
            "QListWidget::item{background:#FFFFFF;border:1px solid #DCE8F5;border-radius:10px;margin:2px 0;padding:0;}"
            "QListWidget::item:selected{background:#F3F8FF;border:1px solid #AFCDED;}"
        )
    for label in page.findChildren(QLabel):
        text = label.text().strip()
        if text in {"Selecionada", "Incluída por Todos", "LIGADO"}:
            label.setStyleSheet(
                "color:#07865F;background:#ECFBF5;border:1px solid #A9E9D1;"
                "border-radius:8px;padding:5px 9px;font-weight:700;"
            )
        elif text in {"Disponível", "DESLIGADO", "N/A"}:
            label.setStyleSheet(
                "color:#5E769C;background:#F6F9FD;border:1px solid #D7E4F2;"
                "border-radius:8px;padding:5px 9px;font-weight:700;"
            )
        elif len(text) <= 3 and text.isupper() and text.isalpha():
            style = label.styleSheet()
            if "background:#087af7" in style:
                label.setStyleSheet(
                    "color:#087AF7;background:#EAF4FF;border:1px solid #C8DFF6;"
                    "border-radius:9px;font-weight:800;"
                )


def _polish_terms(page: QWidget) -> None:
    for label in page.findChildren(QLabel):
        text = label.text().strip()
        style = label.styleSheet()
        if text in {"▶", "▤"} and "background:#" in style:
            if text == "▶":
                label.setStyleSheet(
                    "color:#7A3DF0;background:#F3EDFF;border:1px solid #DCCCF9;"
                    "border-radius:10px;font-size:23px;"
                )
            else:
                label.setStyleSheet(
                    "color:#087AF7;background:#EAF4FF;border:1px solid #C8DFF6;"
                    "border-radius:10px;font-size:23px;"
                )
        if text.endswith("termo(s)"):
            label.setStyleSheet(
                "color:#075FDB;background:#EAF4FF;border:1px solid #C8DFF6;"
                "border-radius:8px;padding:8px 12px;font-weight:800;"
            )
    for lst in page.findChildren(QListWidget):
        lst.setStyleSheet(
            "QListWidget{background:#F8FBFF;border:1px solid #D7E6F7;border-radius:10px;padding:6px;color:#17376D;}"
            "QListWidget::item{background:#FFFFFF;border:1px solid #E0EAF5;border-radius:8px;padding:8px;margin:3px 0;}"
            "QListWidget::item:selected{background:#EAF4FF;border:1px solid #6DA9EA;color:#075FDB;}"
        )


def _polish_history(page: QWidget) -> None:
    for button in page.findChildren(QPushButton):
        if button.text().strip() in {"Notícias", "Vídeos"}:
            button.setMinimumHeight(36)
            button.setMaximumHeight(38)


def _polish_video_editor(page: QWidget) -> None:
    editor = getattr(page, "editor", None)
    if editor is None:
        return

    central = editor.centralWidget()
    if central is not None:
        central.setStyleSheet("background:#F7FAFE;color:#0B2860;")

    for frame in editor.findChildren(QFrame):
        if frame.objectName() == "panel":
            frame.setGraphicsEffect(None)
            frame.setStyleSheet(
                "QFrame#panel{background:#FFFFFF;border:1px solid #D7E6F7;border-radius:10px;}"
            )

    for label in editor.findChildren(QLabel):
        style = label.styleSheet().lower()
        if any(token in style for token in ("#0a1320", "#09121f", "#07111f", "#0d1828", "#18263a")):
            label.setStyleSheet(
                "color:#5F7398;background:#F8FBFF;border:1px solid #D7E6F7;"
                "border-radius:8px;padding:8px;"
            )

    media_list = getattr(editor, "media_list", None)
    if isinstance(media_list, QListWidget):
        media_list.setStyleSheet(
            "QListWidget{background:#FFFFFF;color:#17376D;border:1px solid #D7E6F7;border-radius:8px;padding:6px;}"
            "QListWidget::item{background:#FFFFFF;border:1px solid #E0EAF5;border-radius:7px;padding:8px;margin:2px 0;}"
            "QListWidget::item:selected{background:#EAF4FF;color:#075FDB;border:1px solid #6DA9EA;}"
        )

    video_widget = getattr(editor, "video_widget", None)
    if video_widget is not None:
        video_widget.setStyleSheet(
            "background:#05070A;border:1px solid #C7D8EB;border-radius:8px;"
        )


def apply_reference_layout(window: QWidget) -> None:
    """Aplica o acabamento visual de referência sem alterar lógica de negócio."""
    _polish_shell(window)
    _polish_home(window)
    pages = getattr(window, "pages", {})
    for page in pages.values() if isinstance(pages, dict) else []:
        name = page.__class__.__name__
        if name == "RefinedPdfEditorPage":
            _polish_pdf(page)
        elif name == "RefinedExtractorPage":
            _polish_extractor(page)
        elif name == "DemandsPage":
            _polish_demands(page)
        elif name == "SettingsPage":
            _polish_settings(page)
        elif name in {"NewsPage", "VideosPage"}:
            _polish_search_pages(page)
        elif name == "SourcesPage":
            _polish_sources(page)
        elif name == "TermsPage":
            _polish_terms(page)
        elif name == "HistoryPage":
            _polish_history(page)
        elif name == "VideoEditorPage":
            _polish_video_editor(page)
