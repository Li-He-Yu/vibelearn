# scripts

## intro
這個資料夾用來放主流程會直接使用的小工具腳本，避免每次在聊天裡重寫。

## tools
- `config_utils.py`：讀取 project-level `vibelearn.config.yaml` 的小型共用模組，提供 project root 與路徑解析。
- `extract_pdf_to_cache.py`：正式的 PDF 抽取器。寫入 project config 指定的文字快取與 manifest。
- `pdf_to_text.py`：相容舊命令的 wrapper，內部轉呼叫 `extract_pdf_to_cache.py`。
- `md_grader.py`：把批改回寫到指定 markdown（避免 emoji，固定 UTF-8）。
- `init_project_config.py`：把範例設定檔複製成目前專案可用的 `vibelearn.config.yaml`。

## notice
- 這些工具不會修改原始 PDF。
- Windows 終端機若用 cp950 顯示，emoji（✅/❌）容易造成顯示或寫檔混亂；工具預設用 `OK/NG` 標記。
