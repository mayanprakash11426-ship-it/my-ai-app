from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Ellipse, RoundedRectangle
from kivy.core.window import Window
from kivy.clock import Clock

from google import genai
import threading


# =========================================================
# GEMINI SETTINGS
# =========================================================

API_KEY = "AQ.Ab8RN6Lr95LBAO9S4EI7Ke2iTJ1ss5YRATgRI39LiXphRNADpQ"

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.8-flash"


# =========================================================
# MY AI
# =========================================================

def ask_gemini(question):

    try:

        prompt = """
You are My AI, a friendly and intelligent personal AI assistant.

Answer naturally and clearly.

If the user speaks Hindi or Hinglish,
reply in Hindi or Hinglish.

For Class 9 study questions:
- use easy language
- give exam-friendly answers
- explain step-by-step when needed

Keep simple questions concise.
Do not unnecessarily repeat the question.

User:
""" + question

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        return response.text

    except Exception as e:

        return "Sorry, Gemini error:\n" + str(e)


# =========================================================
# CHAT TEXT
# =========================================================

class ChatLabel(Label):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.size_hint_y = None
        self.halign = "left"
        self.valign = "top"

        self.bind(
            texture_size=self.update_height
        )

    def update_height(self, *args):

        self.height = self.texture_size[1] + 40


# =========================================================
# MY AI CHATBOX
# =========================================================

class AIChat(Widget):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        # -------------------------------------------------
        # WIDE CHATBOX
        # -------------------------------------------------

        self.width = Window.width * 0.94

        self.height = Window.height * 0.56

        self.x = (
            Window.width - self.width
        ) / 2

        # Upper-center
        self.y = (
            Window.height
            - self.height
            - 35
        )

        # -------------------------------------------------
        # BACKGROUND
        # -------------------------------------------------

        with self.canvas:

            Color(
                0.025,
                0.035,
                0.065,
                0.99
            )

            self.bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[28]
            )

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        self.title = Label(

            text="☁  My AI",

            font_size=max(
                22,
                min(
                    27,
                    self.width / 15
                )
            ),

            bold=True,

            color=(
                0.55,
                0.85,
                1,
                1
            ),

            size_hint=(None, None),

            size=(
                240,
                55
            ),

            pos=(
                self.x + 18,
                self.top - 58
            )
        )

        self.add_widget(
            self.title
        )

        # -------------------------------------------------
        # ONLINE
        # -------------------------------------------------

        self.status = Label(

            text="● Online",

            font_size=max(
                12,
                min(
                    15,
                    self.width / 25
                )
            ),

            color=(
                0.35,
                1,
                0.65,
                1
            ),

            size_hint=(None, None),

            size=(
                110,
                25
            ),

            pos=(
                self.x + 20,
                self.top - 82
            )
        )

        self.add_widget(
            self.status
        )

        # -------------------------------------------------
        # CLOSE
        # -------------------------------------------------

        self.close_button = Button(

            text="×",

            font_size=max(
                26,
                min(
                    32,
                    self.width / 13
                )
            ),

            background_normal="",

            background_color=(
                0.12,
                0.14,
                0.20,
                1
            ),

            size_hint=(None, None),

            size=(
                50,
                50
            ),

            pos=(
                self.right - 63,
                self.top - 58
            )
        )

        self.close_button.bind(
            on_press=self.close_chat
        )

        self.add_widget(
            self.close_button
        )

        # -------------------------------------------------
        # SCROLL AREA
        # -------------------------------------------------

        self.scroll = ScrollView(

            size_hint=(None, None),

            size=(
                self.width - 30,
                self.height - 145
            ),

            pos=(
                self.x + 15,
                self.y + 78
            ),

            do_scroll_x=False,

            do_scroll_y=True,

            bar_width=5
        )

        # -------------------------------------------------
        # CHAT CONTENT
        # -------------------------------------------------

        self.chat = ChatLabel(

            text=(
                "My AI:\n\n"
                "Hello 👋\n"
                "I'm ready to help you.\n\n"
                "Ask me anything!"
            ),

            # Responsive text size
            font_size=max(
                17,
                min(
                    22,
                    self.width / 18
                )
            ),

            color=(
                0.93,
                0.95,
                1,
                1
            ),

            text_size=(
                self.width - 60,
                None
            )
        )

        self.scroll.add_widget(
            self.chat
        )

        self.add_widget(
            self.scroll
        )

        # -------------------------------------------------
        # INPUT
        # -------------------------------------------------

        self.input_box = TextInput(

            hint_text="Message My AI...",

            font_size=max(
                16,
                min(
                    20,
                    self.width / 20
                )
            ),

            multiline=False,

            background_normal="",

            background_color=(
                0.09,
                0.11,
                0.16,
                1
            ),

            foreground_color=(
                1,
                1,
                1,
                1
            ),

            cursor_color=(
                0.35,
                0.80,
                1,
                1
            ),

            padding=[
                15,
                13
            ],

            size_hint=(None, None),

            size=(
                self.width - 90,
                55
            ),

            pos=(
                self.x + 15,
                self.y + 15
            )
        )

        self.input_box.bind(
            on_text_validate=self.send_message
        )

        self.add_widget(
            self.input_box
        )

        # -------------------------------------------------
        # SEND
        # -------------------------------------------------

        self.send_button = Button(

            text="➤",

            font_size=max(
                22,
                min(
                    28,
                    self.width / 14
                )
            ),

            background_normal="",

            background_color=(
                0.10,
                0.52,
                1,
                1
            ),

            size_hint=(None, None),

            size=(
                60,
                55
            ),

            pos=(
                self.right - 75,
                self.y + 15
            )
        )

        self.send_button.bind(
            on_press=self.send_message
        )

        self.add_widget(
            self.send_button
        )

        # Keyboard
        Window.bind(
            keyboard_height=self.keyboard_changed
        )

    # =====================================================
    # KEYBOARD
    # =====================================================

    def keyboard_changed(
        self,
        window,
        height
    ):

        if height > 0:

            self.y = height + 15

            max_y = (
                Window.height
                - self.height
                - 10
            )

            self.y = min(
                self.y,
                max_y
            )

        else:

            self.y = (
                Window.height
                - self.height
                - 35
            )

        self.update_layout()

    # =====================================================
    # UPDATE LAYOUT
    # =====================================================

    def update_layout(self):

        self.bg.pos = self.pos
        self.bg.size = self.size

        self.title.pos = (
            self.x + 18,
            self.top - 58
        )

        self.status.pos = (
            self.x + 20,
            self.top - 82
        )

        self.close_button.pos = (
            self.right - 63,
            self.top - 58
        )

        self.scroll.pos = (
            self.x + 15,
            self.y + 78
        )

        self.scroll.size = (
            self.width - 30,
            self.height - 145
        )

        self.chat.text_size = (
            self.width - 60,
            None
        )

        self.input_box.pos = (
            self.x + 15,
            self.y + 15
        )

        self.send_button.pos = (
            self.right - 75,
            self.y + 15
        )

    # =====================================================
    # SEND
    # =====================================================

    def send_message(self, instance):

        question = self.input_box.text.strip()

        if not question:
            return

        self.chat.text += (
            "\n\n"
            "You:\n"
            + question
            + "\n\n"
            "☁ My AI:\n"
            "Thinking..."
        )

        self.input_box.text = ""

        self.send_button.disabled = True

        Clock.schedule_once(
            self.scroll_bottom,
            0.1
        )

        threading.Thread(
            target=self.get_answer,
            args=(question,),
            daemon=True
        ).start()

    # =====================================================
    # GEMINI
    # =====================================================

    def get_answer(self, question):

        answer = ask_gemini(question)

        Clock.schedule_once(
            lambda dt: self.show_answer(answer),
            0
        )

    # =====================================================
    # SHOW ANSWER
    # =====================================================

    def show_answer(self, answer):

        self.chat.text = self.chat.text.replace(
            "Thinking...",
            answer
        )

        self.send_button.disabled = False

        Clock.schedule_once(
            self.scroll_bottom,
            0.1
        )

    # =====================================================
    # SCROLL
    # =====================================================

    def scroll_bottom(self, *args):

        self.scroll.scroll_y = 0

    # =====================================================
    # CLOSE
    # =====================================================

    def close_chat(self, instance):

        Window.unbind(
            keyboard_height=self.keyboard_changed
        )

        if self.parent:

            self.parent.remove_widget(
                self
            )


# =========================================================
# FLOATING SKY CLOUD BUTTON
# =========================================================

class SkyButton(Widget):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.size = (
            95,
            95
        )

        self.pos = (
            Window.width - 115,
            80
        )

        # -------------------------------------------------
        # SKY CIRCLE
        # -------------------------------------------------

        with self.canvas:

            Color(
                0.10,
                0.55,
                1,
                1
            )

            self.circle = Ellipse(
                pos=self.pos,
                size=self.size
            )

            Color(
                0.025,
                0.10,
                0.20,
                1
            )

            self.inner = Ellipse(
                pos=(
                    self.x + 5,
                    self.y + 5
                ),
                size=(
                    85,
                    85
                )
            )

        # -------------------------------------------------
        # CLOUD LOGO
        # -------------------------------------------------

        with self.canvas:

            Color(
                0.90,
                0.97,
                1,
                1
            )

            self.cloud1 = Ellipse(
                pos=(
                    self.x + 18,
                    self.y + 32
                ),
                size=(
                    35,
                    25
                )
            )

            self.cloud2 = Ellipse(
                pos=(
                    self.x + 30,
                    self.y + 42
                ),
                size=(
                    40,
                    35
                )
            )

            self.cloud3 = Ellipse(
                pos=(
                    self.x + 50,
                    self.y + 32
                ),
                size=(
                    35,
                    25
                )
            )

            self.cloud_base = RoundedRectangle(
                pos=(
                    self.x + 20,
                    self.y + 30
                ),
                size=(
                    60,
                    23
                ),
                radius=[10]
            )

        self.bind(
            pos=self.update_logo
        )

        self.dragging = False

    # =====================================================
    # UPDATE CLOUD
    # =====================================================

    def update_logo(self, *args):

        self.circle.pos = self.pos

        self.inner.pos = (
            self.x + 5,
            self.y + 5
        )

        self.cloud1.pos = (
            self.x + 18,
            self.y + 32
        )

        self.cloud2.pos = (
            self.x + 30,
            self.y + 42
        )

        self.cloud3.pos = (
            self.x + 50,
            self.y + 32
        )

        self.cloud_base.pos = (
            self.x + 20,
            self.y + 30
        )

    # =====================================================
    # TOUCH DOWN
    # =====================================================

    def on_touch_down(self, touch):

        if self.collide_point(
            *touch.pos
        ):

            self.start_x = touch.x
            self.start_y = touch.y

            self.dragging = False

            return True

        return super().on_touch_down(
            touch
        )

    # =====================================================
    # DRAG
    # =====================================================

    def on_touch_move(self, touch):

        if (
            abs(
                touch.x - self.start_x
            ) > 10

            or

            abs(
                touch.y - self.start_y
            ) > 10
        ):

            self.dragging = True

        if self.dragging:

            self.pos = (
                touch.x - 47,
                touch.y - 47
            )

            self.x = max(
                0,
                min(
                    self.x,
                    Window.width - self.width
                )
            )

            self.y = max(
                0,
                min(
                    self.y,
                    Window.height - self.height
                )
            )

            return True

        return super().on_touch_move(
            touch
        )

    # =====================================================
    # TOUCH UP
    # =====================================================

    def on_touch_up(self, touch):

        if self.collide_point(
            *touch.pos
        ):

            if not self.dragging:

                self.parent.add_widget(
                    AIChat()
                )

            self.dragging = False

            return True

        return super().on_touch_up(
            touch
        )


# =========================================================
# MAIN APP
# =========================================================

class MyAI(App):

    def build(self):

        root = Widget()

        root.add_widget(
            SkyButton()
        )

        return root


# =========================================================
# RUN
# =========================================================

MyAI().run()