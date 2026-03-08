import sys
from PyQt6.QtCore import QUrl, Qt, QSize
from PyQt6.QtWidgets import (QApplication, QMainWindow, QToolBar, QLineEdit, 
                             QVBoxLayout, QWidget, QTabWidget, QProgressBar, 
                             QPushButton, QHBoxLayout)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QFont

class ChromeButton(QPushButton):
    """Chrome風の円形ボタン"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(32, 32)
        self.setFont(QFont("Segoe UI Symbol", 12))

class ChromeTab(QWebEngineView):
    def __init__(self, parent=None):
        super().__init__(parent)

class ChromeBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Google Chrome Open Source Clone")
        
        # タブシステム
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.sync_url_and_title)

        # メインレイアウト
        self.setCentralWidget(self.tabs)
        
        # UIパーツの構築
        self.setup_nav_bar()
        
        # 初回起動
        self.add_new_tab(QUrl("https://www.google.com"), "Google")

    def setup_nav_bar(self):
        self.nav_bar = QToolBar()
        self.addToolBar(self.nav_bar)

        # 戻る・進む・更新
        self.back_btn = ChromeButton("‹")
        self.back_btn.clicked.connect(lambda: self.tabs.currentWidget().back())
        
        self.next_btn = ChromeButton("›")
        self.next_btn.clicked.connect(lambda: self.tabs.currentWidget().forward())
        
        self.reload_btn = ChromeButton("⟳")
        self.reload_btn.clicked.connect(lambda: self.tabs.currentWidget().reload())

        self.home_btn = ChromeButton("⌂")
        self.home_btn.clicked.connect(self.go_home)

        # アドレスバー
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # 新規タブ
        self.new_tab_btn = ChromeButton("+")
        self.new_tab_btn.clicked.connect(lambda: self.add_new_tab())

        # ウィジェットをバーに追加
        self.nav_bar.addWidget(self.back_btn)
        self.nav_bar.addWidget(self.next_btn)
        self.nav_bar.addWidget(self.reload_btn)
        self.nav_bar.addWidget(self.home_btn)
        self.nav_bar.addWidget(self.url_bar)
        self.nav_bar.addWidget(self.new_tab_btn)

        # プログレスバー（最上部に配置）
        self.progress = QProgressBar()
        self.statusBar().addPermanentWidget(self.progress, 1)
        self.statusBar().hide() # 普段は隠す

    def add_new_tab(self, qurl=None, label="New Tab"):
        if qurl is None:
            qurl = QUrl("https://www.google.com")
        
        browser = ChromeTab()
        browser.setUrl(qurl)
        
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # イベント連携
        browser.urlChanged.connect(lambda q, b=browser: self.update_url_text(q, b))
        browser.loadProgress.connect(self.progress.setValue)
        browser.titleChanged.connect(lambda t, b=browser: self.update_tab_title(t, b))
        
        # 読込開始・終了でプログレスバーを制御
        browser.loadStarted.connect(lambda: self.progress.show())
        browser.loadFinished.connect(lambda: self.progress.hide())

    def navigate_to_url(self):
        text = self.url_bar.text()
        if "." not in text or " " in text:
            url = QUrl(f"https://www.google.com/search?q={text}")
        else:
            url = QUrl(text) if text.startswith("http") else QUrl(f"https://{text}")
        self.tabs.currentWidget().setUrl(url)

    def go_home(self):
        self.tabs.currentWidget().setUrl(QUrl("https://www.google.com"))

    def update_url_text(self, q, browser):
        if browser == self.tabs.currentWidget():
            self.url_bar.setText(q.toString())

    def update_tab_title(self, title, browser):
        index = self.tabs.indexOf(browser)
        if index != -1:
            self.tabs.setTabText(index, title[:20])

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def sync_url_and_title(self, i):
        if i != -1:
            browser = self.tabs.widget(i)
            self.url_bar.setText(browser.url().toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # スタイル適用
    try:
        with open("style.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except:
        pass

    window = ChromeBrowser()
    window.show()
    sys.exit(app.exec())
