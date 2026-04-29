# DBAdmin Lite (phpMyAdmin-like)

MySQL/MariaDB 대상 웹 DB 관리 도구입니다.

## 포함 기능
- DB/테이블 탐색, 행 조회/추가/수정/삭제
- 사용자 조회/생성/삭제
- Trigger 목록 조회
- Event Scheduler 이벤트 목록 조회
- 세션/프로세스 목록 조회 (`SHOW FULL PROCESSLIST`)
- 글로벌 상태 모니터링 (`SHOW GLOBAL STATUS`)
- SQL 실행기 (읽기 전용 모드 옵션 제공)

## 설정 파일
앱 설정은 `config.py`에서 관리합니다.

환경변수:
- `DATABASE_URL` (기본값: `mysql+pymysql://root:root@127.0.0.1:3306/mysql`)
- `SECRET_KEY`
- `MAX_ROWS`
- `SQL_READONLY=true|false`

## 실행
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
export DATABASE_URL='mysql+pymysql://user:password@host:3306'
flask run --debug
```

접속: `http://127.0.0.1:5000`

## 주의
- 운영 환경에서는 인증/권한 분리, CSRF, SQL 감사로그, 접근제어(IP/VPN), TLS를 반드시 적용하세요.
- SQL 실행기는 강력하므로 최소 권한 DB 계정을 사용하세요.


## 아키텍처 (Clean Architecture)
- `dbadmin/domain`: 순수 도메인 규칙/검증
- `dbadmin/application`: 유스케이스/서비스
- `dbadmin/infrastructure`: DB 게이트웨이(SQLAlchemy 어댑터)
- `dbadmin/interfaces/web`: Flask 앱 구성(팩토리)
- `app.py`: 웹 라우팅/프레젠테이션 진입점
