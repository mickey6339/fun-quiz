
import json
from pathlib import Path


# 퀴즈 한 문제를 관리하는 클래스
class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = int(answer)

    def display(self):
        print("\n" + self.question)

        for i, choice in enumerate(self.choices, 1):
            print(f"{i}. {choice}")

    def check_answer(self, user_answer):
        return user_answer == self.answer


# 퀴즈 게임 전체를 관리하는 클래스
class QuizGame:
    def __init__(self):
        self.quiz_list = []
        self.best_score = 0
        self.state_file = Path(__file__).with_name("state.json")
        self.load_state()

    # 기본 퀴즈 5개
    def default_quizzes(self):
        return [
            Quiz(
                "Q1. '알잘딱깔센'의 뜻은 무엇일까요?",
                [
                    "알아서 잘 딱 깔끔하고 센스 있게",
                    "알고 보면 잘생겼는데 깔끔한 센스",
                    "알록달록 잘 꾸민 딱 깔끔한 센터",
                    "알면 알수록 잘 딱딱 맞아떨어지는 센스",
                ],
                1,
            ),
            Quiz(
                "Q2. '오운완'의 뜻은 무엇일까요?",
                [
                    "오늘 운동 완전히 망했다",
                    "오늘 운동 완료",
                    "오늘의 운동 왕",
                    "오후 운동 완료",
                ],
                2,
            ),
            Quiz(
                "Q3. '내또출'의 뜻은 무엇일까요?",
                [
                    "내일 또 출발",
                    "내가 또 출력함",
                    "내일 또 출근",
                    "내 마음 또 출렁이네",
                ],
                3,
            ),
            Quiz(
                "Q4. '점메추'의 뜻은 무엇일까요?",
                [
                    "점심 메뉴 추천",
                    "점심 메뉴 추가",
                    "점심 때 메밀국수 추첨",
                    "점심 메이트 추천",
                ],
                1,
            ),
            Quiz(
                "Q5. '완내스'의 뜻은 무엇일까요?",
                [
                    "완전 내 스타일",
                    "완벽한 내비게이션 스타일",
                    "완전 내 스케줄",
                    "완성도 높은 내 스타",
                ],
                1,
            ),
        ]

    # JSON 파일에서 데이터 불러오기
    def load_state(self):
        if not self.state_file.exists():
            self.quiz_list = self.default_quizzes()
            self.save_state()
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.quiz_list = [
                Quiz(item["question"], item["choices"], item["answer"])
                for item in data["quizzes"]
            ]
            self.best_score = data.get("best_score", 0)

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("저장 파일을 읽을 수 없어 기본 퀴즈로 시작합니다.")
            self.quiz_list = self.default_quizzes()
            self.best_score = 0
            self.save_state()

    # JSON 파일에 데이터 저장하기
    def save_state(self):
        data = {
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer,
                }
                for quiz in self.quiz_list
            ],
            "best_score": self.best_score,
        }

        with open(self.state_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    # 메뉴 출력
    def show_menu(self):
        print("\n" + "=" * 45)
        print("       신조어 & 줄임말 퀴즈 게임")
        print("=" * 45)
        print("1. 퀴즈 풀기")
        print("2. 새 퀴즈 추가")
        print("3. 퀴즈 목록 보기")
        print("4. 최고 점수 확인")
        print("5. 종료")
        print("=" * 45)

    # 퀴즈 풀기
    def play_quiz(self):
        if not self.quiz_list:
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0
        total = len(self.quiz_list)

        for quiz in self.quiz_list:
            quiz.display()

            while True:
                user_input = input("정답 번호를 입력하세요 (1~4): ").strip()

                if user_input in ["1", "2", "3", "4"]:
                    break

                print("잘못된 입력입니다. 1~4 사이의 번호를 입력하세요.")

            if quiz.check_answer(int(user_input)):
                print("정답입니다!")
                score += 1
            else:
                print(
                    f"오답입니다! 정답은 {quiz.answer}번 "
                    f"({quiz.choices[quiz.answer - 1]})입니다."
                )

        print("\n" + "=" * 45)
        print(f"퀴즈 종료! 최종 점수: {score} / {total}점")

        if score > self.best_score:
            self.best_score = score
            print("새로운 최고 점수입니다!")

        self.save_state()

    # 새 퀴즈 추가
    def add_quiz(self):
        print("\n[새 퀴즈 추가]")

        question = input("문제를 입력하세요: ").strip()

        if not question:
            print("문제는 비워둘 수 없습니다.")
            return

        choices = []

        for i in range(1, 5):
            while True:
                choice = input(f"{i}번 보기를 입력하세요: ").strip()

                if choice:
                    choices.append(choice)
                    break

                print("보기는 비워둘 수 없습니다.")

        while True:
            answer = input("정답 번호를 입력하세요 (1~4): ").strip()

            if answer in ["1", "2", "3", "4"]:
                break

            print("1~4 사이의 번호를 입력하세요.")

        new_quiz = Quiz(question, choices, int(answer))
        self.quiz_list.append(new_quiz)
        self.save_state()

        print("새 퀴즈가 추가되고 저장되었습니다!")

    # 퀴즈 목록 보기
    def show_quiz_list(self):
        print("\n[등록된 퀴즈 목록]")

        if not self.quiz_list:
            print("등록된 퀴즈가 없습니다.")
            return

        for i, quiz in enumerate(self.quiz_list, 1):
            print(f"{i}. {quiz.question}")

    # 최고 점수 확인
    def show_best_score(self):
        print(f"\n현재 최고 점수: {self.best_score}점")

    # 게임 실행
    def run(self):
        print("신조어 퀴즈 게임에 오신 것을 환영합니다!")

        try:
            while True:
                self.show_menu()
                choice = input("메뉴 번호를 선택하세요: ").strip()

                if choice == "1":
                    self.play_quiz()

                elif choice == "2":
                    self.add_quiz()

                elif choice == "3":
                    self.show_quiz_list()

                elif choice == "4":
                    self.show_best_score()

                elif choice == "5":
                    print("게임을 종료합니다.")
                    break

                else:
                    print("잘못된 입력입니다. 1~5 중에서 선택하세요.")

        except (KeyboardInterrupt, EOFError):
            print("\n프로그램을 안전하게 종료합니다.")

        finally:
            self.save_state()
            print("데이터를 저장했습니다.")


# 프로그램 시작
if __name__ == "__main__":
    game = QuizGame()
    game.run()
