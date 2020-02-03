import lessons, telebot
Token =('936648651:AAGRqcs_gqzqsEb9M-545UaX0L643_wkcQg')
alld = ["Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця"]
bot = telebot.TeleBot('936648651:AAGRqcs_gqzqsEb9M-545UaX0L643_wkcQg')

@bot.message_handler(type=['text'])
def get_lessons_str(group, day):
    group_lessons = lessons.get(group)
    if not group_lessons:
        return None

    lessons_per_day = group_lessons.get(day)
    if not lessons_per_day:
        return None

    lesson_str = f"{day}:\n"
    for lesson in lessons_per_day:
        lesson_str += f"\t{lesson}\n"
    lesson_str += "\n"

    return lesson_str


def lessons(message, group, day):
    a, b = map(int, message.text.split())
    if a in lessons.get(group) and b in lessons.get(day):
        bot.send_message(message.chat.id, get_lessons_str(group=a, day=b))


lessons = {
    "411": {
        "Понеділок": [
            'Фізика',
            'Фізика',
            'Алгебра',
            'Алгебра',
            'Українська література',
            'Українська література',
            'Біологія'
        ],
        "Вівторок": [
            'Геометрія',
            'Геометрія',
            'Біологія',
            'Історія',
            'Українська мова',
            'Українська мова',
            'Історія',
            'Фізкультура'
        ],
        "Середа": [
            'Англійська мова',
            'Англійська мова',
            'Фізика',
            'Фізика',
            'Алгебра',
            'Алгебра',
            'Історія',
            'Історія'
        ],
        "Четвер": [
            'Хімія',
            'Початкова військова підготовка',
            'Алгебра',
            'Алгебра',
            'Фізика',
            'Фізика',
            'Нічого/Хімія'
        ],
        "П'ятниця": [
            'Географія',
            'Російська',
            'Інформатика',
            'Геометрія',
            'Фізкультура',
            'Фізкультура',
            'Зарубіжна література'
        ]
    }
}