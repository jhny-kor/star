# GitHub Star 목록

[목록 열기](https://jhny-kor.github.io/star/)

jhny-kor의 공개 Star 저장소를 역할·키워드·활용 상황으로 정리한 목록입니다.
검색, 주 용도별 그룹, 키워드 색인, Excel 다운로드를 제공합니다.

한국 시간 매일 오전 9시와 오후 6시에 변경을 확인하고, 변경 시 갱신합니다.
기능 설명은 공개 소개·README 기준이며, 개별 설치·실행 시험 결과가 아닙니다.

## AI 에이전트용 탐색

배포 후 진입점: https://jhny-kor.github.io/star/llms.txt

안내 → 분야 목록 → 관련 분야 → 후보 3~5개 상세 → 공식 README 순서로 읽습니다.
20개 분야의 Markdown·JSON과 저장소별 Markdown은 하나의 `catalog.json`에서 자동 생성합니다.
분류 ID와 설명 근거를 보존하며 확인되지 않은 환경·연결 방식·네트워크·입출력은 null입니다.
수집 시각과 개별 기능 확인 시각은 다릅니다. 실제 실행 검증은 `not_tested`입니다.

```bash
python scripts/search_catalog.py "PDF" --category docs_office --limit 5
python -m unittest discover -s tests -v
python scripts/build_agent_site.py
```

Python 3.10 이상, 추가 패키지 없이 실행합니다. `_site/`가 배포 산출물입니다.
원본 HTML과 JSON이 불일치하거나 내부 링크가 끊기면 빌드가 실패합니다.
원본 HTML의 검색·필터·페이지 이동 스크립트는 유지하고, 배포 시 정적 안내 링크를 주입합니다.
상세 절차는 [agent-guide.md](agent-guide.md)를 참고하세요.

## Pages 배포 연결

1. PR을 main에 병합합니다.
2. Settings → Pages → Build and deployment → Source를 **GitHub Actions**로 설정합니다.
3. Actions → **Agent catalog Pages**에서 Run workflow를 실행합니다.
4. `/star/llms.txt`와 `/star/categories/index.md`에 접근되는지 확인합니다.

워크플로는 PR에서 시험·문서 생성·링크 검증·산출물 업로드를 수행합니다.
main push 또는 수동 실행에서는 통과한 `_site`를 Pages로 게시합니다. PR에서는 게시하지 않습니다.
기존 branch 기반 게시를 계속 사용하면 `_site`가 게시되지 않아 에이전트용 경로가 제공되지 않습니다.
설정 안내: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

기존 Star 수집·설명 생성 프로그램은 이 저장소에 포함되어 있지 않습니다. 기존 갱신을 유지하고
`catalog.json`, `index.html`, Excel을 일관된 상태로 갱신하세요. 그 이후 이 워크플로가 문서를 재생성합니다.
외부 갱신이 PAT/GitHub App으로 push하면 push 이벤트를 사용할 수 있습니다.
다른 Actions의 `GITHUB_TOKEN`으로 push할 경우 후속 push 워크플로가 실행되지 않을 수 있으므로
갱신 작업에서 `workflow_dispatch` 또는 `repository_dispatch`의 `catalog-updated` 이벤트를 호출하세요.
생성 시각을 새로 삽입하지 않아 같은 입력에서 같은 결과가 나옵니다. 깨끗한 산출물을 생성해 삭제된 항목도 제거합니다.

## 조회용 Skill

`skills/star-catalog/`는 별도로 설치할 배포용 Skill입니다. 사이트 게시만으로 에이전트에 등록되지는 않습니다.
해당 폴더를 사용하는 에이전트가 지원하는 Skill 디렉터리에 복사하고 등록 절차를 따르세요.
Skill 미지원 환경은 `agent-guide.md`의 AGENTS.md용 조회 규칙을 작업 대상 프로젝트에 추가하세요.
