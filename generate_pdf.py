"""マニュアル.md を PDF に変換するスクリプト"""
import re
from pathlib import Path
from fpdf import FPDF

BASE_DIR = Path(__file__).parent
MD_FILE = BASE_DIR / "マニュアル.md"
PDF_FILE = BASE_DIR / "マニュアル.pdf"

# 日本語フォント
FONT_PATH = r"C:\Windows\Fonts\meiryo.ttc"
FONT_BOLD_PATH = r"C:\Windows\Fonts\meiryob.ttc"


class ManualPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("Meiryo", "", FONT_PATH, uni=True)
        self.add_font("Meiryo", "B", FONT_BOLD_PATH, uni=True)
        self.set_auto_page_break(auto=True, margin=20)

    def header(self):
        if self.page_no() > 1:
            self.set_font("Meiryo", "", 8)
            self.set_text_color(128, 128, 128)
            self.cell(0, 8, "note記事生成システム（Claude Code版） マニュアル", align="R", new_x="LMARGIN", new_y="NEXT")
            self.set_draw_color(200, 200, 200)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Meiryo", "", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"- {self.page_no()} -", align="C")


def parse_markdown(text):
    """Markdown を簡易パースして構造化データにする"""
    lines = text.split("\n")
    blocks = []
    in_code = False
    code_buf = []
    in_table = False
    table_buf = []

    for line in lines:
        # コードブロック
        if line.strip().startswith("```"):
            if in_code:
                blocks.append(("code", "\n".join(code_buf)))
                code_buf = []
                in_code = False
            else:
                # テーブルが途中なら閉じる
                if in_table:
                    blocks.append(("table", table_buf[:]))
                    table_buf = []
                    in_table = False
                in_code = True
            continue
        if in_code:
            code_buf.append(line)
            continue

        # テーブル
        if "|" in line and line.strip().startswith("|"):
            stripped = line.strip()
            # セパレータ行（|---|---|）はスキップ
            if re.match(r"^\|[\s\-:|]+\|$", stripped):
                continue
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if not in_table:
                in_table = True
            table_buf.append(cells)
            continue
        elif in_table:
            blocks.append(("table", table_buf[:]))
            table_buf = []
            in_table = False

        # 見出し
        if line.startswith("# ") and not line.startswith("## "):
            blocks.append(("h1", line[2:].strip()))
        elif line.startswith("## "):
            blocks.append(("h2", line[3:].strip()))
        elif line.startswith("### "):
            blocks.append(("h3", line[4:].strip()))
        elif line.strip() == "---":
            blocks.append(("hr", ""))
        elif line.strip() == "":
            blocks.append(("blank", ""))
        else:
            blocks.append(("text", line))

    if in_table and table_buf:
        blocks.append(("table", table_buf[:]))
    if in_code and code_buf:
        blocks.append(("code", "\n".join(code_buf)))

    return blocks


def render_text_with_bold(pdf, text, font_size=10):
    """**太字** を含むテキストをレンダリング"""
    parts = re.split(r"(\*\*[^*]+\*\*)", text)
    pdf.set_font("Meiryo", "", font_size)
    for part in parts:
        if part.startswith("**") and part.endswith("**"):
            pdf.set_font("Meiryo", "B", font_size)
            pdf.write(6, part[2:-2])
            pdf.set_font("Meiryo", "", font_size)
        elif part.startswith("`") and part.endswith("`"):
            pdf.set_font("Meiryo", "", font_size - 1)
            pdf.set_text_color(180, 40, 40)
            pdf.write(6, part[1:-1])
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Meiryo", "", font_size)
        else:
            # インラインコード処理
            code_parts = re.split(r"(`[^`]+`)", part)
            for cp in code_parts:
                if cp.startswith("`") and cp.endswith("`"):
                    pdf.set_font("Meiryo", "", font_size - 1)
                    pdf.set_text_color(180, 40, 40)
                    pdf.write(6, cp[1:-1])
                    pdf.set_text_color(0, 0, 0)
                    pdf.set_font("Meiryo", "", font_size)
                else:
                    pdf.write(6, cp)
    pdf.ln(6)


def main():
    md_text = MD_FILE.read_text(encoding="utf-8")
    blocks = parse_markdown(md_text)

    pdf = ManualPDF()
    pdf.add_page()

    for btype, content in blocks:
        # ページ残りが少なければ改ページ
        if pdf.get_y() > 265:
            pdf.add_page()

        if btype == "h1":
            pdf.ln(5)
            pdf.set_font("Meiryo", "B", 20)
            pdf.set_text_color(30, 60, 120)
            pdf.multi_cell(0, 12, content)
            pdf.set_draw_color(30, 60, 120)
            pdf.line(10, pdf.get_y() + 2, 200, pdf.get_y() + 2)
            pdf.ln(8)

        elif btype == "h2":
            pdf.ln(6)
            pdf.set_font("Meiryo", "B", 14)
            pdf.set_text_color(40, 80, 150)
            pdf.set_fill_color(235, 242, 255)
            pdf.cell(0, 9, f"  {content}", fill=True, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(4)

        elif btype == "h3":
            pdf.ln(3)
            pdf.set_font("Meiryo", "B", 12)
            pdf.set_text_color(60, 60, 60)
            pdf.cell(0, 8, content, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)

        elif btype == "text":
            pdf.set_text_color(0, 0, 0)
            stripped = content.strip()
            # リスト項目
            if stripped.startswith("- ") or stripped.startswith("* "):
                pdf.set_font("Meiryo", "", 10)
                indent = (len(content) - len(content.lstrip())) * 2 + 5
                pdf.set_x(10 + indent)
                pdf.cell(4, 6, "・")
                render_text_with_bold(pdf, stripped[2:], 10)
            elif re.match(r"^\d+\.\s", stripped):
                pdf.set_font("Meiryo", "", 10)
                num_match = re.match(r"^(\d+\.)\s(.*)", stripped)
                indent = (len(content) - len(content.lstrip())) * 2 + 5
                pdf.set_x(10 + indent)
                pdf.set_font("Meiryo", "B", 10)
                pdf.cell(8, 6, num_match.group(1))
                pdf.set_font("Meiryo", "", 10)
                render_text_with_bold(pdf, num_match.group(2), 10)
            else:
                pdf.set_font("Meiryo", "", 10)
                render_text_with_bold(pdf, stripped, 10)

        elif btype == "code":
            pdf.ln(2)
            pdf.set_fill_color(245, 245, 245)
            pdf.set_draw_color(200, 200, 200)
            pdf.set_font("Meiryo", "", 8)
            pdf.set_text_color(40, 40, 40)

            code_lines = content.split("\n")
            # コードブロックの高さを計算
            block_h = len(code_lines) * 5 + 4
            if pdf.get_y() + block_h > 270:
                pdf.add_page()

            start_y = pdf.get_y()
            for cl in code_lines:
                pdf.set_x(12)
                pdf.cell(186, 5, cl, new_x="LMARGIN", new_y="NEXT")

            end_y = pdf.get_y() + 2
            pdf.rect(11, start_y - 1, 188, end_y - start_y + 1, style="D")
            # 背景を描画（簡易版）
            pdf.set_fill_color(245, 245, 245)
            pdf.ln(4)

        elif btype == "table":
            pdf.ln(2)
            if not content:
                continue
            num_cols = len(content[0])
            col_w = 180 / num_cols

            # ヘッダー行
            pdf.set_font("Meiryo", "B", 9)
            pdf.set_fill_color(50, 80, 140)
            pdf.set_text_color(255, 255, 255)
            for i, cell in enumerate(content[0]):
                pdf.cell(col_w, 7, cell, border=1, fill=True)
            pdf.ln()

            # データ行
            pdf.set_font("Meiryo", "", 9)
            pdf.set_text_color(0, 0, 0)
            for row_idx, row in enumerate(content[1:]):
                if pdf.get_y() > 265:
                    pdf.add_page()
                bg = (245, 248, 255) if row_idx % 2 == 0 else (255, 255, 255)
                pdf.set_fill_color(*bg)
                for cell in row:
                    clean = re.sub(r"`([^`]*)`", r"\1", cell)
                    pdf.cell(col_w, 7, clean, border=1, fill=True)
                pdf.ln()
            pdf.ln(3)

        elif btype == "hr":
            pdf.ln(3)
            pdf.set_draw_color(200, 200, 200)
            pdf.line(10, pdf.get_y(), 200, pdf.get_y())
            pdf.ln(3)

        elif btype == "blank":
            pdf.ln(2)

    pdf.output(str(PDF_FILE))
    print(f"[OK] PDF 生成完了: {PDF_FILE}")


if __name__ == "__main__":
    main()
