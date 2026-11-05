
import json
import os
import shutil


class Quiz:
    def __init__(self, question: str, options: list[str], answer: int):
        self.question = question
        self.options = options
        self.answer = answer

    def display(self, idx: int):
        print(f"\n[문제 {idx}] {self.question}")
        for i, opt in enumerate(self.options, 1):
            print(f"  {i}. {opt}")

    def check_answer(self, user_answer: int) -> bool:
        return self.answer == user_answer

    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "choices": self.options,
            "answer": self.answer,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(data["question"], data["choices"], data["answer"])


class QuizGame:
    def __init__(self, state_file="state.json"):
        self.state_file = state_file
        self.backup_file = f"{state_file}.bak"
        self.quizzes: list[Quiz] = []
        self.best_score = 0
        self.load_state()

    def default_quizzes(self) -> list[Quiz]:
        return [
            Quiz(
                "다음 중 '찐텐'의 의미는 무엇일까요?",
                [
                    "억지로 만들어 낸 즐거운 분위기",
                    "진심에서 우러나오는 실제 감정과 텐션",
                    "친구들과 함께하는 단체 모임",
                    "긴장해서 말이 많아지는 상태",
                ],
                2,
            ),
            Quiz(
                "다음 중 '분조카'의 의미는 무엇일까요?",
                [
                    "분위기 좋은 카페",
                    "분식 메뉴를 조합한 카페",
                    "분주하게 돌아가는 카페",
                    "분위기를 조절하는 카페",
                ],
                1,
            ),
            Quiz(
                "다음 중 '별다줄'의 의미는 무엇일까요?",
                [
                    "별처럼 빛나는 줄임말",
                    "별도로 다른 줄을 세우는 것",
                    "별걸 다 줄인다",
                    "별일 없이 다 줄어든다는 뜻",
                ],
                3,
            ),
        ]

    def load_state(self):
        if not os.path.exists(self.state_file):
            print("기본 퀴즈 세트로 초기화합니다.")
            self.quizzes = self.default_quizzes()
            self.best_score = 0
            self.save_state()
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.quizzes = [
                    Quiz.from_dict(q) for q in data.get("quizzes", [])
                ]
                self.best_score = data.get("best_score", 0)

                if not self.quizzes:
                    self.quizzes = self.default_quizzes()

        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            print(f"[경고] 데이터 파일 손상 감지: {e}")

            if os.path.exists(self.backup_file):
                try:
                    shutil.copyfile(self.backup_file, self.state_file)
                    with open(self.state_file, "r", encoding="utf-8") as file:
                        data = json.load(file)
                        self.quizzes = [
                            Quiz.from_dict(q) for q in data.get("quizzes", [])
                        ]
                        self.best_score = data.get("best_score", 0)
                    print("백업 데이터 복구 완료!")
                    return
                except Exception:
                    print("백업 복구 실패.")

            self.quizzes = self.default_quizzes()
            self.best_score = 0
            self.save_state()

    def save_state(self):
        try:
            if os.path.exists(self.state_file):
                shutil.copyfile(self.state_file, self.backup_file)

            payload = {
                "quizzes": [q.to_dict() for q in self.quizzes],
                "best_score": self.best_score,
            }

            with open(self.state_file, "w", encoding="utf-8") as file:
                json.dump(payload, file, ensure_ascii=False, indent=2)

        except OSError as e:
            print(f"[오류] 파일 저장 실패: {e}")

    def play_quiz_set(self, quiz_set: list[Quiz], update_record=True):
        if not quiz_set:
            print("등록된 문제가 없습니다.")
            return

        current_score = 0
        print("\n=== 신조어 퀴즈 시작 ===")

        for idx, quiz in enumerate(quiz_set, 1):
            quiz.display(idx)

            while True:
                user_input = input("정답 번호 입력 (1-4): ").strip()

                if user_input in ["1", "2", "3", "4"]:
                    choice = int(user_input)
                    break

                print("[입력 오류] 1, 2, 3, 4 중 하나를 입력하세요.")

            if quiz.check_answer(choice):
                print(">> 정답입니다! (+1점)")
                current_score += 1
            else:
                print(f">> 오답입니다! 정답은 {quiz.answer}번입니다.")

        print(f"\n최종 결과: {current_score} / {len(quiz_set)}점")

        if update_record:
            if current_score > self.best_score:
                print(f"최고 점수 갱신! ({self.best_score}점 -> {current_score}점)")
                self.best_score = current_score
            else:
                print(f"현재 최고 기록: {self.best_score}점")
            self.save_state()

    def play(self):
        self.play_quiz_set(self.quizzes)

    def add_quiz(self):
        print("\n=== 신규 퀴즈 출제 ===")

        new_quizzes = self.default_quizzes()
        existing_questions = {q.question for q in self.quizzes}
        added_count = 0

        for quiz in new_quizzes:
            if quiz.question not in existing_questions:
                self.quizzes.append(quiz)
                added_count += 1

        if added_count > 0:
            self.save_state()
            print(f"새 퀴즈 {added_count}개를 저장했습니다.")

        print("\n새로운 퀴즈 3문제를 시작합니다!")
        self.play_quiz_set(new_quizzes, update_record=False)

    def show_quizzes(self):
        print("\n=== 등록된 퀴즈 목록 ===")
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"{idx}. {quiz.question} (정답: {quiz.answer}번)")

    def run(self):
        while True:
            print("\n===============================")
            print("  신조어 & 줄임말 퀴즈 게임")
            print("===============================")
            print("1. 퀴즈 풀기")
            print("2. 신규 퀴즈 추가")
            print("3. 전체 퀴즈 목록 보기")
            print("4. 최고 점수 확인")
            print("5. 종료")

            menu = input("메뉴 선택 (1-5): ").strip()

            if menu == "1":
                self.play()
            elif menu == "2":
                self.add_quiz()
            elif menu == "3":
                self.show_quizzes()
            elif menu == "4":
                print(f"\n현재 최고 점수: {self.best_score}점")
            elif menu == "5":
                print("게임을 종료합니다.")
                self.save_state()
                break
            else:
                print("[입력 오류] 1부터 5 사이의 숫자를 입력해 주세요.")


if __name__ == "__main__":
    game = QuizGame()

    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n프로그램 중단. 데이터를 저장합니다.")
        game.save_state()
