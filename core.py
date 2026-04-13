import sys
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLineEdit,
    QPushButton, QTabWidget, QLabel, QGridLayout
)
from PyQt6.QtWebEngineWidgets import QWebEngineView


class HomePage(QWidget):
    def __init__(self, browser):
        super().__init__()
        self.browser = browser

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(25)

        # --- TITLE ---
        title = QLabel("🌧️ RainExplorer Core")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 42px; color: #8ab4f8; font-weight: bold;")
        layout.addWidget(title)

        subtitle = QLabel("Search the web in the shared core.")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 16px; color: #e8eaed;")
        layout.addWidget(subtitle)

        # --- SEARCH BAR ---
        search_layout = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Enter URL...")
        self.search.setMinimumHeight(40)
        self.search.returnPressed.connect(self.go)
        self.search.setStyleSheet("""
            QLineEdit {
                border-radius: 20px;
                padding: 0 15px;
                background-color: #202124;
                color: white;
                border: 1px solid #3c4043;
            }
        """)
        search_layout.addWidget(self.search)

        btn = QPushButton("Go")
        btn.clicked.connect(self.go)
        btn.setStyleSheet("background:#8ab4f8; border-radius:15px; padding:8px;")
        search_layout.addWidget(btn)

        layout.addLayout(search_layout)

        description = QLabel("This is the open source core of RainExplorer. It provides basic browsing features and a simple interface. It was stripped of all tracking and privacy features to be as lightweight and fast as possible. You can use it as a standalone browser or as the core for your own RainExplorer-based browser.")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)
        description.setStyleSheet("font-size: 14px; color: #e8eaed;")
        layout.addWidget(description)

        # --- QUICK LINKS ---
        grid = QGridLayout()

        links = [
            ("Google", "https://google.com"),
            ("YouTube", "https://youtube.com"),
            ("GitHub", "https://github.com"),
            ("Wikipedia", "https://wikipedia.org"),
            ("Reddit", "https://reddit.com"),
            ("StackOverflow", "https://stackoverflow.com"),
        ]

        row, col = 0, 0
        for name, url in links:
            b = QPushButton(name)
            b.setMinimumSize(140, 60)
            b.setStyleSheet("""
                QPushButton {
                    background-color: #303134;
                    color: white;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #3c4043;
                }
            """)
            b.clicked.connect(lambda _, u=url: self.browser.open_url(u))
            grid.addWidget(b, row, col)

            col += 1
            if col > 2:
                col = 0
                row += 1


        layout.addLayout(grid)

    def go(self):
        text = self.search.text().strip()
        if text:
            if not text.startswith("http"):
                text = "http://" + text
            self.browser.open_url(text)


class SimpleBrowser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RainExplorer Core")
        self.setGeometry(100, 100, 1200, 800)

        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)

        # --- NAV BAR ---
        nav = QHBoxLayout()

        self.back_btn = QPushButton("←")
        self.back_btn.clicked.connect(self.go_back)
        nav.addWidget(self.back_btn)

        self.forward_btn = QPushButton("→")
        self.forward_btn.clicked.connect(self.go_forward)
        nav.addWidget(self.forward_btn)

        self.reload_btn = QPushButton("↻")
        self.reload_btn.clicked.connect(self.reload_page)
        nav.addWidget(self.reload_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.load_url)
        nav.addWidget(self.url_bar)

        layout.addLayout(nav)

        # --- TABS ---
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.update_url)

        layout.addWidget(self.tabs)

        self.add_home_tab()

    # --- TABS ---
    def add_home_tab(self):
        home = HomePage(self)
        index = self.tabs.addTab(home, "Home")
        self.tabs.setCurrentIndex(index)

    def add_browser_tab(self, url):
        browser = QWebEngineView()
        browser.setUrl(QUrl(url))
        browser.urlChanged.connect(self.update_url)

        index = self.tabs.addTab(browser, "Loading...")
        self.tabs.setCurrentIndex(index)

    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def current(self):
        return self.tabs.currentWidget()

    # --- NAVIGATION ---
    def open_url(self, url):
        self.add_browser_tab(url)

    def load_url(self):
        url = self.url_bar.text().strip()
        if not url.startswith("http"):
            url = "http://" + url
        self.open_url(url)

    def update_url(self, *args):
        widget = self.current()
        if isinstance(widget, QWebEngineView):
            self.url_bar.setText(widget.url().toString())
        else:
            self.url_bar.clear()

    def go_back(self):
        if isinstance(self.current(), QWebEngineView):
            self.current().back()

    def go_forward(self):
        if isinstance(self.current(), QWebEngineView):
            self.current().forward()

    def reload_page(self):
        if isinstance(self.current(), QWebEngineView):
            self.current().reload()


def main():
    app = QApplication(sys.argv)
    window = SimpleBrowser()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()