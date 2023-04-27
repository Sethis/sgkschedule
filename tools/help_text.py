

class HelpText:
    value: tuple[dict[str, str], ...] = (
        {
            "id": "AgACAgIAAxkBAAIcw2RJXE9iE9b8OnTDAVc8vcp6Q7u_AAKmyTEb08xIShGtkdPSldoLAQADAgADeQADLwQ",
            "text": "Как-то грустно. Всё такое... Незаданное... <b>Исправим? Жмакай вперёд</b>"
        },
        {
            "id": "AgACAgIAAxkBAAIcxGRJXF1mH10bQ0GRyNqBRFnqRFOVAAKnyTEb08xISnFV1OhlpdfsAQADAgADeQADLwQ",
            "text": "Вообще, я тебе советую сначала быстренько посмотреть весь туториал, запомнить "
                    "все действия и повторить самому уже после просмотра. "
                    "Так вот, первым делом <b>тык на настройки</b>"
        },
        {
            "id": "AgACAgIAAxkBAAIcxWRJXHLNhTKeJTSIK6k9ha70w2OYAAKpyTEb08xISmFN5Hik2FDTAQADAgADeQADLwQ",
            "text": "Тут куча столбцов всяких. Но нам сейчас нужна именно вторая колонка"
        },
        {
          "id": "AgACAgIAAxkBAAIcxmRJXISuPdSgadMmf9n1YtChYIjMAAK0yTEb08xISj9Hrqbl-v2XAQADAgADeQADLwQ",
          "text": "Думаю, стоит начать по порядку, то есть с заполнения кабинета"
        },
        {
            "id": "AgACAgIAAxkBAAIcx2RJXJNYoHwG_b09nc3zyf21Gp4fAAK2yTEb08xISqHJAZTvB5TvAQADAgADeQADLwQ",
            "text": "Тут появится такой текст. На него просто отвечаем номером любого кабинета, "
                    "где ты чаще всего бываешь. У меня это 539, там рядом даже диванчик недавно поставили...."
        },
        {
            "id": "AgACAgIAAxkBAAIc3mRJYatXlrwkqmqhK_-8YjjiNSpMAALxyTEb08xISh__RRWgeJf_AQADAgADeQADLwQ",
            "text": "Вот так. У нас всё получилось! Мы с тобой такие молодцы.."
        },
        {
            "id": "AgACAgIAAxkBAAIcyWRJXLgVPCRpVR_LhRtyclJlGXupAAK5yTEb08xISsMV4k0hJW9uAQADAgADeQADLwQ",
            "text": "Теперь давай заполним педагога. Здесь можно указать своего куратора или себя самого, "
                    "если вы преподаватель, конечно"
        },
        {
            "id": "AgACAgIAAxkBAAIcymRJXMXTRqpFwgMRzgABcGqu8v9IWQACuskxG9PMSEp8RYLT6P_8uAEAAwIAA3kAAy8E",
            "text": "Опять ввести что-то просят. Но мы не пугаемся и вводим фамилию. Можно добавить и имя, "
                    "если фамилия очень уж популярная"
        },
        {
            "id": "AgACAgIAAxkBAAIcy2RJXN327KMgMs7HwGeGjID_M9cjAAK_yTEb08xISrirAAHvEE3RVgEAAwIAA3kAAy8E",
            "text": "К счастью, это не мой случай и мне хватило только фамилии"
        },
        {
            "id": "AgACAgIAAxkBAAIc4WRJYgSej_q_05bjJ34DhXoTm5zpAALzyTEb08xISgL5--VHcATAAQADAgADeQADLwQ",
            "text": "Кстати, мы уже всё заполнили! Опять же, мы такие молодцы.."
        },
        {
            "id": "AgACAgIAAxkBAAIcz2RJXVeqyMcdGO9ZeZd8-Nw8iOgiAALEyTEb08xISrNmKup1yw8TAQADAgADeQADLwQ",
            "text": "Так.. Как там бот называется.. Точно, расписание! Давай по группе посмотрим"
        },
        {
          "id": "AgACAgIAAxkBAAIc0GRJXWVka1VjRpkxSh7OffnHECqxAALFyTEb08xISomH__BgGQ0tAQADAgADeQADLwQ",
          "text": "Помогите."
        }
        ,
        {
            "id": "AgACAgIAAxkBAAIc0WRJXXe-t3ye0-x_mf70UEaShTH9AALGyTEb08xISnUNTe0HrZ2NAQADAgADeQADLwQ",
            "text": "Так, мне срочно нужно вспомнить хорошие времена."
        }
        ,
        {
            "id": "AgACAgIAAxkBAAIc0mRJXYW8WgtX6bUab1m0TqskEhWsAALJyTEb08xISvuy27pxzjRdAQADAgADeQADLwQ",
            "text": "Воу. Тут целый календарь! А мне так его не хватало.. Теперь буду пользоваться ботом "
                    "как минимум из-за такого суперского календаря.."
        }
        ,
        {
            "id": "AgACAgIAAxkBAAIc02RJXY-un_jLh9plMWWCKqSL_nMfAALKyTEb08xISgV_tupHo0jHAQADAgADeQADLwQ",
            "text": "Так, а это что за кнопочка такая?"
        }
        ,
        {
            "id": "AgACAgIAAxkBAAIc1GRJXZsbkscVPfm1cgdVwJoUIaG_AALMyTEb08xISuKtoSoud0I7AQADAgADeQADLwQ",
            "text": "Ура, он даже листается. Вау. Какой он классный!!\n\n"
                    "<span class='tg-spoiler'>(он потратил на него слишком много времени. "
                    "Просто поддержи его. Скажи что календарик классный)</span>"
        }
        ,
        {
            "id": "AgACAgIAAxkBAAIc1WRJXbSjPDSjTfdsiXv3hH0zNgLbAALOyTEb08xISq9eN_gg7_8lAQADAgADeQADLwQ",
            "text": "А если сюда жмакнуть.."
        }
        ,
        {
            "id": "AgACAgIAAxkBAAIc1mRJXc-gW0wGzV7LTnJMMEPfHPcJAALPyTEb08xISsUjPKsjBWRbAQADAgADeQADLwQ",
            "text": "Работает!!"
        }
        ,
        {
            "id": "AgACAgIAAxkBAAIc12RJXeBUJCFVAfIaWZgbMiWQxmJhAALQyTEb08xISjNLOEgJSCIPAQADAgADeQADLwQ",
            "text": "Так, а что у меня будет через год?"
        }
        ,
        {
            "id": "AgACAgIAAxkBAAIc2GRJXe0lVE8d46-G_GfQduVa0QABwwAC0ckxG9PMSEr4w9SIWJRUxQEAAwIAA3kAAy8E",
            "text": "Опять что-то ввести просят. Ладно, я введу, но это последний раз"
        }
        ,
        {
            "id": "AgACAgIAAxkBAAIc2WRJXgABiyN7J-9e_B7z7MFfdi0S5AAC0skxG9PMSEqt7KBkGk5EQQEAAwIAA3kAAy8E",
            "text": "Второкурсовое..."
        },
        {
            "id": "AgACAgIAAxkBAAIc2mRJXiTe9N-qLjZ-6fuicpeYW4sBAALTyTEb08xISl3vIu2If_DwAQADAgADeQADLwQ",
            "text": "А у педагогов там как дела?"
        },
        {
            "id": "AgACAgIAAxkBAAIc22RJXlM7nJEIfK8zDTVcjoG3RsPlAALUyTEb08xISp4rpEn1igI_AQADAgADeQADLwQ",
            "text": "Жестб."
        }
        )

help_text = HelpText