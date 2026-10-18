#!/usr/bin/env python3
"""
Minnesota Class D Instruction Permit - Knowledge Test Practice

Adaptive drill system:
  - All 1000 questions per run from a bank based on the MN Driver's Manual
  - Max 15 wrong answers - the 16th wrong answer auto-restarts the test instantly
  - Every attempt is shuffled, BUT questions you got wrong before come FIRST,
    then questions you have never answered, then ones you answered correctly
  - Wrong answers persist between sessions so the app keeps drilling weak spots

100% Free - Works Offline
"""

import sys
import csv
import random
import sqlite3
import os
from datetime import datetime

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QRadioButton, QButtonGroup, QProgressBar,
    QMessageBox, QTabWidget, QTextEdit, QListWidget, QListWidgetItem,
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from question_bank import build_bank

# ---------------- Config ----------------
QUESTION_BANK = build_bank()
TOTAL_QUESTIONS = len(QUESTION_BANK)   # all 1000 questions per run
MAX_WRONG = 15  # 16th wrong answer = instant auto-restart
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "minnesota_test_results.db")


class MinnesotaPermitTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Minnesota Permit Knowledge Test Practice - Adaptive")
        self.setGeometry(80, 80, 980, 780)

        self.init_database()

        # Test state
        self.current_question_index = 0
        self.user_answers = []
        self.scored = []            # which slots have been scored
        self.wrong_count = 0        # live wrong count this attempt
        self.wrong_questions = []   # details of misses this attempt
        self.test_active = False
        self.elapsed_seconds = 0
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)

        self.setStyleSheet("""
            QMainWindow { background-color: #2b2b2b; }
            QLabel { font-size: 14px; color: #e0e0e0; }
            QPushButton {
                background-color: #0078d7; color: white; font-size: 14px;
                padding: 10px 20px; border: none; border-radius: 4px; font-weight: bold;
            }
            QPushButton:hover { background-color: #106ebe; }
            QPushButton:disabled { background-color: #555; color: #888; }
            QRadioButton { font-size: 15px; color: #e0e0e0; padding: 8px; spacing: 10px; }
            QRadioButton:hover { background-color: #3c3c3c; }
            QListWidget { background-color: #1e1e1e; color: #e0e0e0; border: 1px solid #444; font-size: 13px; }
            QTextEdit { background-color: #1e1e1e; color: #e0e0e0; border: 1px solid #444; }
            QProgressBar { border: 1px solid #444; border-radius: 4px; background: #1e1e1e;
                text-align: center; font-weight: bold; color: #e0e0e0; height: 22px; }
            QProgressBar::chunk { background-color: #0078d7; }
            QTabWidget::pane { border: 1px solid #444; }
            QTabBar::tab { background: #1e1e1e; color: #e0e0e0; padding: 10px 20px; }
            QTabBar::tab:selected { background: #0078d7; color: white; }
        """)

        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_widget.setLayout(self.main_layout)

        title = QLabel("Minnesota Class D Permit - Adaptive Practice Test")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #0078d7; margin-bottom: 10px;")
        self.main_layout.addWidget(title)

        self.tabs = QTabWidget()
        self.main_layout.addWidget(self.tabs)

        self.test_tab = QWidget()
        self.setup_test_tab()
        self.tabs.addTab(self.test_tab, "Take Test")

        self.wrong_tab = QWidget()
        self.setup_wrong_tab()
        self.tabs.addTab(self.wrong_tab, "Wrong Answers - Study These")

        self.info_tab = QWidget()
        self.setup_info_tab()
        self.tabs.addTab(self.info_tab, "Info")

        self.status_bar = QLabel("Ready - Click 'Start Test' when you are ready")
        self.status_bar.setStyleSheet(
            "background-color: #1e1e1e; padding: 10px; border: 1px solid #444; "
            "font-weight: bold; font-size: 14px;")
        self.main_layout.addWidget(self.status_bar)

        self.load_wrong_history()

    # ==================== UI SETUP ====================
    def setup_test_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        self.test_tab.setLayout(layout)

        top_row = QHBoxLayout()
        self.timer_label = QLabel("Time: 0:00")
        self.timer_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        top_row.addWidget(self.timer_label)

        self.wrong_label = QLabel(f"Wrong: 0/{MAX_WRONG}")
        self.wrong_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.wrong_label.setStyleSheet("color: #e0e0e0; padding-left: 30px;")
        top_row.addWidget(self.wrong_label)
        top_row.addStretch()
        layout.addLayout(top_row)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, TOTAL_QUESTIONS)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("Question %v of %m")
        layout.addWidget(self.progress_bar)

        self.question_label = QLabel(
            "Click 'Start Test' to begin.\n\n"
            f"Rules: answer all {TOTAL_QUESTIONS} questions. "
            f"If you get {MAX_WRONG + 1} wrong, the test RESTARTS automatically "
            "with a new shuffled order - your missed questions come back first.")
        self.question_label.setWordWrap(True)
        self.question_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.question_label.setStyleSheet(
            "margin: 15px 0; padding: 20px; background: #1e1e1e; "
            "border: 1px solid #444; border-radius: 6px;")
        self.question_label.setMinimumHeight(120)
        layout.addWidget(self.question_label)

        self.answer_group = QButtonGroup()
        self.answer_radio_buttons = []
        for i in range(4):
            rb = QRadioButton("")
            rb.setVisible(False)
            rb.toggled.connect(lambda checked, idx=i: self.on_answer_selected(idx) if checked else None)
            self.answer_group.addButton(rb, i)
            self.answer_radio_buttons.append(rb)
            layout.addWidget(rb)

        layout.addStretch()

        nav_layout = QHBoxLayout()
        self.prev_button = QPushButton("< Previous")
        self.prev_button.setEnabled(False)
        self.prev_button.clicked.connect(self.previous_question)
        nav_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("Next >")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.next_question)
        nav_layout.addWidget(self.next_button)

        nav_layout.addStretch()

        self.submit_button = QPushButton("Submit Test")
        self.submit_button.setStyleSheet("background-color: #c0392b;")
        self.submit_button.setEnabled(False)
        self.submit_button.clicked.connect(self.confirm_submit)
        nav_layout.addWidget(self.submit_button)

        self.start_button = QPushButton("Start Test")
        self.start_button.setStyleSheet(
            "background-color: #28a745; font-size: 16px; padding: 12px 30px;")
        self.start_button.clicked.connect(self.start_test)
        nav_layout.addWidget(self.start_button)

        layout.addLayout(nav_layout)

    def setup_wrong_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        self.wrong_tab.setLayout(layout)

        header = QLabel("Questions you got wrong - study these to pass:")
        header.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        layout.addWidget(header)

        self.wrong_list = QListWidget()
        self.wrong_list.setWordWrap(True)
        layout.addWidget(self.wrong_list)

        btn_row = QHBoxLayout()
        export_button = QPushButton("Export to CSV")
        export_button.clicked.connect(self.export_wrong_questions)
        btn_row.addWidget(export_button)

        clear_button = QPushButton("Clear History")
        clear_button.setStyleSheet("background-color: #c0392b;")
        clear_button.clicked.connect(self.clear_history)
        btn_row.addWidget(clear_button)

        btn_row.addStretch()
        layout.addLayout(btn_row)

    def setup_info_tab(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        self.info_tab.setLayout(layout)

        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setHtml(f"""
        <h2 style="color:#0078d7;">How This Adaptive Practice Test Works</h2>
        <ul>
            <li><b>{len(QUESTION_BANK)}-question bank</b> built from the Minnesota Driver's Manual</li>
            <li><b>Every run covers the entire bank</b> - missed questions are
                shuffled to the front, unanswered next, correct ones last</li>
            <li><b>Max {MAX_WRONG} wrong answers</b> - the {MAX_WRONG+1}th wrong answer
                <b>automatically restarts the whole test instantly</b></li>
            <li><b>Shuffled every attempt</b> - but questions you missed come back FIRST,
                then questions you have never seen, then ones you got right</li>
            <li><b>Your misses are remembered</b> between sessions - the test keeps
                drilling your weak spots until you master them</li>
            <li><b>All 1,000 questions per run</b> - the full bank, ordered so
                your weakest questions hit first</li>
        </ul>

        <h3 style="color:#0078d7;">How to Use</h3>
        <ol>
            <li>Click <b>Start Test</b></li>
            <li>Answer each question - Next/Previous to move around</li>
            <li>Watch the <b>Wrong: X/{MAX_WRONG}</b> counter - hit {MAX_WRONG+1} and the
                test restarts automatically with a fresh shuffle</li>
            <li>Finish within {MAX_WRONG} wrong and you pass; then check the
                <b>Wrong Answers</b> tab to study every miss</li>
        </ol>

        <h3 style="color:#0078d7;">About the Real Test</h3>
        <p>The real Class D knowledge test needs 80% (32/40) to pass. This practice
        uses a stricter {MAX_WRONG}-wrong limit to push you toward mastery - if you can
        stay under {MAX_WRONG+1} here, you will comfortably pass the real thing.</p>

        <h3 style="color:#0078d7;">Honest Disclaimer</h3>
        <p>Unofficial practice tool. The real exam uses Idemia's AutoTest system with a
        protected question bank. These questions come from the same Minnesota Driver's
        Manual the real test draws from, but wording may differ. Read the free manual
        from the MN DVS website too.</p>

        <p><b>Cost:</b> $0 forever. Fully offline.</p>
        """)
        layout.addWidget(info_text)

    # ==================== DATABASE ====================
    def init_database(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_date TEXT,
                score INTEGER,
                wrong INTEGER,
                total INTEGER,
                passed INTEGER,
                restarted INTEGER DEFAULT 0
            )""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wrong_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                attempt_id INTEGER,
                test_date TEXT,
                question TEXT,
                your_answer TEXT,
                correct_answer TEXT,
                explanation TEXT,
                chapter TEXT
            )""")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS question_stats (
                qid TEXT PRIMARY KEY,
                times_right INTEGER DEFAULT 0,
                times_wrong INTEGER DEFAULT 0,
                last_wrong INTEGER DEFAULT 0,
                answered INTEGER DEFAULT 0
            )""")
        conn.commit()
        conn.close()

    def _stats(self):
        """qid -> (times_right, times_wrong, last_wrong, answered)"""
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT qid, times_right, times_wrong, last_wrong, answered FROM question_stats")
        rows = {r[0]: r[1:] for r in cur.fetchall()}
        conn.close()
        return rows

    def _update_stat(self, qid, correct_bool):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT times_right, times_wrong FROM question_stats WHERE qid=?", (qid,))
        row = cur.fetchone()
        if row:
            tr, tw = row
        else:
            tr, tw = 0, 0
        if correct_bool:
            tr += 1
        else:
            tw += 1
        cur.execute("""
            INSERT INTO question_stats (qid, times_right, times_wrong, last_wrong, answered)
            VALUES (?, ?, ?, ?, 1)
            ON CONFLICT(qid) DO UPDATE SET
                times_right=?, times_wrong=?, last_wrong=?, answered=1
        """, (qid, tr, tw, 0 if correct_bool else 1, tr, tw, 0 if correct_bool else 1))
        conn.commit()
        conn.close()

    # ==================== TEST FLOW ====================
    def _build_question_order(self):
        """Wrong-flagged first, then never-answered, then answered-correct. Each group shuffled."""
        stats = self._stats()
        wrong_first, unanswered, answered_right = [], [], []
        for q in QUESTION_BANK:
            s = stats.get(q.get("id"))
            if s is None or s[3] == 0:
                unanswered.append(q)
            elif s[2] == 1:
                wrong_first.append(q)
            else:
                answered_right.append(q)
        random.shuffle(wrong_first)
        random.shuffle(unanswered)
        random.shuffle(answered_right)
        return (wrong_first + unanswered + answered_right)[:TOTAL_QUESTIONS]

    def start_test(self):
        self.test_questions = self._build_question_order()
        self.current_question_index = 0
        self.user_answers = [-1] * len(self.test_questions)
        self.scored = [False] * len(self.test_questions)
        self.scored_right = [False] * len(self.test_questions)
        self.wrong_count = 0
        self.wrong_questions = []
        self.elapsed_seconds = 0
        self.test_active = True

        self.progress_bar.setValue(1)
        self.progress_bar.setFormat(f"Question %v of {len(self.test_questions)}")
        self.timer_label.setText("Time: 0:00")
        self.timer_label.setStyleSheet("color: #e0e0e0;")
        self.wrong_label.setText(f"Wrong: 0/{MAX_WRONG}")
        self.wrong_label.setStyleSheet("color: #e0e0e0; padding-left: 30px;")

        self.update_question_display()
        for rb in self.answer_radio_buttons:
            rb.setVisible(True)

        self.start_button.setEnabled(False)
        self.prev_button.setEnabled(False)
        self.next_button.setEnabled(True)
        self.submit_button.setEnabled(True)

        self.status_bar.setText(
            f"Test in progress - answer all {len(self.test_questions)} questions, "
            f"max {MAX_WRONG} wrong")
        self.status_bar.setStyleSheet(
            "background-color: #fff3cd; color: #856404; padding: 10px; "
            "font-weight: bold; font-size: 14px;")
        self.timer.start()

    def _score_current(self):
        """Score current question if answered and not yet scored. Returns True if restart triggered."""
        i = self.current_question_index
        if self.scored[i] or self.user_answers[i] == -1:
            return False
        self.scored[i] = True
        q = self.test_questions[i]
        is_right = self.user_answers[i] == q["correct"]
        self.scored_right[i] = is_right
        self._update_stat(q["id"], is_right)
        if not is_right:
            self.wrong_count += 1
            self.wrong_questions.append({
                "number": i + 1,
                "question": q["question"],
                "your_answer": q["options"][self.user_answers[i]],
                "correct_answer": q["options"][q["correct"]],
                "explanation": q["explanation"],
                "chapter": q["chapter"],
            })
            self.wrong_label.setText(f"Wrong: {self.wrong_count}/{MAX_WRONG}")
            self.wrong_label.setStyleSheet(
                "color: #ff6666; padding-left: 30px; font-weight: bold;")
            if self.wrong_count > MAX_WRONG:
                self.auto_restart()
                return True
        return False

    def auto_restart(self):
        """16th wrong answer - instantly restart with a fresh shuffle, wrong questions first."""
        self.timer.stop()
        self._save_attempt(passed=False, restarted=True)
        self.test_active = False

        self.status_bar.setText(
            f"{MAX_WRONG + 1} WRONG ANSWERS - TEST RESTARTING... missed questions come back first!")
        self.status_bar.setStyleSheet(
            "background-color: #c0392b; color: white; padding: 10px; "
            "font-weight: bold; font-size: 14px;")
        try:
            QApplication.beep()
        except Exception:
            pass

        QTimer.singleShot(1500, self.start_test)

    def on_answer_selected(self, option_index):
        if not (self.test_active and 0 <= self.current_question_index < len(self.user_answers)):
            return
        i = self.current_question_index
        if self.user_answers[i] == option_index:
            return
        self.user_answers[i] = option_index
        # If already scored and answer changed, rescore immediately (keeps live count honest)
        if self.scored[i]:
            q = self.test_questions[i]
            was_right = self.scored_right[i]
            now_right = option_index == q["correct"]
            if was_right != now_right:
                if now_right:
                    self.wrong_count -= 1
                    self.wrong_questions = [w for w in self.wrong_questions if w["number"] != i + 1]
                    self._update_stat(q["id"], True)
                else:
                    self.wrong_count += 1
                    self.wrong_questions.append({
                        "number": i + 1,
                        "question": q["question"],
                        "your_answer": q["options"][option_index],
                        "correct_answer": q["options"][q["correct"]],
                        "explanation": q["explanation"],
                        "chapter": q["chapter"],
                    })
                    self._update_stat(q["id"], False)
                self.scored_right[i] = now_right
                self.wrong_label.setText(f"Wrong: {self.wrong_count}/{MAX_WRONG}")
                if self.wrong_count > MAX_WRONG:
                    self.auto_restart()

    def previous_question(self):
        if self._score_current():
            return
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.update_question_display()

    def next_question(self):
        if self._score_current():
            return
        if self.current_question_index < len(self.test_questions) - 1:
            self.current_question_index += 1
            self.update_question_display()

    def update_question_display(self):
        q = self.test_questions[self.current_question_index]
        self.question_label.setText(
            f"Question {self.current_question_index + 1} of {len(self.test_questions)}"
            f"   [{q['chapter']}]\n\n{q['question']}")

        self.answer_group.setExclusive(False)
        for i, rb in enumerate(self.answer_radio_buttons):
            rb.setText(f"{chr(65 + i)}.  {q['options'][i]}")
            rb.setChecked(self.user_answers[self.current_question_index] == i)
        self.answer_group.setExclusive(True)

        self.progress_bar.setValue(self.current_question_index + 1)
        self.prev_button.setEnabled(self.current_question_index > 0)
        self.next_button.setEnabled(self.current_question_index < len(self.test_questions) - 1)

    def update_timer(self):
        if not self.test_active:
            return
        self.elapsed_seconds += 1
        m, s = divmod(self.elapsed_seconds, 60)
        h, m = divmod(m, 60)
        self.timer_label.setText(f"Time: {h}:{m:02d}:{s:02d}" if h else f"Time: {m}:{s:02d}")

    def confirm_submit(self):
        unanswered = sum(1 for a in self.user_answers if a == -1)
        msg = "Submit your test now?"
        if unanswered > 0:
            msg += f"\n\nWarning: {unanswered} question(s) still unanswered - they count as WRONG."
        reply = QMessageBox.question(
            self, "Submit Test", msg,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.finish_test()

    def finish_test(self):
        if not self.test_active:
            return
        # Score all remaining questions (unanswered count as wrong)
        self.current_question_index = max(0, self.current_question_index)
        for i in range(len(self.test_questions)):
            if self.scored[i]:
                continue
            self.scored[i] = True
            q = self.test_questions[i]
            ans = self.user_answers[i]
            is_right = ans == q["correct"]
            self._update_stat(q["id"], is_right)
            if not is_right:
                self.wrong_count += 1
                self.wrong_questions.append({
                    "number": i + 1,
                    "question": q["question"],
                    "your_answer": q["options"][ans] if ans != -1 else "(no answer)",
                    "correct_answer": q["options"][q["correct"]],
                    "explanation": q["explanation"],
                    "chapter": q["chapter"],
                })

        self.test_active = False
        self.timer.stop()
        self.timer_label.setStyleSheet("color: #e0e0e0;")

        score = len(self.test_questions) - self.wrong_count
        passed = self.wrong_count <= MAX_WRONG
        result = f"Score: {score}/{len(self.test_questions)} | Wrong: {self.wrong_count}/{MAX_WRONG} - "
        result += "PASSED" if passed else f"FAILED (more than {MAX_WRONG} wrong)"

        if passed:
            self.status_bar.setStyleSheet(
                "background-color: #28a745; color: white; padding: 10px; "
                "font-weight: bold; font-size: 14px;")
        else:
            self.status_bar.setStyleSheet(
                "background-color: #c0392b; color: white; padding: 10px; "
                "font-weight: bold; font-size: 14px;")
        self.status_bar.setText(result + " - Check 'Wrong Answers' tab to study")

        self.question_label.setText(
            "TEST COMPLETE\n\n" +
            f"{result}\n\nYou missed {self.wrong_count} question(s).\n"
            "Go to the 'Wrong Answers - Study These' tab to review every one.\n"
            f"Next test: your missed questions come back FIRST, then unanswered ones.")
        for rb in self.answer_radio_buttons:
            rb.setVisible(False)

        self.prev_button.setEnabled(False)
        self.next_button.setEnabled(False)
        self.submit_button.setEnabled(False)
        self.start_button.setEnabled(True)
        self.start_button.setText("Take Test Again")

        self._save_attempt(passed=passed, restarted=False)
        self.update_wrong_tab()

        if passed:
            QMessageBox.information(self, "PASSED",
                f"You stayed under {MAX_WRONG + 1} wrong - you passed!\n\n"
                "Keep practicing until you pass every time.")
        else:
            QMessageBox.warning(self, "Restart Required",
                f"You had {self.wrong_count} wrong (limit is {MAX_WRONG}).\n\n"
                "The test auto-restarts next time you click Start - your missed "
                "questions will be first in the new shuffle.")

    # ==================== PERSISTENCE ====================
    def _save_attempt(self, passed, restarted):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        test_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        score = sum(1 for i, q in enumerate(getattr(self, "test_questions", []))
                    if self.user_answers and i < len(self.user_answers)
                    and self.user_answers[i] == q["correct"])
        cur.execute(
            "INSERT INTO attempts (test_date, score, wrong, total, passed, restarted) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (test_date, score, self.wrong_count,
             len(getattr(self, "test_questions", [])), 1 if passed else 0,
             1 if restarted else 0))
        attempt_id = cur.lastrowid
        for w in self.wrong_questions:
            cur.execute("""
                INSERT INTO wrong_questions
                (attempt_id, test_date, question, your_answer, correct_answer, explanation, chapter)
                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (attempt_id, test_date, w["question"], w["your_answer"],
                 w["correct_answer"], w["explanation"], w["chapter"]))
        conn.commit()
        conn.close()

    def update_wrong_tab(self):
        self.wrong_list.clear()
        if not self.wrong_questions:
            self.wrong_list.addItem(QListWidgetItem(
                "No wrong answers on your last test - great job!"))
            return
        for w in self.wrong_questions:
            text = (
                f"Q{w['number']} [{w['chapter']}]\n"
                f"{w['question']}\n\n"
                f"Your answer: {w['your_answer']}\n"
                f"Correct answer: {w['correct_answer']}\n"
                f"Why: {w['explanation']}\n"
                f"{'-' * 70}")
            self.wrong_list.addItem(QListWidgetItem(text))
        self.tabs.setCurrentWidget(self.wrong_tab)

    def load_wrong_history(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            SELECT question, your_answer, correct_answer, explanation, chapter, test_date
            FROM wrong_questions ORDER BY test_date DESC LIMIT 50""")
        rows = cur.fetchall()
        conn.close()
        for row in rows:
            text = (
                f"[{row[4]}] (missed {row[5]})\n"
                f"{row[0]}\n\n"
                f"Your answer: {row[1]}\n"
                f"Correct answer: {row[2]}\n"
                f"Why: {row[3]}\n"
                f"{'-' * 70}")
            self.wrong_list.addItem(QListWidgetItem(text))

    def export_wrong_questions(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            SELECT question, your_answer, correct_answer, explanation, chapter
            FROM wrong_questions ORDER BY test_date DESC""")
        rows = cur.fetchall()
        conn.close()
        if not rows:
            QMessageBox.information(self, "Nothing to Export", "No wrong answers saved yet.")
            return
        filename = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            f"wrong_questions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Question", "Your Answer", "Correct Answer", "Explanation", "Chapter"])
            writer.writerows(rows)
        QMessageBox.information(self, "Export Complete",
                              f"Exported {len(rows)} questions to:\n{filename}")

    def clear_history(self):
        reply = QMessageBox.question(
            self, "Clear History",
            "Delete ALL saved history including wrong-answer memory?\n"
            "The test will forget which questions you struggle with.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply != QMessageBox.StandardButton.Yes:
            return
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("DELETE FROM wrong_questions")
        cur.execute("DELETE FROM attempts")
        cur.execute("DELETE FROM question_stats")
        conn.commit()
        conn.close()
        self.wrong_list.clear()
        QMessageBox.information(self, "Cleared", "All history cleared.")


def main():
    app = QApplication(sys.argv)
    window = MinnesotaPermitTest()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
