
# 🎯 신조어 & 줄임말 퀴즈 게임 (fun-quiz)

> **Python 3.12 기반 콘솔 인터랙티브 퀴즈 프로그램 & Git 브랜칭 워크플로우 실습 프로젝트**

본 프로젝트는 파이썬 객체 지향 프로그래밍(OOP) 패러다임과 JSON 영속성 관리 및 자동 백업/복구 시스템을 결합하여 개발한 콘솔 퀴즈 게임입니다.  
Git 필수 7대 명령어 실습, 기능별 브랜칭 전략(main - feature), 10회 이상의 커밋 사이클 및 원격 저장소 복제(clone/pull) 라이프사이클을 준수했습니다.

---

## 📌 1. 프로젝트 기획 및 개발 배경

* **선정 주제:** 젊은 세대 신조어 및 줄임말 퀴즈
* **기획 배경:** 모바일 중심 소통에서 확대되는 세대 간 신조어 사용 격차를 줄이고, 학습 효율을 높이기 위해 게임화(Gamification) 요소를 결합했습니다.
* **기본 문제 구성:** 기본 퀴즈 3문항 내장(알잘딱깔센, 분조카, 중꺾마), 신규 퀴즈 동적 추가 기능 지원.

---

## 🛠 2. 개발 환경 및 기술 스택

| 구분 | 적용 기술 / 도구 | 활용 목적 |
| :--- | :--- | :--- |
| **Language** | Python 3.12 | 클래스 기반 객체 지향 프로그래밍, CLI 입출력 |
| **Data Storage** | JSON (state.json, state.json.bak) | 영속성 보존, 2단계 자동 백업 및 예외 복구 |
| **VCS** | Git | 로컬 버전 관리, 10회 이상 커밋, 브랜칭 및 원격 동기화 |
| **Repository** | GitHub (mickey6339/fun-quiz) | 원격 코드 호스팅 및 협업 환경 검증 |
| **Environment** | Windows 11, VS Code, PowerShell | CLI 빌드, 디버깅, 셸 환경 테스트 |
<img width="523" height="280" alt="커밋10개" src="https://github.com/user-attachments/assets/fe6c1eec-b43d-42f9-9949-35ec762191fd" />

---

## 💡 3. 아키텍처 의사결정: 함수형 대비 클래스(OOP) 채택 논리

| 비교 항목 | 단순 함수형 구조 (def 중심) | 객체 지향 구조 (OOP 클래스) - **본 프로젝트 채택** |
| :--- | :--- | :--- |
| **상태 관리** | global 전역 변수 남발로 상태 오염 위험 | QuizGame 인스턴스 내부 속성으로 상태 은닉 및 캡슐화 |
| **데이터 무결성** | 딕셔너리 키(quiz['question']) 오타 위험 노출 | Quiz 클래스로 데이터 필드 타입 강제 및 검증 |
| **확장성** | 문제 유형 추가 시 전역 함수 전체 수정 불가피 | Quiz 클래스를 상속받아 새로운 퀴즈 형태 확장 용이 |
| **유지보수** | 입출력과 데이터 처리가 강하게 결합됨 | 채점(check_answer), 직렬화(to_dict) 단위 테스트 용이 |

---

## 💾 4. 데이터 저장 방식 분석: JSON의 한계와 대안 논의

### 1) JSON 채택 이유
* 직관적인 텍스트 포맷으로 디버깅이 용이하며, 파이썬 표준 라이브러리로 가볍게 동작.
* indent=2 및 ensure_ascii=False 설정을 통해 한글 가독성 확보.

### 2) JSON 방식의 기술적 한계
1. **메모리 및 I/O 병목:** 데이터 1건만 수정되어도 파일 전체를 메모리에 올리고 다시 쓰는 비효율 발생 (대용량 확장 시 부적합).
2. **동시성(Concurrency) 제어 부재:** 여러 프로세스가 동시 접근할 때 파일 락(Lock) 기능이 없어 데이터 유실 위험 존재.
3. **트랜잭션(ACID) 미지원:** 쓰기 작업 도중 프로그램이 강제 중단될 경우 JSON 파일이 깨지는 현상 발생 가능.

### 3) 향후 고도화 방안 (Next Step)
* 데이터 규모가 수천 개 이상으로 커지거나 멀티유저 환경으로 확장될 경우, SQLite나 PostgreSQL 같은 관계형 데이터베이스(RDBMS)로 전환하여 인덱싱 조회 및 ACID 트랜잭션을 보장하도록 설계.

---

## 🛡 5. 데이터 백업 정책 및 무결성 복구 전략

1. **자동 백업 메커니즘 (state.json.bak):**
   * 새로운 상태 저장(save_state) 시 기존 정상 파일을 백업 파일(state.json.bak)로 자동 복제 후 덮어쓰기 수행.
   * <img width="476" height="260" alt="자동파일백업" src="https://github.com/user-attachments/assets/94693d25-053a-4b51-9e35-aaa20869e135" />

2. **손상 시 2단계 복원 워크플로우:**
   * state.json 파일 읽기 오류(JSONDecodeError 등) 감지 시 안내 메시지 출력.
   * 백업본(state.json.bak)이 존재하면 즉시 복원하여 이전 데이터 보존.
   * 백업본마저 없거나 손상되었을 경우 기본 퀴즈 3문항으로 안전 리셋 후 파일 재생성.
3. **비정상 종료 방어:**
   * Ctrl+C(KeyboardInterrupt) 또는 입력 중단(EOFError) 감지 시 save_state()를 호출하여 데이터 손실 방지.

---

## 🌿 6. Git 버전 관리 및 브랜치 실습 내역

| 순서 | 명령어 | 작업 내용 |
| :---: | :--- | :--- |
| **1** | git init | 로컬 Git 저장소 생성 |
| **2** | git add . | 초기 파일 및 .gitignore 등록 |
| **3** | git commit -m "docs: 초기 세팅 및 README 작성" | 초기 기준선 설정 |
| **4** | git checkout -b feature/quiz-core | 기능 개발 전용 브랜치 분기 |
| **5** | git commit -m "feat: 퀴즈 로직 및 상태 저장 구현" | 핵심 로직 커밋 |
| **6** | git checkout main & git merge | main 브랜치로 병합 (Fast-forward) |
| **7** | git remote add & git push | GitHub 원격 동기화 |
| **8** | git commit -m "feat: 자동 백업 및 예외 복구 탑재" | 데이터 안정성 로직 반영 |
| **9** | git commit -m "docs: 클래스 채택 논리 및 JSON 한계 분석 추가" | 아키텍처 문서 고도화 |
| **10** | git commit -m "test: clone 및 pull 워크플로우 검증" | 복제 및 동기화 사이클 검증 |
| **11** | git commit -m "docs: 실행 로그 및 최종 제출본 완성" | 커밋 10회 이상 완결 |

---

## 📷 7. 실행 및 실습 검증 증빙 (Execution Logs)
### 1) 프로그램 실행 및 입력 예외 처리 로그 (평가 항목 #1, #2 증빙)
<img width="511" height="806" alt="menu_list_score_exit" src="https://github.com/user-attachments/assets/131215d4-434b-4123-b688-6eb5d106caa8" />
<img width="574" height="697" alt="score" src="https://github.com/user-attachments/assets/44b43607-a1be-41da-8b8f-3cb8f22e317b" />

---

---

## 🚀 8. 실행 가이드 (Quick Start)

### 1) 프로그램 실행 명령어
터미널 환경에 맞춰 아래 명령어 중 하나를 실행합니다.

* 기본 실행 명령어: python main.py
* 환경 변수 미등록 PC 실행 명령어: & "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe" main.py

### 2) 조작 메뉴 안내
* 1번: 퀴즈 풀기 (4지선다 객관식 번호 입력)
* 2번: 신규 퀴즈 등록
* 3번: 전체 퀴즈 목록 조회
* 4번: 현재 최고 점수 확인
* 5번: 데이터 저장 및 안전 종료

---

## 📋 9. state.json 스키마 설계 및 중첩 구조 채택 사유 (평가 항목 #17 보완)

### 1) 필드별 역할 및 정의
| 필드명 | 데이터 타입 | 설명 및 역할 |
| :--- | :---: | :--- |
| quizzes | List[Dict] | 전체 퀴즈 목록을 순서대로 관리하는 최상위 배열 컨테이너 |
| quizzes[].question | String | 사용자에게 화면으로 출력할 퀴즈 문항 텍스트 |
| quizzes[].choices | List[String] | 4지선다 객관식 선택지 보기 목록 (1번~4번 매핑) |
| quizzes[].answer | Integer | 실제 정답 번호 (1~4 범위의 정수값, 인덱스 판정 기준) |
| high_score | Integer | 플레이어가 달성한 역대 최고 점수 기록 보존 |

### 2) 계층형 중첩 구조(Nested Structure) 채택 사유
1. **문제 단위의 원자성(Atomicity) 확보:** 하나의 퀴즈를 구성하는 '질문-보기 목록-정답'을 단일 객체(Dict)로 묶어 관리함으로써, 배열 정렬이나 신규 문제 추가/삭제 시 데이터 간의 참조 불일치를 원천 차단합니다.
2. **객체-도메인 매핑 일치:** Quiz 클래스의 속성(question, options, answer)과 1:1로 정확히 직렬화(to_dict) 및 역직렬화(from_dict)가 이루어지도록 설계하여 파싱 로직의 복잡도를 낮췄습니다.
3. **메타데이터 분리 독립성:** 퀴즈 목록(quizzes)과 전역 상태 데이터(high_score)를 동격의 루트 키로 분리 배치하여, 향후 '플레이어 프로필', '누적 플레이 횟수' 등 추가 메타데이터가 늘어나도 기존 퀴즈 구조를 변경하지 않고 유연하게 확장 가능합니다.

---

## 🔍 10. 요구사항 변경 시 영향도 분석 (Change Impact Analysis) (평가 항목 #20 보완)

프로그램의 기능 추가 및 요구사항 수정 시, 영향받는 파일과 관련 메서드의 의존성 매핑 목록입니다.

| 변경 요구사항 시나리오 | 수정 대상 파일 | 영향받는 클래스 및 메서드 | 구체적 영향도 및 수정 내용 |
| :--- | :--- | :--- | :--- |
| **선택지 문항 수 변경 (예: 4지선다 ➔ 5지선다 또는 O/X)** | main.py | Quiz.__init__, Quiz.check_answer<br>QuizGame.add_quiz, QuizGame.play | • 입력값 유효 범위 검증 조건 수정 (1~4 ➔ 1~5 또는 1~2)<br>• 선택지 출력 반복문 및 안내 문구 템플릿 변경 |
| **저장 스키마 확장 (예: 퀴즈별 해설, 난이도 필드 추가)** | main.py<br>state.json | Quiz.__init__, Quiz.to_dict<br>QuizGame.load_state, QuizGame.add_quiz | • Quiz 클래스 생성자 및 딕셔너리 직렬화/역직렬화 필드 추가<br>• 퀴즈 등록 메서드(add_quiz)에 난이도/해설 입력 프롬프트 반영 |
| **점수 시스템 개편 (예: 문항별 배점 차등화, 감점제 도입)** | main.py | Quiz.__init__, Quiz.to_dict<br>QuizGame.play, QuizGame.save_state | • Quiz 모델에 배점(points) 속성 추가<br>• play() 루프 내 점수 누적 연산식 및 최고 점수(high_score) 갱신 로직 수정 |
| **데이터 저장소 전환 (JSON ➔ SQLite / DB 도입)** | main.py<br>(신규 DB 파일) | QuizGame.load_state, QuizGame.save_state<br>QuizGame.__init__ | • JSON 파일 I/O 로직을 SQL 쿼리(INSERT, SELECT)로 전면 교체<br>• 백업 복구 메커니즘을 DB 트랜잭션(Commit/Rollback) 방식으로 전환 |
