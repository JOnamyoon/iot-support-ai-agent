# GitHub 제출 방법 (10분 버전)

1. GitHub에서 **New repository** → 이름 `iyuno-agent-portfolio` → **Public** → Create repository.
2. 이 폴더 전체를 업로드하거나 Git을 사용합니다.

```bash
git init
git add .
git commit -m "Build job-posting evidence AI agent"
git branch -M main
git remote add origin https://github.com/YOUR_ID/iyuno-agent-portfolio.git
git push -u origin main
```

3. GitHub의 **Actions** 탭에서 CI가 초록색인지 확인합니다.
4. README 맨 위에 본인의 GitHub Actions badge를 추가합니다.
5. `streamlit run src/app.py` 실행 후 화면을 1~2분 녹화합니다.
6. README에 데모 영상 링크 또는 GIF를 추가합니다.
7. PowerPoint의 `[GitHub URL 입력]`, `[이름/학번 입력]` 부분만 수정합니다.

## 제출 전 체크
- [ ] Public repository URL
- [ ] README 요구사항 매핑
- [ ] RAG + citation + tool calling 데모
- [ ] 30-question evaluation / metrics.json
- [ ] pytest 5 tests / GitHub Actions CI
- [ ] data sources / access date / notes
- [ ] 2-minute demo or GIF
- [ ] final reflection
- [ ] PPT에 GitHub URL, 이름, 학번 입력
