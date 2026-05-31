# Templates of Note/Test/Ans

## Note 模板
- `Template__Multi_File_Input__Notes_Summary_Outline_Terms.md`: 此為多份檔案為同一章節時，可以參考的的筆記模板
- `Template__Single_File_Input__Notes_Summary_Outline_Terms.md`: 此為僅輸入一份檔案時，可以參考的的筆記模板

## Test 模板
- `Template__Multi_File_Input__Test.md`: 此為多份檔案為同一章節時，可以參考的的出題模板
- `Template__Single_File_Input__Test.md`: 此為僅輸入一份檔案時，可以參考的的出題模板

## Ans 模板
答案與範圍: 在生成題目時，同時記錄每一題對應的答案與出題範圍  
暫無模板

## review 模板
`Template__Grading_Example.md`: UNDONE_MARK

## Config Example

- `example-vibelearn.config.yaml`：專案層設定檔範例，可由 `scripts/init_project_config.py` 複製到 repo root。這份範例只放專案層設定，不重複 skill 內建模板與腳本路徑。
- `example-style-guidance.md`：專案層風格引導範例。當你不想公開自己的模板，但仍想讓輸出靠近你的筆記/出題習慣時，可先複製這份檔案到專案中再填入。

## Usage Rules

- 模仿模板的考試導向深度與密度，不要逐字複製其章節結構。
- 先依單檔或多檔輸入選模板，再依教材密度調整篇幅。
- 若 `vibelearn.config.yaml` 提供 project-owned 模板覆寫，優先使用 project 模板，再回退到這裡的內建模板。
- 若 `vibelearn.config.yaml` 提供 guidance 檔案，將其視為風格與密度調整的最高優先級參考。
- 若模板語氣偏浮誇，以目前 skill 的內容規則為準。
