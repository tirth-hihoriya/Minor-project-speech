#!/usr/bin/env python

##################################################################################################################
#                                                   CREDITS                                                      #
#                                                                                                                #
#     https://towardsdatascience.com/transcribing-interview-data-from-video-to-text-with-python-5cdb6689eea1     #
##################################################################################################################

import wave, contextlib, math, time

import speech_recognition as sr
from moviepy.editor import AudioFileClip
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
import moviepy.editor as mp

class Ui_MainWindow:
    """Main window GUI."""

    def __init__(self):
        """Initialisation function."""
        self.mp4_file_name = ""
        self.output_file = ""
        self.audio_file = "speech.wav"

    def setupUi(self, MainWindow):
        # Define visual components and positions
        # Main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(653, 836)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 20, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.selected_video_label = QtWidgets.QLabel(self.centralwidget)
        self.selected_video_label.setGeometry(QtCore.QRect(230, 20, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.selected_video_label.setFont(font)
        self.selected_video_label.setFrameShape(QtWidgets.QFrame.Box)
        self.selected_video_label.setText("")
        self.selected_video_label.setObjectName("selected_video_label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(50, 90, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.transcribed_text = QtWidgets.QTextBrowser(self.centralwidget)
        self.transcribed_text.setGeometry(QtCore.QRect(230, 320, 381, 431))
        self.transcribed_text.setObjectName("transcribed_text")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(230, 280, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.transcribe_button = QtWidgets.QPushButton(self.centralwidget)
        self.transcribe_button.setEnabled(False)
        self.transcribe_button.setGeometry(QtCore.QRect(230, 150, 221, 81))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.transcribe_button.setFont(font)
        self.transcribe_button.setObjectName("transcribe_button")
        self.transcribe_button.clicked.connect(self.process_and_transcribe_audio)
        self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar.setGeometry(QtCore.QRect(230, 250, 381, 23))
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName("progress_bar")
        self.message_label = QtWidgets.QLabel(self.centralwidget)
        self.message_label.setGeometry(QtCore.QRect(0, 760, 651, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.message_label.setFont(font)
        self.message_label.setFrameShape(QtWidgets.QFrame.Box)
        self.message_label.setText("")
        self.message_label.setObjectName("message_label")
        self.output_file_name = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.output_file_name.setGeometry(QtCore.QRect(230, 90, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.output_file_name.setFont(font)
        self.output_file_name.setObjectName("output_file_name")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 653, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_mp4_video_recording = QtWidgets.QAction(MainWindow)
        self.actionOpen_mp4_video_recording.setObjectName("actionOpen_mp4_video_recording")
        self.actionOpen_mp4_video_recording.triggered.connect(self.open_audio_file)
        self.actionAbout_vid2text = QtWidgets.QAction(MainWindow)
        self.actionAbout_vid2text.setObjectName("actionAbout_vid2text")
        self.actionAbout_vid2text.triggered.connect(self.show_about)
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionNew.triggered.connect(self.new_project)
        self.menuFile.addAction(self.actionOpen_mp4_video_recording)
        self.menuFile.addAction(self.actionNew)
        self.menuAbout.addAction(self.actionAbout_vid2text)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """Translate UI method."""
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Selected video file:"))
        self.label_3.setText(_translate("MainWindow", "Output file name:"))
        self.label_5.setText(_translate("MainWindow", "Transcribed text:"))
        self.transcribe_button.setText(_translate("MainWindow", "Transcribe"))
        self.output_file_name.setPlaceholderText(_translate("MainWindow", "transcript.txt"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionOpen_mp4_video_recording.setText(_translate("MainWindow", "Open mp4 video recording"))
        self.actionAbout_vid2text.setText(_translate("MainWindow", "About this project"))
        self.actionNew.setText(_translate("MainWindow", "New"))

    def open_audio_file(self):
        """Open the audio (*.mp4) file."""
        file_name = QFileDialog.getOpenFileName()
        self.transcribe_button.setEnabled(True)
        self.mp4_file_name = file_name[0]
        self.message_label.setText("")
        self.selected_video_label.setText(file_name[0])

    def convert_mp4_to_wav(self):
        """Convert the mp4 video file into an audio file."""
        self.message_label.setText("Converting mp4 to audio (*.wav)...")
        self.convert_thread = convertVideoToAudioThread(self.mp4_file_name, self.audio_file)
        self.convert_thread.finished.connect(self.finished_converting)
        self.convert_thread.start()

    def get_audio_duration(self, audio_file):
        """Determine the length of the audio file."""
        with contextlib.closing(wave.open(audio_file,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration

    def transcribe_audio(self, audio_file):
        """Transcribe the audio file."""
        total_duration = self.get_audio_duration(audio_file) / 10
        total_duration = math.ceil(total_duration)
        self.td = total_duration
        if len(self.output_file_name.toPlainText()) > 0:
            self.output_file = self.output_file_name.toPlainText()
        else:
            self.output_file = "my_speech_file.txt"
        self.thread = transcriptionThread(total_duration, audio_file, self.output_file)
        self.thread.finished.connect(self.finished_transcribing)
        self.thread.change_value.connect(self.set_progress_value)
        self.thread.start()

    def finished_converting(self):
        """Reset message text when conversion is finished."""
        self.message_label.setText("Transcribing file...")
        self.transcribe_audio(self.audio_file)

    def finished_transcribing(self):
        """This run when transcription finished to tidy up UI."""
        self.progress_bar.setValue(100)
        self.transcribe_button.setEnabled(True)
        self.message_label.setText("")
        self.update_text_output()

    def set_progress_value(self, val):
        """Update progress bar value."""
        increment = int(math.floor(100*(float(val)/self.td)))
        self.progress_bar.setValue(increment)

    def process_and_transcribe_audio(self):
        """Process the audio into a textual transcription."""
        self.transcribe_button.setEnabled(False)
        self.message_label.setText("Converting mp4 to audio (*.wav)...")
        self.convert_mp4_to_wav()

    def update_text_output(self):
        """Update the text box with the transcribed file."""
        f = open(self.output_file, "r")
        self.transcribed_text.setText(f.read())
        f.close()

    def new_project(self):
        """Clear existing fields of data."""
        self.message_label.setText("")
        self.transcribed_text.setText("")
        self.selected_video_label.setText("")
        self.output_file_name.document().setPlainText("")
        self.progress_bar.setValue(0)

    def show_about(self):
        """Show about message box."""
        msg = QMessageBox()
        msg.setWindowTitle("About this Project")
        msg.setText("The project has been created by Tirth Patel and Tirth Hihoriya\n"
                    "Credits to Dr. Alan Davies for providing the code for the GUI")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

class convertVideoToAudioThread(QThread):
    """Thread to convert mp4 video file to wav file."""

    def __init__(self, mp4_file_name, audio_file):
        """Initialization function."""
        QThread.__init__(self)
        self.mp4_file_name = mp4_file_name
        self.audio_file = audio_file

    def __del__(self):
        """Destructor."""
        self.wait()

    def run(self):
        """Run video conversion task."""
        # audio_clip = AudioFileClip(self.mp4_file_name)
        # audio_clip.write_audiofile(self.audio_file)
        my_clip = mp.VideoFileClip(self.mp4_file_name)
        my_clip.audio.write_audiofile(self.audio_file)

class transcriptionThread(QThread):
    """Thread to transcribe file from audio to text."""

    change_value = pyqtSignal(int)

    def __init__(self, total_duration, audio_file, output_file):
        """Initialization function."""
        QThread.__init__(self)
        self.total_duration = total_duration
        self.audio_file = audio_file
        self.output_file = output_file

    def __del__(self):
        """Destructor."""
        self.wait()

    def run(self):
        """Run transcription, audio to text."""
        # r = sr.Recognizer()
        # for i in range(0, self.total_duration):
        #     try:
        #         with sr.AudioFile(self.audio_file) as source:
        #             audio = r.record(source, offset=i*10, duration=10)
        #             f = open(self.output_file, "a")
        #             f.write(r.recognize_google(audio))
        #             f.write(" ")
        #         self.change_value.emit(i)
        #     except:
        #         print("Unknown word detected...")
        #         continue
        #     f.close()
        import os
        import shutil

        from pydub import AudioSegment
        from pydub.silence import split_on_silence

        def match_target_amplitude(sound, target_dBFS):
            change_in_dBFS = target_dBFS - sound.dBFS
            return sound.apply_gain(change_in_dBFS)

        if os.path.exists('result'):
            shutil.rmtree('result')
        os.mkdir('result')

        sound = AudioSegment.from_wav(self.audio_file)
        normalized_sound = match_target_amplitude(sound, -20.0)
        chunks = split_on_silence(normalized_sound, min_silence_len=1000, silence_thresh=-30)
        for i, chunk in enumerate(chunks):
            fullPath = "result/speech_{number}_{length}.wav".format(number=i+1, length=len(chunk))
            chunk.export(fullPath, format="wav")

        import speech_recognition as sr

        offset = 0
        times = []

        audio_files = os.listdir("result")
        audio_files = sorted([file_ for file_ in audio_files if file_.endswith(".wav")])
        r = sr.Recognizer()
        of = open(self.output_file, "w")
        for i, audioname in enumerate(audio_files):
            audio = sr.AudioFile(os.path.join("result", audioname))
            try:
                with audio as source:
                    audio_file = r.record(source)
                result = r.recognize_google(audio_file)
                times.append(offset)
                # exporting the result
                of.write(f"Time: {str(times[-1]//60000).zfill(2)}:{str((times[-1]//1000) - (times[-1]//60000)*60).zfill(2)} => ")
                of.write("Recognized Speech: ")
                of.write(result)
                of.write("\n")
            except sr.UnknownValueError:
                pass
            finally:
                offset += len(chunks[i])
                self.change_value.emit(i)
        of.close()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
