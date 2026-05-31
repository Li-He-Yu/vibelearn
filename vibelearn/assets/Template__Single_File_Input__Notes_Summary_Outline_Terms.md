下面是對 **Chapter 5 — The ARM Instruction Set（encoding）** 的考試導向整理（僅依 `chapter5_ARM_instruction_set.pdf` 內容），重點放在：例外（exceptions）、條件執行（conditional execution）、控制流程、SWI、以及各類指令的 assembler syntax 與（能從教材讀到的）binary encoding 欄位。

---

# 1️⃣ Summary（考點總結，5–8 條）

* ARM 指令（ARM state）每條指令都帶 **cond field（bits[31:28]）**，是否執行取決於 CPSR 的 **N/Z/C/V**；`AL` 可省略，`NV=1111` 保留不可用。  
* **Exceptions** 分三類來源（指令直接造成／指令副作用／外部），進入例外時會切 mode、保存 return address 到 `r14_<mode>`、保存 CPSR 到 `SPSR_<mode>`、並跳到對應 vector address（如 SWI=0x08）。  
* **Exception return** 的難點是「恢復 CPSR」與「回到正確 PC」不能分開做；教材給兩種典型作法：`MOVS pc, r14` / `SUBS pc, r14, #imm`（利用 `S` 特殊語意），或 `LDMFD ..., {..,pc}^`（`^` 特殊語意）。  
* **Branch / BL / BX / BLX**：`B{L}{cond} <expr>` 以 PC-relative offset 跳躍（range 約 ±32MB）；`BL` 用 `r14 (lr)` 留 return；`BX/BLX` 提供 ARM/Thumb state 切換機制（BLX 於 v5T 提到）。  
* **SWI（較新 ISA 也稱 SVC）** 的 encoding 為 `cond 1111 imm24`；進入 SVC mode、保存 `r14_svc`/`SPSR_svc`、disable IRQ、PC=0x08；教材也列出 ARM Angel 的 SWI service（WriteC/Write0/Exit…）與一個典型 SWI handler 寫法（保存暫存器、從 `[r14,#-4]` 取回 SWI 指令、mask 取出 SWI number）。  
* **Data processing instructions** 的 encoding 主軸：`cond 00 I opcode S Rn Rd Operand2`；`opcode[24:21]` 對應 AND/EOR/SUB/…/MVN；`S` 控制是否更新 CPSR；Operand2 可為立即數（含 #rot）或移位暫存器（shift by imm / shift by Rs）。  
* **Multiply** 系列在教材以 assembler syntax 與功能表整理：`MUL/MLA`（32-bit result）與 `UMULL/UMLAL/SMULL/SMLAL`（64-bit, RdHi:RdLo）。  
* **Data transfer / status reg / others**：LDR/STR（single word/byte）與 halfword/signed byte 的 encoding 欄位（P/U/B/W/L…）；`SWP`（記憶體與暫存器交換）；`MRS/MSR`（CPSR/SPSR ↔ GPR，含 field mask c/x/s/f）；另外還有 `CLZ`、`BKPT`、unused instruction space、memory faults、ARM variants。

---

# 2️⃣ Outline（章節結構＝老師出題順序）

## (A) Introduction
* ARM 支援的資料型別（byte/half-word/word；signed/unsigned）。
* 32-bit operands（Thumb 例外）；短資料型別主要靠 data transfer 支援。
* Memory organization：little-endian / big-endian（default little-endian）。

## (B) ARM Operating Modes & Registers（含 banked registers）
* CPSR[4:0] mode bits：User/FIQ/IRQ/SVC/Abort/Undef/System。
* 特權 mode 有 `SPSR_<mode>`（進入例外時保存 CPSR）。
* Banked registers：各 mode 的 `sp/lr`（與 FIQ 的額外 banked regs）概念。

## (C) Exceptions（例外）
* Exception groups：指令直接／指令副作用／外部。
* Exception entry：切 mode、保存 `r14_<mode>`、保存 CPSR→SPSR、disable IRQ（FIQ 另外 disable FIQ）、PC 跳 vector。
* Vector addresses：Reset(0x00)、Undef(0x04)、SWI(0x08)、Prefetch abort(0x0C)、Data abort(0x10)、IRQ(0x18)、FIQ(0x1C)；以及 0x14 的歷史說明。
* Exception return：恢復 user registers、恢復 CPSR、回到正確 PC；問題點與 Solution I/II。
* Exception priorities（Reset/Data abort/FIQ/IRQ/Prefetch abort/SWI&Undef）。

## (D) Conditional execution
* cond field（bits[31:28]）與 N/Z/C/V 的對應。
* ARM condition codes 表（EQ/NE/CS(HS)/CC(LO)/MI/PL/VS/VC/HI/LS/GE/LT/GT/LE/AL/NV）。
* Alternative mnemonics：CS vs HS、CC vs LO。
* 範例：`ADDNE r0, r1, r2`。

## (E) Branch / BL / BX / BLX（含 Thumb 切換）
* `B {L} {cond} <expression>`，PC-relative offset，range ±32MB。
* Branch conditions 表（BEQ/BNE/BPL/BMI/BCC/BLO/BCS/BHS/…）。
* `BX|BLX Rm` 與 `BLX label` 的 encoding 概念與用途（切到 Thumb；v5T）。
* GNU GAS `.code 16` / `.code 32`。

## (F) Software Interrupt（SWI / SVC）
* SWI encoding：`cond 1111 imm24`；SWI number 表示功能（ARM Angel 列表）。
* Processor actions for SWI：enter SVC、保存 `r14_svc` / `SPSR_svc`、disable IRQ、PC=0x08。
* SWI handler 範例：`STMF sp!, {r0-r12,r14}`、`LDR r10,[r14,#-4]`、`BIC` 取 imm24、`BL service_routine`、`LDMFD sp!, {r0-r12,pc}^` 返回。

## (G) Data processing instructions（含 encoding）
* Binary encoding：`cond 00 I opcode S Rn Rd Operand2`（含立即數 #rot、shift by imm、shift by Rs）。
* opcode 表（AND/EOR/SUB/RSB/ADD/ADC/SBC/RSC/TST/TEQ/CMP/CMN/ORR/MOV/BIC/MVN）。
* assembler syntax：`<op>{cond}{S} Rd, Rn, #imm` 或 `... Rm, {shift}`；`S` 代表 set condition flags。
* 範例：64-bit addition：`ADDS` + `ADC`。

## (H) Multiply instructions
* assembler syntax：`MUL`、`MLA`、`{mull}`（RdHi:RdLo）。
* 乘法類型表：MUL/MLA/UMULL/UMLAL/SMULL/SMLAL（32-bit vs 64-bit、signed/unsigned、accumulate）。

## (I) Data transfer instructions（含 encoding 與 syntax）
* Single word/unsigned byte：binary encoding 欄位（offset immediate/register + shift，P/U/B/W/L，Rn/Rd）。
* Half-word & signed byte：binary encoding 欄位（P/U/W/L、H/S、Imm[7:4]/Imm[3:0] 或 Rm）。
* LDR/STR assembler syntax：pre-index / post-index / PC-relative form；`B`（byte）、`T`（privileged mode 下用 user view 的 memory translation）。
* Multiple register transfer（LDM/STM）：教材有 binary encoding 圖與 addressing mode names、syntax（本 PDF 的文字擷取無法取得完整 bit 欄位細節）。  
* `SWP{cond}{B} Rd, Rm, [Rn]`。
* MRS/MSR：status register ↔ general register（含 encoding 與 field mask）。

## (J) Coprocessor instructions
* Coprocessor architecture：最多 16 logical coprocessors；每個最多 16 private registers；ARM 負責 control flow。
* 類型：CDP（data operations）、LDC/STC（data transfers，pre/post indexed，N bit 控制長度）、MRC/MCR（register transfers）。
* assembler syntax：`CDP{cond} <CP#>, <Cop1>, CRd, CRn, CRm {,<Cop2>}`；`LDC|STC{cond}{L}...`；`MRC/MCR...`。

## (K) Others
* `CLZ`（v5T）：語法 `CLZ{cond} Rd, Rm` 與其 encoding 欄位。
* `BKPT`（v5T）：debug break；unconditional。
* Unused instruction space、memory faults、ARM architecture variants（表格）。

---

# 3️⃣ 關鍵名詞＋一句話解釋（考試可寫）

| 關鍵名詞 | 一句話定義（可直接寫在考卷上） |
| --- | --- |
| ARM state / Thumb state | ARM state 使用 32-bit 指令；Thumb state 使用較短指令，BX/BLX 可用於狀態切換（教材提到 v5T）。 |
| Endianness | 記憶體位元組序（little-endian / big-endian），影響 half-word/word 的 byte 排列。 |
| CPSR | Current Program Status Register，包含 N/Z/C/V 與 mode bits 等狀態資訊。 |
| SPSR | Saved Program Status Register，特權 mode 進入例外時用來保存舊 CPSR。 |
| Banked registers | 不同 mode 具有「不同實體的暫存器版本」（常見為 sp/lr；FIQ 還有更多 banked regs）。 |
| Exception | 程式執行期間的非一般控制流程事件（如 SWI、abort、IRQ/FIQ），需要切 mode 並跳向量表處理。 |
| Exception vector | 例外入口位址表；每種例外對應固定 vector address（如 SWI=0x08）。 |
| Exception entry | 進入例外時的硬體動作：切 mode、保存 return address、保存 CPSR→SPSR、disable 中斷、PC 跳 vector。 |
| Exception return | 從例外 handler 回到原本流程：恢復 registers/CPSR 並回到正確 PC；教材指出不能把「恢復 CPSR」與「回 PC」拆開做。 |
| `MOVS pc, r14` | 例外返回的一種典型寫法：利用 `S` 的特殊語意同時恢復 CPSR 並跳回 return address（教材 Solution I）。 |
| `SUBS pc, r14, #4/#8` | IRQ/FIQ/abort 等返回常用：回到「被 usurped」指令位置或 retry data abort（教材 Solution I）。 |
| `LDMFD ..., {..,pc}^` | 例外返回另一種典型寫法：`^` 表示特殊形式（教材 Solution II）。 |
| cond field | ARM 指令 bits[31:28]，決定指令是否執行（依 CPSR 的 N/Z/C/V）。 |
| N/Z/C/V | CPSR 的四個條件旗標：Negative/Zero/Carry/oVerflow，用於條件執行與條件分支。 |
| Condition code mnemonic | cond 的助記（EQ/NE/CS/CC/MI/PL/VS/VC/HI/LS/GE/LT/GT/LE/AL），決定何時執行。 |
| CS vs HS（alias） | 同一個 cond：CS 多用於「加法 carry set」語境；HS 多用於「unsigned compare higher-or-same」。 |
| Branch（B/BL） | `B` 做跳躍；`BL` 會把 return address 存到 `r14 (lr)` 以便返回。 |
| PC-relative branch | branch offset 加到 PC 形成目標位址；教材給 range 約 ±32MB。 |
| BX / BLX | branch-and-exchange：對 Rm 或 label 跳躍並可切換 ARM/Thumb state（BLX 於 v5T）。 |
| SWI / SVC | Software Interrupt（較新 ISA 稱 SVC）：以 `cond 1111 imm24` 觸發例外，通常用 imm24 當 service number。 |
| SVC mode | SWI 進入的特權 mode（教材 SWI processor actions：enter supervisor mode）。 |
| SWI handler | 處理 SWI 的例外程式：保存暫存器、解析 SWI number、分派到 service routine，最後返回。 |
| Data processing encoding | 指令格式 `cond 00 I opcode S Rn Rd Operand2`；`opcode` 決定算術/邏輯功能。 |
| `opcode[24:21]` | data processing 的功能碼欄位，對應 AND/EOR/SUB/…/MVN（教材表格）。 |
| `S` bit | data processing 的旗標：是否更新 CPSR 的 N/Z/C/V（教材用 ADDS/ADC 示例）。 |
| Operand2 | data processing 的第二運算元，可為立即數（含 #rot）或移位後暫存器（shift by imm / Rs）。 |
| Multiply / MLA | `MUL` 為乘法；`MLA` 為乘加（multiply-accumulate）：`Rm*Rs+Rn`（32-bit result）。 |
| UMULL / SMULL | long multiply（64-bit result）：unsigned / signed 版本，結果放 `RdHi:RdLo`。 |
| LDR/STR（single transfer） | 單一 word/byte 的 load/store；encoding 含 P/U/B/W/L、Rn/Rd、offset（imm 或 reg+shift）。 |
| P/U/B/W/L bits | single transfer 的控制欄位：pre/post、add/sub offset、byte/word、write-back、load/store。 |
| Pre-index / Post-index | addressing mode：P=1 pre-index（存取前先加 offset），P=0 post-index（存取後再更新 base）。 |
| Write-back | 把更新後位址寫回 base register（教材提到 auto-index / `!`）。 |
| Halfword/signed byte transfer | 支援 half-word 與 signed byte 的 transfer 指令類型；教材給出 H/S 與 split immediate 欄位。 |
| LDM/STM | multiple register transfer；教材給出 syntax 與 addressing mode names（本 PDF 的 encoding 圖文字擷取不足）。 |
| SWP | swap：`SWP Rd, Rm, [Rn]` 交換 memory 與 register；`B` 決定 word/byte。 |
| MRS | move PSR→GPR：`MRS Rd, CPSR|SPSR`。 |
| MSR | move GPR/imm→PSR：可選 CPSR/SPSR 與欄位遮罩（c/x/s/f）。 |
| PSR field mask（c/x/s/f） | MSR 的欄位選擇：control/extension/status/flags（對應 PSR 位元範圍）。 |
| Coprocessor（CP#） | ARM 的硬體擴充機制：最多 16 個邏輯 coprocessors，ARM 仍掌控 control flow。 |
| CDP | coprocessor data operation 指令：在 coprocessor 內做資料運算。 |
| LDC/STC | coprocessor data transfer：ARM 計算位址，coprocessor 控制傳幾個 words；支援 pre/post index。 |
| MRC/MCR | coprocessor register transfer：ARM GPR ↔ coprocessor register（或更新 ARM flags）。 |
| CLZ | Count Leading Zeros（v5T）：計算 Rm 前導 0 的個數，結果寫入 Rd。 |
| BKPT | breakpoint（v5T）：用於軟體除錯，讓處理器進入 debug 流程；教材標示 unconditional。 |
| Unused instruction space | 未使用 opcode 空間；執行時應觸發 undefined instruction trap（教材提到舊 ARM 行為可能不可預測）。 |

---

# 使用提醒（只放策略，不放答案）

* 這份投影片同時考「概念」與「欄位辨識」：看到 encoding 圖，先把 `cond/opcode/S/Rn/Rd/offset` 等欄位對應出來再答語意。  
* Exceptions 題的標準答題順序：**entry 做什麼 → vector address → handler 需要保存什麼 → return 怎麼同時恢復 CPSR+PC**。  
* SWI 題務必能讀懂 handler 範例：為什麼要從 `[r14,#-4]` 取回指令、為什麼要 `BIC ... #0xff000000`。  
* LDR/STR 題先判斷 pre/post index、U=加/減、B=byte/word、W=write-back、L=load/store，再對照 assembler syntax。  
