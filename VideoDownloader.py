from kivy.config import Config
Config.set('graphics', 'resizable', False)
from pathlib import Path
from kivymd.app import MDApp
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
from kivy.uix.image import Image
from pytube import YouTube
import os
import threading

Window.size = [400, 600]

class VideoDownloader(MDApp):

    def help(self):
        if self.state == 0:
            self.state = 1
            self.label.text = "Enter the url and press 'Download'"
        else:
            self.state = 0
            self.label.text = ""

    def mutitask_downld(self, obj):
        song = threading.Thread(target=self.download_song)
        song.start()

    def download_song(self):
        if self.input.text == "":
            self.toolbar.title = "Enter the url"
        else:
            url = str(self.input.text)
            yt = YouTube(url)
            try:
                self.toolbar.title = "Download started"
                self.label.text = "Downloading " + "'" +  yt.title + "'"
                video = yt.streams.filter(res="720p").first()
                destination = str(Path.home()/"Downloads")
                out_file = video.download(output_path=destination)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp4'
                os.rename(out_file, new_file)
                self.label.text="Downloaded and saved successfully in \n" + destination
                self.toolbar.title = "Video Downloader"
            except Exception:
                self.label.text="Error Occured!"

    def build(self):
        sc = MDScreen()
        self.state = 0
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepOrange"
        self.toolbar = MDToolbar(title="Video Downloader")
        self.toolbar.pos_hint = {"top": 1}
        self.toolbar.right_action_items = [
            ["help", lambda x: self.help()]]
        sc.add_widget(self.toolbar)
        sc.add_widget(Image(
                source="video.png",
                pos_hint = {"center_x": 0.5, "center_y": 0.6}
        ))
        self.input = MDTextField(
            hint_text="Enter the youtube url",
            size_hint=(0.8, 1),
            pos_hint={"center_x": 0.5, "center_y": 0.35}
            )
        sc.add_widget(self.input)
        btn = MDFillRoundFlatButton(
            text="Download",
            pos_hint={"center_x": 0.5, "center_y": 0.25},
            on_release=self.mutitask_downld
            )
        sc.add_widget(btn)
        self.label = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color="orange",
            pos_hint={"center_x": 0.5, "center_y": 0.15}
            )
        sc.add_widget(self.label)
        return sc
        
if __name__ == '__main__':
    VideoDownloader().run()
