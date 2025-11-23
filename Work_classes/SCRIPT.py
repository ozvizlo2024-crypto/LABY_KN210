class MyName:
    """Опис класу / Документація
    """
    total_names = 0  # Class Variable

    def __init__(self, name=None, domain="itcollege.lviv.ua") -> None:
        """Ініціалізація класу
        """
        # Перевірка на Anonymous
        name = name if name is not None else self.anonymous_user().name

        # Перевірка що імʼя містить лише літери
        if not name.isalpha():
            raise ValueError("Ім'я може містити лише літери!")

        # Робимо першу букву великою
        self.name = name.capitalize()

        # Домен можна змінювати
        self.domain = domain

        MyName.total_names += 1
        self.my_id = self.total_names

    @property
    def whoami(self) -> str:
        return f"My name is {self.name}"

    @property
    def my_email(self) -> str:
        return self.create_email()

    def create_email(self) -> str:
        """Можна змінювати домен"""
        return f"{self.name.lower()}@{self.domain}"

    @classmethod
    def anonymous_user(cls):
        return cls("Anonymous")

    @staticmethod
    def say_hello(message="Hello to everyone!") -> str:
        return f"You say: {message}"

    @property
    def full_name(self) -> str:
        return f"User #{self.my_id}: {self.name} ({self.my_email})"

    def name_length(self) -> int:
        """Повертаємо кількість букв у імені"""
        return len(self.name)

    def save_to_file(self, filename="users.txt"):
        """Додаємо інформацію у файл"""
        with open(filename, "a", encoding="utf-8") as f:
            f.write(self.full_name + "\n")


print("Розпочинаємо створювати об'єкти!")

names = ("Bohdan", "Marta", None, "Oleksandr")

all_names = {name: MyName(name) for name in names}

for name, me in all_names.items():
    print(f"""{">*<"*20}
Object: {me}
Attribute: {me.name} / ID: {me.my_id}
Who am I: {me.whoami}
Email: {me.my_email}
Email method call: {me.create_email()}
Static hello: {me.say_hello("Привіт!")}
Class variable: class={MyName.total_names}, object={me.total_names}
Full name: {me.full_name}
Letters in name: {me.name_length()}
{"<*>"*20}""")

print(f"Створено об'єктів: {MyName.total_names}")
