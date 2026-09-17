from __future__ import annotations

# Contrato V5 público preservado: testes e módulos antigos dependem destes valores.
V5_NAVY = "#052D57"
V5_NAVY_DARK = "#031F3E"
V5_INK = "#0A1F4B"
V5_MUTED = "#58739F"
V5_BG = "#F3F8FE"
V5_BORDER = "#D5E4F3"
V5_BLUE = "#087AF7"
V5_PURPLE = "#743AF3"
V5_ORANGE = "#FF820A"
V5_GREEN = "#08A86F"
V5_RED = "#D92F43"
V5_GOLD = "#F2B715"
V5_SOFT_BLUE = "#EAF4FF"

# Tema claro unificado inspirado no layout de referência do Monitor.
APP_STYLESHEET = """
QMainWindow, QWidget#root { background:#F5F9FE; color:#08245A; }
QWidget { font-family:'Segoe UI'; font-size:11px; color:#08245A; }
QWidget#mainContent { background:#F7FAFE; }

QFrame#sidebar {
    background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #073B78,stop:0.52 #052F66,stop:1 #04285A);
    border:0;
    border-radius:0;
}
QLabel#brandTitle { color:#FFFFFF; font-size:17px; font-weight:800; }
QLabel#brandSub { color:#DCEBFF; font-size:10px; }
QLabel#anchorMark { color:#FFD34D; font-family:'Segoe UI Symbol'; font-size:42px; font-weight:700; }
QPushButton#navButton {
    color:#F7FBFF; background:transparent; border:0; border-radius:10px;
    padding:10px 13px; text-align:left; font-size:13px; font-weight:600;
}
QPushButton#navButton:hover { background:rgba(255,255,255,0.09); }
QPushButton#navButton:checked {
    background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #0D79ED,stop:1 #078EFF);
    border:1px solid #3FB2FF; color:#FFFFFF; font-weight:800;
}
QLabel#newsBadge { color:#6D4B00; background:#FFE28A; border-radius:10px; padding:2px 7px; font-size:9px; font-weight:800; }
QFrame#sideStatusCard { background:rgba(255,255,255,0.06); border:1px solid rgba(153,205,255,0.30); border-radius:11px; }
QLabel#sideStatusTitle { color:#FFFFFF; font-size:10px; font-weight:800; }
QLabel#sideStatusText, QLabel#sideStatusGood { color:#D5E8FF; font-size:9px; }
QLabel#sideMotto { color:#9BCBFF; font-size:8px; font-weight:700; letter-spacing:1px; }

QWidget#pageRoot { background:transparent; }
QFrame#pageHeader {
    background:#FFFFFF;
    border:1px solid #D9E8F7;
    border-radius:13px;
}
QLabel#pageKicker { color:#147BF3; font-size:10px; font-weight:800; letter-spacing:1px; }
QLabel#pageTitle { color:#08245A; font-size:27px; font-weight:800; }
QLabel#pageSubtitle { color:#5F77A1; font-size:12px; }
QLabel#pageIcon { color:#187EF5; font-size:34px; font-weight:700; }
QLabel#muted { color:#6E84A9; }
QLabel#sectionTitle { color:#08245A; font-size:18px; font-weight:800; }
QLabel#cardTitle { color:#08245A; font-size:15px; font-weight:800; }
QLabel#smallTitle { color:#08245A; font-size:12px; font-weight:700; }
QLabel#smallText { color:#6F84A6; font-size:10px; }
QLabel#blueText { color:#0B78EF; font-weight:800; }
QLabel#greenText { color:#079C69; font-weight:800; }
QLabel#goldText { color:#C98A00; font-weight:800; }
QLabel#purpleText { color:#7B3FF2; font-weight:800; }
QLabel#redText { color:#E13650; font-weight:800; }

QFrame#card, QFrame#techCard, QFrame#resultCard, QFrame#filterCard, QFrame#settingsBlock {
    background:#FFFFFF;
    border:1px solid #D9E8F7;
    border-radius:13px;
}
QFrame#resultCard:hover, QFrame#techCard:hover { border-color:#84BEFF; background:#FBFDFF; }
QFrame#statusCard { background:#ECFBF5; border:1px solid #A9E8D0; border-radius:12px; }
QFrame#warningCard { background:#FFF8E4; border:1px solid #F2D179; border-radius:10px; }
QFrame#dangerCard { background:#FFF0F3; border:1px solid #F1B8C3; border-radius:10px; }
QFrame#emptyPanel { background:#FBFDFF; border:1px dashed #BDD8F5; border-radius:12px; }
QFrame#footerFrame { background:#FFFFFF; border-top:1px solid #E1ECF7; }
QFrame#pillGreen { background:#EFFBF6; border:1px solid #BDEBD8; border-radius:10px; }
QFrame#pillGold { background:#FFF9E7; border:1px solid #F1DA97; border-radius:10px; }
QFrame#pillBlue { background:#F3F8FF; border:1px solid #D0E3F8; border-radius:10px; }

QLineEdit, QComboBox, QSpinBox, QDateEdit, QTimeEdit {
    background:#FFFFFF; color:#09265E; border:1px solid #CFE0F2; border-radius:9px;
    padding:8px 10px; min-height:28px; selection-background-color:#0A7CF3;
}
QLineEdit:hover, QComboBox:hover, QSpinBox:hover, QDateEdit:hover, QTimeEdit:hover { border-color:#9CC8F7; }
QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDateEdit:focus, QTimeEdit:focus { border:1px solid #2D8DF5; }
QComboBox::drop-down { border:0; width:22px; }

QPushButton {
    background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #1485F7,stop:1 #0875EC);
    color:#FFFFFF; border:1px solid #0B74E5; border-radius:9px; padding:8px 14px;
    font-weight:700; min-height:28px;
}
QPushButton:hover { background:#188AF9; border-color:#3598FA; }
QPushButton:pressed { background:#0668D5; }
QPushButton:disabled { background:#EEF3F9; color:#9AABC2; border-color:#DDE7F2; }
QPushButton[secondary='true'] { background:#FFFFFF; color:#0A3C86; border:1px solid #C9DDF2; }
QPushButton[secondary='true']:hover { background:#F4F9FF; border-color:#8CBFF4; }
QPushButton[danger='true'] { background:#FFF2F4; color:#E02D49; border:1px solid #F0A9B6; }
QPushButton[purple='true'] { background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #7B32F4,stop:1 #286AF0); color:#FFFFFF; border:1px solid #7441EC; }
QPushButton[orange='true'] { background:#FFF2D8; color:#985700; border:1px solid #F2C465; }
QPushButton[green='true'] { background:#EAF9F2; color:#087B57; border:1px solid #A8DFC9; }
QPushButton[gold='true'] { background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #FFD237,stop:1 #FFC51F); color:#08245A; border:1px solid #E8B51A; }
QPushButton[ghost='true'] { background:#FFFFFF; color:#0A70E5; border:1px solid #C8DDF3; }
QPushButton:checked { background:#EAF4FF; color:#0A6FE6; border-color:#2086F3; }

QCheckBox { color:#183A70; spacing:8px; }
QCheckBox::indicator { width:18px; height:18px; border:1px solid #91B6DE; border-radius:4px; background:#FFFFFF; }
QCheckBox::indicator:checked { background:#147EF4; border-color:#147EF4; }
QRadioButton { color:#183A70; spacing:9px; min-height:26px; }
QRadioButton::indicator { width:18px; height:18px; border-radius:9px; border:2px solid #6F9DCD; background:#FFFFFF; }
QRadioButton::indicator:checked { background:#1888F8; border:4px solid #DCEEFF; }

QProgressBar { border:1px solid #D4E3F2; border-radius:4px; background:#EEF4FA; text-align:center; min-height:8px; max-height:8px; color:#526C93; }
QProgressBar::chunk { background:#0BB77B; border-radius:4px; }
QListWidget, QTableWidget { background:transparent; color:#143667; border:0; gridline-color:#DFEAF5; alternate-background-color:#F8FBFE; outline:0; }
QListWidget::item { background:#FFFFFF; border:1px solid #DCE8F4; border-radius:9px; padding:8px; margin:3px 0; }
QListWidget::item:selected { background:#EAF4FF; color:#0B63CB; border-color:#84BCF7; }
QHeaderView::section { background:#F4F8FC; color:#536D93; padding:7px; border:0; border-bottom:1px solid #DDE8F3; font-weight:700; }
QScrollArea { border:0; background:transparent; }
QScrollArea QWidget#qt_scrollarea_viewport { background:transparent; }
QScrollBar:vertical { background:transparent; width:9px; margin:0; }
QScrollBar::handle:vertical { background:#C1D5E9; min-height:32px; border-radius:4px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height:0; }
QTabWidget::pane { border:0; background:transparent; }
QTabBar::tab { background:#FFFFFF; color:#183A70; border:1px solid #D3E3F2; padding:9px 18px; margin-right:7px; border-radius:8px; font-weight:700; }
QTabBar::tab:selected { background:#EAF4FF; color:#086FE6; border-color:#2D8DF5; }
QToolTip { background:#FFFFFF; color:#08245A; border:1px solid #C6DDF2; }
"""
