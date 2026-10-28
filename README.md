# events-api 起點：松年長照中心跌倒事件紀錄

Git 與自動化 **第 14 節 綜合 Workshop B** 的範本 repo。講義：<https://hackmd.io/c/r12AlLGsfl>

> 林護理長：「夜班如果偵測到有人跌倒，我希望隔天早上能看到一筆紀錄：幾點、哪一台攝影機、哪裡。先不用有 AI，有地方收、收進來的資料是對的就好。」

## 開始

1. 右上角 **Use this template → Create a new repository**，名稱填 `events-api`、選 **Public**
2. 在 VM 裡：

```bash
git clone git@github.com:<你的帳號>/events-api.git
cd events-api
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

一開始會看到 **1 個紅燈**（`test_event_time_without_timezone_rejected`），這是第一個任務。

## 內容

| 路徑 | 用途 |
| --- | --- |
| `app/main.py` | FastAPI：`GET /health`、`POST /events`、`GET /events`（存在記憶體） |
| `tests/test_events.py` | 5 個測試，每個對應一條需求 |
| `requirements.txt` | 與 `devops-ci-demo` 同版本 |

## 卡住了？

| 分支 | 內容 |
| --- | --- |
| `checkpoint/fixed` | 任務 1 完成：時區檢查已補上，5 個測試全綠 |
| `checkpoint/ci` | 任務 2 完成：再加 `.github/workflows/ci.yml` |
| `checkpoint/release` | 任務 3 完成：再加協作規範（PR 範本、CODEOWNERS）與「打 tag 自動發 Release」的 workflow |

建 repo 時勾 **Include all branches** 才會有這些分支。救援方式是「把那個分支的檔案整份拿過來」，不是切過去：

```bash
git fetch origin
git switch -c rescue/ci                 # 在你自己的歷史上開一個 branch
git restore --source=origin/checkpoint/ci --staged --worktree -- .   # 把 checkpoint/ci 的檔案全部拿過來
git status                              # 看到被改／新增的檔案
git commit -m "chore: 從 checkpoint/ci 接續"
```

> 為什麼不直接 `git switch checkpoint/ci`？用範本建出來的 repo，每個分支都是各自獨立的一個 commit，跟你的 `main` 沒有共同祖先，之後開 PR 會出現 `unrelated histories`。

資料都是虛構的。
