from tkinter import *
import random
import requests
import ast
import time
import pygame
import tkinter as tk

pygame.mixer.init()

correct_sound = pygame.mixer.Sound("sounds/correct_answer.mp3")
incorrect_sound = pygame.mixer.Sound("sounds/incorrect_answer.mp3")
countdown_music = pygame.mixer.music.load("sounds/clock_countdown.mp3")
result_sound = pygame.mixer.Sound("sounds/result_sound.mp3")
click_sound = pygame.mixer.Sound("sounds/click_sound.mp3")
not_type_sound = pygame.mixer.Sound("sounds/not_type.mp3")
not_type_sound.set_volume(4)

click_sound.set_volume(2)

window = Tk()
window.title("Quiz game")

score = 0
fr_score = 0
number_question = 0
after_id = ""
animation_after = ""
play_number = 0
animation_number = -1
full_seconds = 0
incorrect_direction = {"questions": [], "answers": []}
correct_direction = {"questions": [], "answers": []}
selected1 = ""
selected2 = ""
select_text_tru_fal1 = True
select_text_tru_fal2 = True
middle_start = True

difficulty_label_info = Label(window, text="", bg="black", font=("Times New Roman", 12))
category_label_info = Label(window, text="", fg="white", bg="black", font=("Times New Roman", 12))


def sec(dif):
    if dif == "easy":
        seco = 20
    elif dif == "medium" or dif == "hard":
        seco = 15
    return seco

def error(framik):
    Label(framik, text="An error has occured. Please try it again later.", font=("Times New Roman", 17, "bold"), fg="red", bg="white").place(x=250, y=120, anchor="center")
    Label(framik, text="Check your internet connection.", font=("Times New Roman", 12), fg="grey", bg="white").place(x=250, y=145, anchor="center")
    def go_back():
        for widget in framik.winfo_children():
            widget.destroy()
        framik.destroy()
        login_game()
    button_try = Button(framik, text="Try again", fg="white", bg="black", font=("Arial", 13), command=go_back)
    button_try.place(x=250, y=280, anchor="center")


def start_game(frame_width, start_frame, bg_frame_color, main_fg_color, amount_string_var, category_string_var,
               difficulty_string_var, frame_height):
    global selected1, selected2, middle_start
    amount_text = amount_string_var.get()
    category_text = category_string_var.get()
    difficulty_text = difficulty_string_var.get()

    if amount_text != "None" and category_text != "None" and difficulty_text != "None":
        start_frame.destroy()
        click_sound.play()

        selected1 = ""
        selected2 = ""

        with open("files/category_names.txt", "r") as file:
            s = file.read()
            r = ast.literal_eval(s)

        category_number = r[category_text]["number"]

        seconds = sec(difficulty_text)

        width2 = 600
        height2 = 400 + 40
        # screen_width_2 = window.winfo_screenwidth()
        # screen_height_2 = window.winfo_screenheight()
        # x2 = int(screen_width_2 // 2 - width2 // 2)
        # y2 = int(screen_height_2 // 2 - height2 // 2 - 75)
        middle_start = False
        x2 = window.winfo_x()
        y2 = window.winfo_y()
        window.geometry(f"{width2}x{height2}+{x2}+{y2}")

        game_frame = Frame(window, width=frame_width, height=frame_height + 40, bg=bg_frame_color)
        game_frame.place(x=50, y=25)

        try:
            response = requests.get(f"https://opentdb.com/api.php?amount={amount_text}&category={category_number}&difficulty={difficulty_text}&type=multiple")
            text = response.json()

            def new_score_label():
                score_label = Label(game_frame, font=("Times New Roman", 15), fg="black", bg=bg_frame_color,
                                    text=f"{score}/{fr_score}")
                score_label.place(anchor="ne", x=frame_width - 8, y=15)
                return score_label

            score_label = new_score_label()

            def again_game(animation_after):
                global score, fr_score, number_question, play_number, animation_number, full_seconds, incorrect_direction, correct_direction
                score = 0
                fr_score = 0
                number_question = 0
                play_number = 0
                animation_number = -1
                pygame.mixer.music.stop()
                full_seconds = 0
                incorrect_direction = {"questions": [], "answers": []}
                correct_direction = {"questions": [], "answers": []}
                pygame.mixer.music.load("sounds/clock_countdown.mp3")

                click_sound.play()

                game_frame.after_cancel(animation_after)

                login_game()

            def correct_see(cor_but, incor_but, result_screen, canvasik):
                global correct_direction
                if cor_but["state"] != DISABLED:
                    click_sound.play()
                    canvasik.delete("all")

                    cor_but.config(state=DISABLED, border=1, cursor="arrow")
                    incor_but.config(state=NORMAL, border=3, cursor="hand2")
                    result_screen.config(bg="#cef2db")

                    questions = []
                    answers = []
                    for one_question in correct_direction["questions"]:
                        questions.append(one_question)
                    for one_answer in correct_direction["answers"]:
                        answers.append(one_answer)

                    canvasik.create_text(0, 0, anchor="nw", text=" ")
                    img = PhotoImage(file=r"imgs/check_24.png")
                    result_screen.img = img
                    if len(questions) == 0:
                        canvasik.create_text(215, 40, anchor="center", text="No correct answers",
                                             font=("Times New Roman", 18, "bold"), fill="grey")
                    else:

                        for num2 in range(len(questions)):
                            canvasik.create_text(15, num2 * 60 + 10, anchor="nw", text=f"{questions[num2]}     ",
                                                 font=("Times New Roman", 13, "bold"))
                            if num2 == len(questions) - 1:
                                canvasik.create_text(250, num2 * 60 + 40, anchor="nw", fill="green",
                                                     text=f"{answers[num2]}     \n ",
                                                     font=("Times New Roman", 12))
                            else:
                                canvasik.create_text(250, num2 * 60 + 40, anchor="nw", fill="green",
                                                     text=f"{answers[num2]}     ",
                                                     font=("Times New Roman", 12))
                            canvasik.create_image((245, num2 * 60 + 37), image=img, anchor="ne")

                    canvasik.config(scrollregion=canvasik.bbox("all"))

                    text_scrollbar = Scrollbar(result_screen, command=canvasik.yview)
                    text_scrollbar.place(anchor="nw", x=459, y=70, height=309)

                    text_scrollbar_x = Scrollbar(result_screen, command=canvasik.xview, orient="horizontal")
                    text_scrollbar_x.place(anchor="nw", x=22, y=378, width=439)

                    canvasik.config(yscrollcommand=text_scrollbar.set, xscrollcommand=text_scrollbar_x.set)
                    canvasik.place(anchor="nw", x=22, y=70)

            def incorrect_see(incor_but, cor_but, result_screen, canvasik):
                global incorrect_direction
                if incor_but["state"] != DISABLED:
                    click_sound.play()
                    canvasik.delete("all")

                    incor_but.config(state=DISABLED, border=1, cursor="arrow")
                    cor_but.config(state=NORMAL, border=3, cursor="hand2")
                    result_screen.config(bg="#ffd7d7")

                    questions2 = []
                    correct_answers2 = []
                    incorrect_answers2 = []

                    for one_question in incorrect_direction["questions"]:
                        questions2.append(one_question)
                    for correct_answer in incorrect_direction["answers"]:
                        correct_answers2.append(correct_answer[1])
                    for incorrect_answer in incorrect_direction["answers"]:
                        incorrect_answers2.append(incorrect_answer[0])

                    canvasik.create_text(0, 0, anchor="nw", text=" ")
                    img = PhotoImage(file=r"imgs/wrong_24.png")
                    result_screen.img = img
                    if len(questions2) == 0:
                        canvasik.create_text(215, 40, font=("Times New Roman", 18, "bold"), fill="grey",
                                             text="No incorrect answers")
                    else:
                        for num2 in range(len(questions2)):
                            canvasik.create_text(15, num2 * 90 + 10, anchor="nw", text=f"{questions2[num2]}     ",
                                                 font=("Times New Roman", 13, "bold"))

                            canvasik.create_text(250, num2 * 90 + 40, anchor="nw", fill="red",
                                                 text=f"{incorrect_answers2[num2]}     ",
                                                 font=("Times New Roman", 12))
                            canvasik.create_text(245, num2 * 90 + 70, anchor="ne", text="Correct answer:", fill="green",
                                                 font=("Times New Roman", 12))
                            if len(questions2) - 1 == num2:
                                canvasik.create_text(250, num2 * 90 + 70, anchor="nw", fill="green",
                                                     text=f"{correct_answers2[num2]}     \n ",
                                                     font=("Times New Roman", 12))
                            else:
                                canvasik.create_text(250, num2 * 90 + 70, anchor="nw", fill="green",
                                                     text=f"{correct_answers2[num2]}     ",
                                                     font=("Times New Roman", 12))
                            canvasik.create_image((245, num2 * 90 + 37), image=img, anchor="ne")


                    canvasik.config(scrollregion=canvasik.bbox("all"))

                    text_scrollbar = Scrollbar(result_screen, command=canvasik.yview)
                    text_scrollbar.place(anchor="nw", x=459, y=70, height=309)

                    text_scrollbar_x = Scrollbar(result_screen, command=canvasik.xview, orient="horizontal")
                    text_scrollbar_x.place(anchor="nw", x=22, y=378, width=439)

                    canvasik.config(yscrollcommand=text_scrollbar.set, xscrollcommand=text_scrollbar_x.set)
                    canvasik.place(anchor="nw", x=22, y=70)

            def see_results():
                global result_screen
                try:
                    result_screen.destroy()
                except:
                    pass

                result_screen = Toplevel()
                result_screen.resizable(False, False)
                result_screen.title("Your answers")
                result_screen.iconbitmap("imgs/icon_your_answers.ico")
                result_screen.config(bg="#cef2db")

                x_need = window.winfo_x()
                print(x_need)
                y_need = window.winfo_y()
                if x_need >= 500:
                    result_screen.geometry(f"500x400+{x_need-510}+{y_need + 15}")
                elif x_need >= 314:
                    result_screen.geometry(f"500x400+{20}+{y_need + 15}")
                else:
                    result_screen.geometry(f"500x400+{x_need + 610}+{y_need + 15}")


                click_sound.play()

                canvasik = Canvas(result_screen, border=2, bg="white", width=430, height=300,
                                  relief="solid")

                correct_answers_button = Button(result_screen, text="Your correct answers", border=0,
                                                font=("Times New Roman", 11, "bold"), relief="solid",
                                                command=lambda: correct_see(correct_answers_button,
                                                                            incorrect_answers_button,
                                                                            result_screen, canvasik), cursor="hand2")
                correct_answers_button.place(anchor="ne", x=230, y=20)

                incorrect_answers_button = Button(result_screen, text="Your incorrect answers", border=1,
                                                  font=("Times New Roman", 11, "bold"), relief="solid",
                                                  command=lambda: incorrect_see(incorrect_answers_button,
                                                                                correct_answers_button, result_screen,
                                                                                canvasik), cursor="hand2")
                incorrect_answers_button.place(anchor="nw", x=270, y=20)

                correct_see(correct_answers_button, incorrect_answers_button, result_screen, canvasik)

                result_screen.mainloop()

            def end_of_the_game(id):
                global score, fr_score, number_question, play_number, animation_number, animation_after

                animation_number += 1

                if int((score / fr_score) * 100) >= 65:
                    g = "#cef2db"
                    pygame.mixer.music.load("sounds/win_song.mp3")
                elif int((score / fr_score) * 100) >= 35:
                    g = "#ffd"
                    pygame.mixer.music.load("sounds/medium_song.mp3")
                else:
                    g = "#ffd7d7"
                    pygame.mixer.music.load("sounds/sad_song.mp3")

                game_frame.config(bg=g)

                heading_game_label_end = Label(game_frame, font=("Times New Roman", 30, "bold"), fg=main_fg_color,
                                               text="Quiz game", bg=g)
                heading_game_label_end.place(anchor="center", x=frame_width // 2, y=45)

                if animation_number >= 1:
                    cat_text = category_text[:]
                    cat_text = cat_text.replace("\n", "")

                    category_label = Label(game_frame, text=cat_text, fg="#3c4b5d", bg=g,
                                           font=("Times New Roman", 17))
                    category_label.place(anchor="center", x=frame_width // 2, y=103)

                    result_sound.play()

                if animation_number >= 2:
                    if difficulty_text == "hard":
                        h = "red"
                        w = 5
                    elif difficulty_text == "medium":
                        h = "yellow"
                        w = 8
                    else:
                        h = "#4aff4a"
                        w = 5
                    difficulty_label = Label(game_frame, text=difficulty_text, fg=h, bg="black",
                                             font=("Times New Roman", 20),
                                             width=w)
                    difficulty_label.place(anchor="center", x=frame_width // 2, y=145)

                if animation_number >= 3:
                    final_score_label = Label(game_frame, font=("Times New Roman", 22, "bold"), fg="black", bg=g,
                                              text=f"Your final score: {score}/{fr_score}")
                    final_score_label.place(anchor="center", x=frame_width // 2, y=255)

                if animation_number >= 4:
                    final_percente_label = Label(game_frame, font=("Times New Roman", 30, "bold"), fg=main_fg_color,
                                                 bg=g,
                                                 text=f"{str(int((score / fr_score) * 100))}%")
                    # if len(str(int((score / fr_score) * 100))) == 1:
                    #     final_percente_label.place(anchor="center", x=frame_width // 2 + 5, y=210)
                    # elif len(str(int((score / fr_score) * 100))) == 2:
                    #     final_percente_label.place(anchor="center", x=frame_width // 2 + 10, y=210)
                    # else:
                    #     final_percente_label.place(anchor="center", x=frame_width // 2 + 15, y=210)
                    final_percente_label.place(anchor="center", x=frame_width // 2, y=205)

                    seconds_label = Label(game_frame, font=("Arial", 11), fg="#3c4b5d", bg=g,
                                          text=f"Time: {full_seconds} sec.")
                    seconds_label.place(anchor="center", x=frame_width // 2, y=290)
                    if g == "#ffd7d7" or g == "#ffd":
                        pygame.mixer.music.play(3, 0.0)
                    else:
                        pygame.mixer.music.play(1, 0.0)

                    result_button = Button(game_frame, text="Your answers", fg="white", bg="black", border=0,
                                           borderwidth=0,
                                           font=("Arial", 10, "bold"), cursor="hand2", command=see_results)
                    result_button.place(anchor="ne", x=frame_width - 10, y=10)

                if id == "more" and animation_number < 4:
                    animation_after = window.after(1000, end_of_the_game, "more")

                again_button = Button(game_frame, text="New game", font=("Arial", 15, "bold"), fg="white",
                                      bg="black", command=lambda: again_game(animation_after), border=0, borderwidth=0,
                                      cursor="hand2")
                again_button.place(anchor="e", x=frame_width // 2 - 10, y=340)

                end_the_game_button = Button(game_frame, text="End the game", fg="white", bg="black",
                                             font=("Arial", 15, "bold"), command=window.destroy, border=0,
                                             borderwidth=0,
                                             cursor="hand2")
                end_the_game_button.place(anchor="w", x=frame_width // 2 + 10, y=340)

            def for_animation():
                global animation_after
                animation_after = window.after(1000, end_of_the_game, "more")
                end_of_the_game("one")

            def control_answer(the_button_answer, true_answer, after_id, category_label_info, difficulty_label_info,
                               the_one_question, number_of_questions):
                global score, fr_score, number_question, play_number, incorrect_direction, correct_direction
                game_frame.after_cancel(after_id)
                pygame.mixer.music.stop()
                play_number = 0

                if the_button_answer == "hedidntdoutchanything":
                    label_didnt_touch = Label(game_frame, text="You didn't press any button!", font=("Arial", 12),
                                              fg="red",
                                              bg=bg_frame_color)
                    label_didnt_touch.place(anchor="center", x=frame_width // 2, y=350)

                    incorrect_direction["questions"].append(the_one_question)
                    incorrect_direction["answers"].append(["You didn't press any button".upper(), true_answer])

                elif true_answer == the_button_answer:
                    label_correct = Label(game_frame, text="Correct answer", fg="green", bg=bg_frame_color,
                                          font=("Arial", 12))
                    label_correct.place(anchor="center", x=frame_width // 2, y=360)

                    correct_direction["questions"].append(the_one_question)
                    correct_direction["answers"].append(true_answer)

                    correct_sound.play()

                else:
                    label_incorrect = Label(game_frame, text="Incorrect answer", fg="red", bg=bg_frame_color,
                                            font=("Arial", 12))
                    label_incorrect.place(anchor="center", x=frame_width // 2, y=350)

                    incorrect_direction["questions"].append(the_one_question)
                    incorrect_direction["answers"].append([the_button_answer, true_answer])

                if the_button_answer == "hedidntdoutchanything" or the_button_answer != true_answer:
                    information_about_correct = Label(game_frame, text=f"Correct answer: {true_answer}", fg="grey",
                                                      bg=bg_frame_color, font=("Arial", 11))
                    information_about_correct.place(anchor="center", x=frame_width // 2, y=370)

                    incorrect_sound.play()

                window.update()

                time.sleep(2)

                for widget in game_frame.winfo_children():
                    widget.destroy()
                category_label_info.destroy()
                difficulty_label_info.destroy()
                number_of_questions.destroy()
                score_label = new_score_label()

                fr_score += 1
                if the_button_answer == true_answer:
                    score += 1
                    score_label.config(text=f"{score}/{fr_score}")
                else:
                    score_label.config(text=f"{score}/{fr_score}")

                try:
                    number_question += 1
                    new_question()
                except:
                    for widget in game_frame.winfo_children():
                        widget.destroy()

                    for_animation()

            def counting_seconds(seconds, timer_label, correct, the_questio, category_label_info, difficulty_label_info,
                                 number_of_questions):
                global after_id, play_number, full_seconds
                seconds -= 1
                full_seconds += 1
                if seconds <= 10:
                    timer_label.config(text=seconds, fg="red")
                    if play_number == 0:
                        pygame.mixer.music.play()
                        play_number = 1
                else:
                    timer_label.config(text=seconds)

                if seconds == 0:
                    pygame.mixer.music.stop()
                    play_number = 0
                    control_answer("hedidntdoutchanything", correct, after_id, category_label_info,
                                   difficulty_label_info, the_questio, number_of_questions)

                if seconds > 0:
                    after_id = game_frame.after(1000, counting_seconds, seconds, timer_label, correct, the_questio,
                                                category_label_info, difficulty_label_info, number_of_questions)

            def new_question():
                heading_game_label = Label(game_frame, font=("Times New Roman", 20, "bold"), fg=main_fg_color,
                                           text="Quiz game", bg=bg_frame_color)
                heading_game_label.place(anchor="center", x=frame_width // 2, y=25)

                timer_label = Label(game_frame, font=("Times New Roman", 20, "bold"), fg="black", bg=bg_frame_color,
                                    text=seconds)
                timer_label.place(anchor="nw", x=15, y=10)

                the_question = text["results"][number_question]["question"]
                if "&#039;" in the_question:
                    the_question = the_question.replace("&#039", "")
                if "&quot;" in the_question:
                    the_question = the_question.replace("&quot;", "")
                question_text = Label(game_frame, fg="black", bg=bg_frame_color,
                                      text=the_question, wraplength=480)
                # print(len(the_question))
                if len(the_question) >= 105:
                    question_text.config(font=("Timesd New Roman", 17, "bold"))
                    yy = 50
                else:
                    question_text.config(font=("Times New Roman", 20, "bold"))
                    yy = 70
                question_text.place(anchor="n", x=frame_width // 2, y=yy)

                if difficulty_text == "hard":
                    h = "red"
                    xxx = 507
                elif difficulty_text == "medium":
                    h = "yellow"
                    xxx = 487
                else:
                    h = "#4aff4a"
                    xxx = 507

                difficulty_label_info = Label(window, text=difficulty_text, fg=h, bg="black",
                                              font=("Times New Roman", 12))
                difficulty_label_info.config(text=difficulty_text, fg=h)
                difficulty_label_info.place(anchor="ne", x=540, y=0)

                photo = PhotoImage(file="imgs/restart_game.png")
                restart_button = Button(game_frame, image=photo, bg=bg_frame_color, border=0,
                                        activebackground=bg_frame_color, cursor="hand2",
                                        command=lambda: again_game(after_id))
                restart_button.image = photo
                restart_button.place(anchor="nw", x=65, y=14)

                cat_text = category_text[:]
                cat_text = cat_text.replace("\n", "")

                category_label_info = Label(window, text=f"{cat_text} -", fg="white", bg="black",
                                            font=("Times New Roman", 12))
                category_label_info.place(anchor="ne", x=xxx, y=0)
                w = category_label_info.winfo_reqwidth()

                number_of_questions = Label(window, text=f"{amount_text} q.", fg="black", bg="#bbb",
                                            font=("Times New Roman", 12))
                number_of_questions.place(anchor="ne", x=xxx - w, y=0)

                correct_answer = text["results"][number_question]["correct_answer"]

                all_answers = []
                for num in range(3):
                    h = text["results"][number_question]["incorrect_answers"][num]
                    if "&#039;" in h:
                        h = h.replace("&#039", "")
                    if "&quot;" in the_question:
                        h = h.replace("&quot;", "")
                        print("clear")
                    all_answers.append(h)
                if "&#039;" in correct_answer:
                    correct_answer = correct_answer.replace("&#039", "")
                if "&quot;" in the_question:
                    correct_answer = correct_answer.replace("&quot;", "")
                    print("clear")
                all_answers.append(correct_answer)
                print(correct_answer)

                first_answer_text = ""
                second_answer_text = ""
                third_answer_text = ""
                fourth_answer_text = ""
                a = [first_answer_text, second_answer_text, third_answer_text, fourth_answer_text]

                for num in range(4):
                    a[num] = random.choice(all_answers)
                    all_answers.remove(a[num])

                button_answer_font = ("Times New Roman", 12)
                first_y = 230
                second_y = 300
                first_x = frame_width // 4 + 10
                second_x = frame_width // 1.5 + 40
                width_answer_button = 23
                height_answer_button = 2

                button_answer_1 = Button(game_frame, text=a[0], font=button_answer_font, bg="#a200cc", fg="white",
                                         width=width_answer_button, height=height_answer_button,
                                         command=lambda: control_answer(a[0], correct_answer, after_id,
                                                                        category_label_info,
                                                                        difficulty_label_info, the_question,
                                                                        number_of_questions), cursor="hand2",
                                         wraplength=200)
                # if len(a[0]) > 32:
                #     some = list(a[0])
                #     s1 = ""
                #     for number in range(len(some)):
                #         if number == len(some) // 1.75:
                #             s1 += f"\n{some[number]}"
                #         else:
                #             s1 += some[number]
                #     button_answer_1.config(text=s1)
                if len(a[0]) > 50:
                    # some = list(a[0])
                    # s1 = ""
                    # for number in range(len(some)):
                    #     if number == len(some) // 2:
                    #         if some[number] == " " or some[number-1] == " ":
                    #             s1 += f"\n{some[number]}"
                    #         else:
                    #             s1 += f"-\n{some[number]}"
                    #     else:
                    #         s1 += some[number]
                    # button_answer_1.config(text=s1)
                    button_answer_1.config(height=3)

                button_answer_1.place(anchor="center", x=first_x, y=first_y)

                button_answer_2 = Button(game_frame, text=a[1], font=button_answer_font, bg="#1390f3", fg="white",
                                         width=width_answer_button, height=height_answer_button,
                                         command=lambda: control_answer(a[1], correct_answer, after_id,
                                                                        category_label_info,
                                                                        difficulty_label_info, the_question,
                                                                        number_of_questions), cursor="hand2",
                                         wraplength=200)

                if len(a[1]) > 50:
                    button_answer_2.config(font=("Times New Roman", 10), width=30, height=3)

                button_answer_2.place(anchor="center", x=first_x, y=second_y)

                button_answer_3 = Button(game_frame, text=a[2], font=button_answer_font, bg="#2ba759", fg="white",
                                         width=width_answer_button, height=height_answer_button,
                                         command=lambda: control_answer(a[2], correct_answer, after_id,
                                                                        category_label_info,
                                                                        difficulty_label_info, the_question,
                                                                        number_of_questions), cursor="hand2",
                                         wraplength=200)

                if len(a[2]) > 50:
                    button_answer_3.config(height=3)

                button_answer_3.place(anchor="center", x=second_x, y=first_y)

                button_answer_4 = Button(game_frame, text=a[3], font=button_answer_font, bg="#ff2d2d", fg="white",
                                         width=width_answer_button, height=height_answer_button,
                                         command=lambda: control_answer(a[3], correct_answer, after_id,
                                                                        category_label_info,
                                                                        difficulty_label_info, the_question,
                                                                        number_of_questions), cursor="hand2",
                                         wraplength=200)
                if len(a[3]) > 50:
                    button_answer_4.config(height=3)

                button_answer_4.place(anchor="center", x=second_x, y=second_y)

                # print(f"len 1: {len(a[0])}")
                # print(f"len 2: {len(a[1])}")
                # print(f"len 3: {len(a[2])}")
                # print(f"len 4: {len(a[3])}")

                global after_id

                after_id = game_frame.after(1000, counting_seconds, seconds, timer_label, correct_answer, the_question,
                                            category_label_info, difficulty_label_info, number_of_questions)

            new_question()

            #AAAAAAAAAAAAAAAAAAAAAAAAAANNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
        except:
            error(game_frame)

    else:
        num_not = 0
        def no_inf(num_not, when, no_informations_label):
            num_not += 1
            if num_not <= 2:
                no_informations_label.place(anchor="center", x=frame_width//2, y=333)
                if when == "again":
                    window.after(1000, no_inf, num_not, "again", no_informations_label)
            if num_not == 3:
                no_informations_label.destroy()
        not_type_sound.play()
        no_informations_label = Label(start_frame, text="You haven't entered all the information!", font=("Arial", 10),
                                      fg="red", bg=bg_frame_color)
        window.after(1000, no_inf, num_not, "again", no_informations_label)
        no_inf(num_not, "one", no_informations_label)


def login_game():
    width = 600
    height = 400
    if middle_start:
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = int(screen_width // 2 - width // 2)
        y = int(screen_height // 2 - height // 2 - 75)
    else:
        x = window.winfo_x()
        y = window.winfo_y()
    window.geometry(f"{width}x{height}+{x}+{y}")
    window.resizable(False, False)
    window.iconbitmap("imgs/question_icon.ico")

    bg_photo = PhotoImage(file="imgs/bg_quiz.png")
    Label(window, image=bg_photo, bg="white").place(x=width + 50, y=-5, anchor="ne")

    Label(window, text="Šimon Drápal 18.1.2024", bg="black", fg="white",
          font=("Arial", 7)).place(anchor="ne", x=width-50, y=375)

    bg_frame_color = "white"
    frame_width = 500
    frame_height = 350
    main_fg_color = "#5b0067"
    fg_options = main_fg_color
    font_options_text = ("Times New Roman", 20, "bold")
    font_options = ("Times New Roman", 10)

    start_frame = Frame(window, width=frame_width, height=frame_height, bg=bg_frame_color)
    start_frame.place(x=50, y=25)

    heading_label = Label(start_frame, font=("Times New Roman", 20, "bold"), fg=main_fg_color, text="Quiz game",
                          bg=bg_frame_color)
    heading_label.place(anchor="center", x=frame_width//2, y=25)

    welcome_label = Label(start_frame, font=("Times New Roman", 30, "bold"), fg="black", bg=bg_frame_color,
                          text="Welcome in quiz game!")
    welcome_label.place(anchor="center", x=frame_width//2, y=90)

    ########### options menu ################

    # amount
    amount_label = Label(start_frame, font=font_options_text, fg=fg_options, bg=bg_frame_color, text="amount")
    amount_label.place(anchor="center", x=frame_width//5, y=170)

    amount_string_var = StringVar(start_frame)
    amount_string_var.set("None")
    amount_option_menu = OptionMenu(start_frame, amount_string_var, "5", "10", "15", "20", "30", "40", "60", "80", "100")
    amount_option_menu.config(highlightthickness=0, width=5, height=1, font=font_options)
    amount_option_menu.place(anchor="center", x=frame_width//5, y=220)
    amount_option_menu["state"] = DISABLED

    # category
    category_label = Label(start_frame, font=font_options_text, fg=fg_options, bg=bg_frame_color, text="category")
    category_label.place(anchor="center", x=frame_width//2, y=170)

    # def changeState():
    #     pick = .get()
    #     if (pick == "op2"):
    #         button['state'] = ACTIVE  # means active state
    #         button.config(text="ACTIVE")
    #     else:
    #         button['state'] = DISABLED  # means disabled state
    #         button.config(text="Disabled")

    def new_choose():
        global selected1, selected2, select_text_tru_fal1, select_text_tru_fal2
        if selected1 != category_string_var.get():
            amount_string_var.set("None")
            difficulty_string_var.set("None")
            difficulty_option_menu["state"] = ACTIVE
            amount_option_menu["state"] = DISABLED
            selected1 = category_string_var.get()
            selected2 = ""
            select_text_tru_fal1 = False
            select_text_tru_fal2 = True

    category_string_var = StringVar(start_frame)
    category_string_var.set("None")
    d = ["General \nknowledge", "Film", "Video games", "Computers", "Sports", "Geography", "Celebrities", "Politics", "History", "Animals", "Mathematics", "Television", "Music", "Vehicles", "Cartoon & \nanimations", "Science & \nnature", "Gadgets", "Comics", "Books", "Board Games", "Mythology", "Art", "Anime & \nmanga"]
    category_option_menu = OptionMenu(start_frame, category_string_var, *d, command=lambda _: new_choose())
    category_option_menu.config(highlightthickness=0, font=font_options)
    category_option_menu.place(anchor="center", x=frame_width//2, y=220)

    # difficulty
    difficulty_label = Label(start_frame, font=font_options_text, fg=fg_options, bg=bg_frame_color, text="difficulty")
    difficulty_label.place(anchor="center", x=frame_width//1.25, y=170)

    def new_choose_difficulty():
        global selected2, select_text_tru_fal2

        if selected2 != difficulty_string_var.get():
            with open("files/category_names.txt", "r") as file:
                r = file.read()
                x = ast.literal_eval(r)

            amount_string_var.set("None")
            amount_option_menu["state"] = ACTIVE
            selected2 = difficulty_string_var.get()
            listik_of_amounts = x[selected1][selected2]
            amount_option_menu["menu"].delete(0, "end")
            for option in listik_of_amounts:
                amount_option_menu["menu"].add_command(label=option, command=tk._setit(amount_string_var, option))
            select_text_tru_fal2 = False

    difficulty_string_var = StringVar(start_frame)
    difficulty_string_var.set("None")
    difficulty_option_menu = OptionMenu(start_frame, difficulty_string_var, "easy", "medium", "hard", command=lambda _: new_choose_difficulty())
    difficulty_option_menu.config(highlightthickness=0, width=7, height=1, font=font_options)
    difficulty_option_menu.place(anchor="center", x=frame_width//1.25, y=220)
    difficulty_option_menu["state"] = DISABLED

    # Select
    select_button = Button(start_frame, font=("Times New Roman", 15, "bold"), fg="white", bg=main_fg_color, text="Select",
                           width=10, command=lambda: start_game(frame_width, start_frame, bg_frame_color,
                                                                main_fg_color, amount_string_var, category_string_var,
                                                                difficulty_string_var, frame_height), cursor="hand2")
    select_button.place(x=frame_width//2, y=295, anchor="center")

    l1 = Label(start_frame, font=("Arial", 8), fg="red", bg=bg_frame_color)
    l1.place(anchor="n", x=frame_width // 5, y=240)

    l2 = Label(start_frame, font=("Arial", 8), fg="red", bg=bg_frame_color)
    l2.place(anchor="n", x=frame_width // 1.25, y=240)

    def n(event):
        global select_text_tru_fal1, select_text_tru_fal2
        xm = event.x
        ym = event.y
        # print(f"x={xm}")
        # print(f"y={ym}")
        if xm >= 64 and xm <= 136 and ym >= 206 and ym <= 234:
            if select_text_tru_fal1:
                l1.config(text="Choose category & difficulty")
            elif select_text_tru_fal2:
                l1.config(text="Choose difficulty")
        else:
            l1.config(text="")

        if xm >= 358 and xm <= 442 and ym >= 206 and ym <= 234:
            if select_text_tru_fal1:
                l2.config(text="Choose category")
        else:
            l2.config(text="")

    start_frame.bind("<Motion>", n)

    window.mainloop()

# with open("files/category_names.txt", "w") as file:
#     file.write(str({'General \nknowledge': {'number': 9, "easy": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "medium": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "hard": ["5", "10", "15", "20", "30", "40", "60", "80", "100"]},
#                     'Film': {'number': 11, "easy": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "medium": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "hard": ["10", "15", "20", "25", "30", "35", "40"]},
#                     'Video games': {'number': 15, "easy": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "medium": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "hard": ["5", "10", "15", "20", "30", "40", "60", "80", "100"]},
#                     'Computers': {'number': 18, "easy": ["5", "10", "15", "20", "25", "30"], "medium": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "hard": ["5", "10", "15", "20", "25", "30"]},
#                     'Sports': {'number': 21, "easy": ["5", "10", "15", "20", "25", "30", "35", "40"], "medium": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "hard": ["5", "10", "15", "20"]},
#                     'Geography': {'number': 22, "easy": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "medium": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "hard": ["5", "10", "15", "20", "30", "40", "60", "80", "100"]},
#                     'Celebrities': {'number': 26, "easy": ["5", "10"], "medium": ["5", "10", "15", "20", "25", "30"], "hard": ["5"]}, 'Politics': {'number': 24, "easy": ["5"], "medium": ["5", "10", "15", "20"], "hard": ["5", "10"]},
#                     'History': {'number': 23, "easy": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "medium": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "hard": ["5", "10", "15", "20", "30", "40", "60", "80", "100"]},
#                     'Animals': {'number': 27, "easy": ["5", "10"], "medium": ["5", "10", "15", "20"], "hard": ["5", "10", "15"]}, 'Mathematics': {'number': 19, "easy": ["5"], "medium": ["5", "10", "15"], "hard": ["5", "10", "15"]},
#                     'Television': {'number': 14, "easy": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "medium": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "hard": ["5", "10", "15", "20", "25"]},
#                     'Music': {'number': 12, "easy": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "medium": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "hard": ["5", "10", "15", "20", "30", "40", "60", "80", "100"]},
#                     'Vehicles': {'number': 28, "easy": ["5", "10", "15"], "medium": ["5", "10", "15", "20"], "hard": ["5", "10", "15"]}, 'Cartoon & \nanimations': {'number': 32, "easy": ["5", "10", "15", "20", "25"], "medium": ["5", "10", "15", "20", "25", "30"], "hard": ["5", "10", "15"]},
#                     'Science & \nnature': {'number': 17, "easy": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "medium": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "hard": ["5", "10", "15", "20", "30", "40", "60", "80", "100"]},
#                     'Gadgets': {'number': 30, "easy": ["5", "10"], "medium": ["5"], "hard": ["5"]}, 'Comics': {'number': 29, "easy": ["5", "10"], "medium": ["5", "10", "15", "20", "25", "30"], "hard": ["5", "10", "15"]},
#                     'Books': {'number': 10, "easy": ["5", "10", "15", "20"], "medium": ["5", "10", "15", "20", "25", "30", "35", "40"], "hard": ["5", "10", "15", "20", "25"]}, 'Board Games': {'number': 16, "easy": ["5", "10"], "medium": ["5", "10"], "hard": ["5", "10", "15", "20"]},
#                     'Mythology': {'number': 20, "easy": ["5", "10"], "medium": ["5", "10", "15", "20"], "hard": ["5", "10"]}, 'Art': {'number': 25, "easy": ["5", "10"], "medium": ["5"], "hard": ["5"]},
#                     'Anime & \nmanga': {'number': 31, "easy": ["5", "10", "15", "20", "30", "40", "45"], "medium": ["5", "10", "15", "20", "30", "40", "60", "80", "100"], "hard": ["5", "10", "15", "20", "30", "35"]}}))

login_game()
