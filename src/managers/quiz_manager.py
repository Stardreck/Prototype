from __future__ import annotations

import random
import pygame
from typing import TYPE_CHECKING, Optional, cast

from components.ui.answer_list import AnswerList
from components.ui.buttons.button import Button
from components.ui.panel import Panel
from components.ui.text import Text
from enums.color import Color

if TYPE_CHECKING:
    from games.story_game import StoryGame


class QuizManager:
    """
    Manages quizzes and tasks within the StoryGame.
    """

    def __init__(self, game: StoryGame) -> None:
        """
        Initialize the QuizManager with a reference to the StoryGame instance.
        :param game: The StoryGame instance.
        """
        self.game: StoryGame = game
        self.font: pygame.font.Font = pygame.font.SysFont(None, 24)
        self.is_quiz_present: False
        self.last_result_is_correct: False

    def get_random_quiz_for_planet(self, planet_name: str) -> Optional[dict]:
        """
        Retrieve a random quiz for the specified planet.
        :param planet_name: Name of the planet.
        :return: A dictionary containing quiz data or None.
        """
        quizzes = self.game.planet_quizzes_current.get(planet_name)

        if not quizzes:
            # Reload quizzes if none available
            self.game.planet_quizzes_current[planet_name] = list(self.game.data.planet_quizzes.get(planet_name, []))
            quizzes = self.game.planet_quizzes_current[planet_name]

        if quizzes:
            return quizzes.pop(random.randint(0, len(quizzes) - 1))
        return None

    def run_quiz_scene(self, quiz_data: dict) -> None:
        """
        Run a quiz scene based on the provided quiz data.
        :param quiz_data: Dictionary containing quiz information.
        """
        quiz_type = quiz_data.get("type", "quiz")
        if quiz_type == "quiz":
            self._run_multiple_choice_quiz(quiz_data)
        elif quiz_type == "task":
            self._run_task_quiz(quiz_data)
        else:
            print("Unknown quiz type: ", quiz_type)

    def _run_multiple_choice_quiz(self, quiz_data: dict) -> None:
        """
        Run a multiple-choice quiz.
        :param quiz_data: Dictionary containing multiple-choice quiz information.
        """
        question, options, correct_idx = quiz_data["question"], quiz_data["options"], quiz_data["correct_idx"]
        self._run_quiz_loop(question, options, correct_idx, is_task=False)

    def _run_task_quiz(self, quiz_data: dict) -> None:
        """
        Run a task-based quiz.
        :param quiz_data: Dictionary containing task information.
        """
        question, correct_value = quiz_data["question"], quiz_data["correct_value"]
        self._run_quiz_loop(question, correct_value, None, is_task=True)

    def button_click(self):
        print("button clicked inside quiz")

    def _run_quiz_loop(self, question: str,
                       answer_data,
                       correct_idx: Optional[int],
                       is_task: bool) -> None:
        """
        Main loop for quiz input and handling.
        :param question: The quiz question.
        :param answer_data: Options for multiple choice or correct value for task.
        :param correct_idx: Index of the correct option (only for multiple-choice quizzes).
        :param is_task: Flag to indicate if this is a task quiz.
        """
        user_input = ""
        self.is_quiz_present = True

        button_component = self.game.ui_manager.ui_components.get("default_panel_confirm_button")
        # cast UIComponent to Button
        confirm_button = cast(Button, button_component)
        confirm_button.set_on_click(lambda: self._process_user_input(user_input, answer_data, correct_idx, is_task))

        while self.is_quiz_present and self.game.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.stop()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.stop()
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif self._is_valid_input(event.key, is_task):
                        user_input += self._map_key_to_char(event.key)

                for key, component in self.game.ui_manager.ui_components.items():
                    component.handle_event(event)
            if self.is_quiz_present:
                self._render_quiz_overlay(question, user_input, is_task, answer_data if not is_task else None)

        confirm_button.set_on_click(None)

    def _process_user_input(self, user_input: str,
                            answer_data,
                            correct_idx: Optional[int],
                            is_task: bool) -> bool:
        """
        Process user input and determine if the answer is correct.
        :param user_input: User's input as a string.
        :param answer_data: Correct value or list of options.
        :param correct_idx: Correct option index for multiple-choice quizzes.
        :param is_task: Flag to indicate if this is a task quiz.
        :return: True if the input is processed successfully, False otherwise.
        """
        try:
            if is_task:
                user_value = float(user_input)
                tolerance = abs(answer_data * 0.01)
                is_correct = abs(user_value - answer_data) <= tolerance
            else:
                is_correct = int(user_input) == correct_idx

            # store is_correct for the next iteration
            self.last_result_is_correct = is_correct

            if is_correct:
                self._display_feedback("Correct answer!")
                self.game.event_manager.decrease_error_count()
            else:
                self._display_feedback("Wrong answer! Hull -1.")
                self.game.hull -= 1
                self.game.event_manager.increase_error_count()
                if self.game.hull <= 0:
                    self.game.game_over("Your ship has been destroyed!")
            self.is_quiz_present = False
            return True
        except ValueError:
            self.is_quiz_present = True
            return False

    def _is_valid_input(self, key: int, is_task: bool) -> bool:
        """
        Check if the input key is valid.
        :param key: Key event code.
        :param is_task: Flag to indicate if this is a task quiz.
        :return: True if the key is valid, False otherwise.
        """
        if is_task:
            return key in range(pygame.K_0, pygame.K_9 + 1) or key == pygame.K_PERIOD
        return key in range(pygame.K_0, pygame.K_9 + 1)

    def _map_key_to_char(self, key: int) -> str:
        """
        Map key event to corresponding character.
        :param key: Key event code.
        :return: Character representation of the key.
        """
        if key == pygame.K_PERIOD:
            return "."
        return str(key - pygame.K_0)

    def _render_quiz_overlay(self, question: str, user_input: str, is_task: bool, options: Optional[list[str]]) -> None:
        """
        Render the quiz overlay on the game screen.
        :param question: The quiz question.
        :param user_input: Current user input.
        :param options: List of options for multiple-choice quizzes.
        """
        self.game.draw()

        target_surface = (self.game.screen.subsurface(self.game.game_rect)
                          if self.game.debug_manager.debug_mode else self.game.screen)

        bg_panel = cast(Panel, self.game.ui_manager.ui_components.get("default_panel_bg"))
        bg_panel.draw(target_surface)

        panel = cast(Panel, self.game.ui_manager.ui_components.get("default_panel"))
        panel.draw(target_surface)

        subtitle = cast(Text, self.game.ui_manager.ui_components.get("default_panel_subtitle"))
        subtitle.set_text(question)
        subtitle.draw(target_surface)

        confirm_button = cast(Button, self.game.ui_manager.ui_components.get("default_panel_confirm_button"))
        confirm_button.draw(target_surface)

        if is_task:
            # calculations task
            title = cast(Text, self.game.ui_manager.ui_components.get("default_panel_title"))
            title.set_text("Aufgabe")
            title.draw(target_surface)
        else:
            # multiple choice
            title = cast(Text, self.game.ui_manager.ui_components.get("default_panel_title"))
            title.set_text("Quiz-Frage")
            title.draw(target_surface)
            answer_list = AnswerList(
                options,
                self.font,
                (255, 255, 255),
                start_position=(554, 291),
                line_spacing=40
            )
            answer_list.draw(target_surface)


        answer_text = Text(f"Antwort eingeben: {user_input}", self.font, (255, 255, 255), (554, 479))
        answer_text.draw(target_surface)

        pygame.display.flip()

    def _display_feedback(self, message: str, duration: int = 1000) -> None:
        """
        Display feedback (e.g., 'Correct answer!') for a set duration.
        :param message: The feedback message to display.
        :param duration: Duration in milliseconds to display the message.
        """
        feedback_surface = pygame.Surface(self.game.screen.get_size())
        feedback_surface.set_alpha(180)
        feedback_surface.fill(Color.BLACK.value)

        font = pygame.font.SysFont(None, 48)
        text_surface = font.render(message, True, Color.WHITE.value)
        text_rect = text_surface.get_rect(center=(self.game.screen.get_width() // 2,
                                                  self.game.screen.get_height() // 2))
        feedback_surface.blit(text_surface, text_rect)

        start_time = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start_time < duration:
            self.game.screen.blit(feedback_surface, (0, 0))
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.stop()
                    return

    # todo remove this old methods later on
    def _run_quiz_loopx(self, question: str,
                        answer_data,
                        correct_idx: Optional[int],
                        is_task: bool) -> None:
        """
        Main loop for quiz input and handling.
        :param question: The quiz question.
        :param answer_data: Options for multiple choice or correct value for task.
        :param correct_idx: Index of the correct option (only for multiple-choice quizzes).
        :param is_task: Flag to indicate if this is a task quiz.
        """
        user_input = ""
        waiting = True

        while waiting and self.game.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.stop()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game.stop()
                        return
                    elif event.key == pygame.K_d:
                        self.game.debug_manager.toggle_debug_mode()
                    elif event.key == pygame.K_RETURN:
                        waiting = not self._process_user_input(user_input, answer_data, correct_idx, is_task)
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif self._is_valid_input(event.key, is_task):
                        user_input += self._map_key_to_char(event.key)

            if waiting:
                self._render_quiz_overlay(question, user_input, answer_data if not is_task else None)

    def _render_quiz_overlayx(self, question: str, user_input: str, options: Optional[list[str]]) -> None:
        """
        Render the quiz overlay on the game screen.
        :param question: The quiz question.
        :param user_input: Current user input.
        :param options: List of options for multiple-choice quizzes.
        """
        self.game.draw()

        target_surface = (self.game.screen.subsurface(self.game.game_rect)
                          if self.game.debug_manager.debug_mode else self.game.screen)
        overlay_width = target_surface.get_width()
        overlay_height = 250

        overlay_rect = pygame.Rect(0, target_surface.get_height() - overlay_height, overlay_width, overlay_height)
        quiz_overlay = pygame.Surface((overlay_width, overlay_height))
        quiz_overlay.set_alpha(180)
        quiz_overlay.fill(Color.BLACK.value)

        lines = [f"QUESTION: {question}"]
        if options:
            lines.extend([f"{i}) {opt}" for i, opt in enumerate(options)])
        lines.append("")
        lines.append(f"Enter answer: {user_input}")

        y_offset = 10
        for line in lines:
            line_img = self.font.render(line, True, Color.WHITE.value)
            quiz_overlay.blit(line_img, (10, y_offset))
            y_offset += line_img.get_height() + 5

        target_surface.blit(quiz_overlay, (overlay_rect.x, overlay_rect.y))
        pygame.display.flip()
