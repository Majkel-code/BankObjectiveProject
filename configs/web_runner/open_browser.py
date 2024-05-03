import webbrowser
import platform

class WebRunner:
    def __init__(self, browser) -> None:           
        self.user_OS = platform.system()
        self._path_windows = f'C:/Program Files (x86)/Google/{browser}/Application/.exe %s'
        self._path_linux = f'/usr/bin/google-{browser} %s'
        self._path_mac = f'open -a /Applications/Google\ {browser}.app %s'
        self._path = ''
        self.url = 'http://127.0.0.1:5500/Web/html/main.html'
        print(self.user_OS)

    def open(self):
        if self.user_OS == 'Windows':
            self._path = self._path_windows
        elif self.user_OS == 'Linux':
            self._path = self._path_linux
        elif self.user_OS == 'Darwin':
            self._path = self._path_mac
        elif self.user_OS == 'Java':
            self._path = self._path_mac
        else:
            webbrowser.open_new_tab(self.url)
        webbrowser.get(self._path).open_new_tab(self.url)