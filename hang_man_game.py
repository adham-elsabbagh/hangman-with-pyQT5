from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
import qdarkstyle
import random
class HangmanGame(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.installEventFilter(self)
        self.view_ref = loadUi("hangmangame.ui" , self)
        self.__choosen_words = ['3dhubs', 'marvin', 'print', 'filament', 'order', 'layer']
        self.__lbl_list = []
        self.init_game()
        self.show()
#adham

    def init_game(self):
        # available choices
        self.__available_choises_list = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        self.__available_choises_list.extend([str(i) for i in range(0, 10)])
        self.available_choices.setText("  ".join(self.__available_choises_list))
        # life counter
        self.life_counter = 5
        # self.guessed_char_counter = 0
        self.lifeCounter.display(self.life_counter)

        # pic random word
        self.__choosen_word = random.choice(self.__choosen_words)

        # remove old lbls
        for lbl in self.__lbl_list:
            self.letters_layout.removeWidget(lbl)
            lbl.deleteLater()
            lbl = (None)

        # create new labels
        self.__lbl_list = [QLabel(self) for i in range(len(self.__choosen_word))]
        # init labels
        self.answer = list()
        for lbl in self.__lbl_list:
            lbl.setText("_")
            lbl.setAlignment(Qt.AlignHCenter)
            self.answer.append("_")
            self.letters_layout.addWidget(lbl)



    def eventFilter(self, source, event):
        #define the keypad
        if event.type() == QEvent.KeyPress :
            try:
                guessed_letter = chr(event.key()).lower()
                if guessed_letter.upper() in self.__available_choises_list:
                    is_winner = -1
                    if guessed_letter in self.__choosen_word:
                        letter_poses = []
                        for index , char in enumerate(self.__choosen_word):
                            if char == guessed_letter:
                                letter_poses.append(index)
                        #remove the upper char
                        self.__available_choises_list.remove(guessed_letter.upper())
                        self.available_choices.setText("  ".join(self.__available_choises_list))
                        #update '_' with correct chars
                        for pos in letter_poses:
                            # self.guessed_char_counter += 1
                            self.__lbl_list[pos].setText(guessed_letter)
                            self.answer[pos] = guessed_letter
                            if "_" not in self.answer:
                                is_winner = 1
                    else:

                        if guessed_letter.upper() in self.__available_choises_list:
                            self.__available_choises_list.remove(guessed_letter.upper())
                            self.available_choices.setText("  ".join(self.__available_choises_list))
                            self.life_counter -= 1
                            if self.life_counter == 0:
                                is_winner = 0
                            self.lifeCounter.display(self.life_counter)


                    if(is_winner != -1):
                        header = "Congratulation" if is_winner == 1 else "hard luck"
                        custom ="score({}/5)\n".format(self.life_counter) if is_winner == 1 else ""
                        msg = "{}do you want to play again".format(custom)
                        reply = QMessageBox.question(self, header ,
                                                           msg, QMessageBox.Yes, QMessageBox.No)

                        if reply == QMessageBox.Yes:
                            self.init_game()
                        else:
                            self.close()

            except Exception as e:
                print("not valid letter")

        return super(HangmanGame, self).eventFilter(source, event)



app =QApplication([])
game = HangmanGame()
app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
app.exec_()

