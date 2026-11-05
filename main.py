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
                "다음 중 '알잘딱깔센'의 올바른 의미는?",
                [
                    "알아서 잘 딱 깔끔하고 센스있게",
                    "알고 보면 잘생겼는데 딱히 깔끔하지는 않음",
                    "알록달록 잘 꾸민 깔끔한 센스",
                    "알려주지 않아도 잘 찾아가는 센스",
                ],
                1,
            ),
            Quiz(
                "다음 중 '분조카'의 올바른 의미는?",
                [
                    "분기별 조립식 카페트",
                    "분위기 좋은 카페",
                    "분노 조절 카운슬링",
                    "분식 조기 마감 카페",
                ],
                2,
            ),
            Quiz(
                "다음 중 '중꺾마'의 올바른 의미는?",
                [
                    "중간에 꺾이는 마음",
                    "중요한 것은 꺾이지 않는 마음",
                    "중요한 순간에 꺾어 마시는 음료",
                    "중국집에서 꺾어 먹는 마늘탕수육",
                ],
                2,
            ),
        ]

    def load_state(self):
        if not os.path.exists(self.state_file):
            print("기존 데이터 파일이 없어 기본 퀴즈 세트로 초기화합니다.")
            self.quizzes = self.default_quizzes()
            self.best_score = 0
            self.save_state()
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
                self.best_score = data.get("best_score", 0)
                if not self.quizzes:
                    self.quizzes = self.default_quizzes()
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            print(f"[경고] state.json 손상 감지 ({e}).")
            if os.path.exists(self.backup_file):
                print(">> 자동 백업 파일(state.json.bak)에서 복구를 시도합니다.")
                try:
                    shutil.copyfile(self.backup_file, self.state_file)
                    with open(self.state_file, "r", encoding="utf-8") as file:
                        data = json.load(file)
                        self.quizzes = [Quiz.from_dict(q) for q in data.get("quizzes", [])]
                        self.best_score = data.get("best_score", 0)
                    print(">> 백업본 복구 완료!")
                    return
                except Exception:
                    print(">> 백업본 복원 실패. 기본 퀴즈 세트로 초기화합니다.")
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
            print(f"[오류] 파일 저장 실패 (디스크 공간/권한 점검 필요): {e}")

    def play(self):
        if not self.quizzes:
            print("등록된 문제가 없습니다.")
            return

        current_score = 0
        print("\n=== 신조어 퀴즈 시작 ===")

        for idx, quiz in enumerate(self.quizzes, 1):
            quiz.display(idx)
            while True:
                user_input = input("정답 번호 입력 (1-4): ").strip()
                if user_input in ["1", "2", "3", "4"]:
                    choice = int(user_input)
                    break
                print("[입력 오류] 1, 2, 3, 4 중 하나만 입력하세요.")

            if quiz.check_answer(choice):
                print(">> 정답입니다! (+1점)")
                current_score += 1
            else:
                print(f">> 오답입니다! (정답: {quiz.answer}번)")

        print(f"\n최종 결과: {current_score} / {len(self.quizzes)} 점")

        if current_score > self.best_score:
            print(f"🎉 축하합니다! 최고 점수 갱신! ({self.best_score}점 -> {current_score}점)")
            self.best_score = current_score
        else:
            print(f"현재 최고 기록: {self.best_score}점")

        self.save_state()

    def add_quiz(self):
        print("\n--- 신규 퀴즈 추가 ---")
        q = input("문제 질문: ").strip()
        while not q:
            print("질문은 비워둘 수 없습니다.")
            q = input("문제 질문: ").strip()

        opts = []
        for i in range(1, 5):
            opt = input(f"보기 {i}: ").strip()
            while not opt:
                print("보기 내용은 필수입니다.")
                opt = input(f"보기 {i}: ").strip()
            opts.append(opt)

        while True:
            ans = input("정답 번호 (1-4): ").strip()
            if ans in ["1", "2", "3", "4"]:
                ans_int = int(ans)
                break
            print("정답 번호는 1, 2, 3, 4 중 하나여야 합니다.")

        self.quizzes.append(Quiz(q, opts, ans_int))
        self.save_state()
        print(">> 퀴즈가 성공적으로 추가 및 저장되었습니다.")

    def show_quizzes(self):
        print("\n=== 등록된 퀴즈 목록 ===")
        for idx, quiz in enumerate(self.quizzes, 1):
            print(f"{idx}. {quiz.question} (정답: {quiz.answer}번)")

    def run(self):
        while True:
            print("\n===============================")
            print("  신조어 & 줄임말 퀴즈 게임  ")
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
                print("게임을 종료합니다. 상태를 안전하게 저장했습니다.")
                self.save_state()
                break
            else:
                print("[입력 오류] 1부터 5 사이의 숫자를 입력해 주세요.")


if __name__ == "__main__":
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n\n[프로그램 강제 중단 감지] 상태를 안전하게 백업 및 저장하고 종료합니다.")
        game.save_state()