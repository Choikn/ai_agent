# 목표
- 앞전 단계에서 프롬프트->업무수행(llm 호출)를 하나의 에이전트로 가정
- 에이전트를 여러개 만들어서 협업 -> A2A 표현
- 랭체인의 체인단위 구성을 n개 구성하여 서로 상호 다른 작업 진행하도록 구성
- 순차적 협업 패턴 진행
  - 랭체인 완결되는 단위 => 에이전트로 표현
  - 구성 (회차 제한)
    - 신입 개발자 에이전트
    - 전문 리뷰어 에이전트
    - 피드백 반영 에이전트
  - 완성된 코드를 개발

# 구조
```
/
L steps
  L step5_a2a_basic.py
```

# 실행(응답 토큰은 1200으로 제한됨)
```
python -m steps.step5_a2a_basic
---
목표 사용자 비밀번호를 입력받아 DB에 저장하는 간단한 함수 (보안고려)
==================================================

[신입 개발자] 코드 작성 중...
---
 ```python
import bcrypt
import sqlite3

def hash_password(plain_password: str) -> bytes:
    """비밀번호를 salt와 함께 해싱"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode('utf-8') ... 
 (코드 생략) 
 ---

[전문 개발자] 코드 검토 중...
---
 # 코드 리뷰

전반적으로 bcrypt 해싱과 파라미터 바인딩을 사용한 점은 좋습니다만, 실무 배포 관점에서 몇 가지 심각한 문제와 개선점이 있습니다.

## 🔴 심각한 문제

### 1. DB 연결마다 커넥션을 새로 열고 닫음 (비효율)
`save_user_password`와 `verify_password`가 호출될 때마다 `sqlite3.connect()`를 새로 생성합니다. 로그인 요청이 많은 서비스라면 매번 커넥션 오버헤드가 발생합니다.

**개선**: connection pool 또는 컨텍스트 매니저로 관리하거나, 최소한 `with sqlite3.connect(db_path) as conn:` 형태로 리소스 관리를 명확히 하세요.

```python
def save_user_password(username: str, plain_password: str, db_path: str = "users.db") -> None:
    hashed_pw = hash_password(plain_password)
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (...)""")
        try:
            cur.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, hashed_pw)
            )
        except sqlite3.IntegrityError:
            print("이미 존재하는 사용자입니다.")
```

### 2. `CREATE TABLE IF NOT EXISTS`가 매 저장 요청마다 실행됨
테이블 생성은 애플리케이션 초기화 시점에 한 번만 실행해야 합니다. 매 저장마다 실행하는 건 불필요한 오버헤드이며, 스키마 관리 책임이 저장 함수에 섞여 있는 것은 관심사 분리(SRP) 위반입니다.

**개선**: `init_db()` 함수로 분리해서 앱 시작 시 한 번만 호출하세요.

### 3. 예외 처리 시 `print` 사용 → 로깅 부재
`print("이미 존재하는 사용자입니다.")`는 운영 환경에서 로그로 추적되지 않습니다. 또한 이 함수는 호출자에게 성공/실패 여부를 알려주지 않아 상위 로직에서 처리할 수 없습니다.

**개선**:
```python
import logging
logger = logging.getLogger(__name__)

def save_user_password(...) -> bool:
    ...
    try:
        cur.execute(...)
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        logger.warning(f"중복 사용자 등록 시도: {username}")
        return False
```

### 4. `username` 존재 여부와 비밀번호 오류를 구분 불가 (타이밍 공격 여지는 적으나 정보 노출 우려)
현재는 문제없지만, 향후 에러 메시지를 사용자에게 노출할 경우 "존재하지 않는 사용자"와 "비밀번호 오류"를 구분해서 알려주면 계정 존재 여부가 노출(User Enumeration)됩니다. API 응답 설계 시 반드시 통합된 에러 메시지("아이디 또는 비밀번호가 일치하지 않습니다")를 사용하세요. (현재 코드는 bool만 반환하니 당장은 문제 없지 ... 
---

[신입 개발자] 피드백 반영하여 수정 중...
최종 결과물
# 개선된 코드

리뷰 감사합니다! 커넥션 관리, 스키마 초기화 분리, 로깅 적용까지 모두 반영해서 다시 작성했습니다.

```python
import bcrypt
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(db_path: str = "users.db") -> None:
    """앱 시작 시 한 번만 호출하여 테이블을 초기화"""
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash BLOB NOT NULL
            )
        """)
        conn.commit()
    logger.info("DB 초기화 완료: %s", db_path)


def hash_password(plain_password: str) -> bytes:
    """비밀번호를 salt와 함께 해싱"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(plain_password.encode('utf-8'), salt)


def save_user_password(username: str, plain_password: str, db_path: str = "users.db") -> bool:
    """
    사용자 비밀번호를 해싱하여 DB에 저장

    Returns:
        bool: 저장 성공 여부 (username 중복 시 False)
    """
    hashed_pw = hash_password(plain_password)

    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, hashed_pw)
            )
            conn.commit()
        logger.info("사용자 등록 성공: %s", username)
        return True
    except sqlite3.IntegrityError:
        logger.warning("중복 사용자 등록 시도: %s", username)
        return False
    except sqlite3.Error as e:
        logger.error("DB 오류 발생 (save_user_password): %s", e)
        return False


def verify_password(username: str, input_password: str, db_path: str = "users.db") -> bool:
    """
    로그인 시 비밀번호 검증

    주의:
        이 함수는 단순히 True/False만 반환합니다.
        상위 API/서비스 레이어에서는 '존재하지 않는 사용자'와 '비밀번호 오류'를
        구분해서 사용자에게 노출하지 말고, 반드시 통합된 에러 메시지
        (예: "아이디 또는 비밀번호가 일치하지 않습니다")를 사용해야
        User Enumeration을 방지할 수 있습니다.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()
            cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
            row = cur.fetchone()
    except sqlite3.Error as e:
```

