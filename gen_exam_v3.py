#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""v3：版式比照段考卷附件，校名：北興國中。輸出 DOCX + PDF + HTML（全繁體）"""
import ast, html as htmlmod

# --- 載入 v2 題庫（避免重打，取字面值不執行） ---
_src = open('gen_exam_v2.py', encoding='utf-8').read()
_tree = ast.parse(_src)
_vals = {}
for _node in _tree.body:
    if isinstance(_node, ast.Assign) and len(_node.targets) == 1 and isinstance(_node.targets[0], ast.Name):
        if _node.targets[0].id in ('QDATA', 'ORIGINAL', 'QTAGS', 'LETTERS'):
            _vals[_node.targets[0].id] = ast.literal_eval(_node.value)
QDATA, ORIGINAL, QTAGS, LETTERS = _vals['QDATA'], _vals['ORIGINAL'], _vals['QTAGS'], _vals['LETTERS']

SCHOOL = '北興國中'
TERM = '115學年度第1學期第1次段考'
GRADE = '七年級國文科試題'
FOOT = '七年級國文科'
BASE = '北興國中_定伯賣鬼_B4雙面考卷40題'

# ================= 1. DOCX =================
from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def style_run(r, size=10, bold=False, color=None):
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.name = '標楷體'
    r._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')
    if color is not None:
        r.font.color.rgb = RGBColor(*color)

def set_page(section, cols=1):
    section.page_width = Mm(257)
    section.page_height = Mm(364)
    section.top_margin = Mm(14)
    section.bottom_margin = Mm(14)
    section.left_margin = Mm(14)
    section.right_margin = Mm(14)
    section.header_distance = Mm(8)
    section.footer_distance = Mm(9)
    sectPr = section._sectPr
    cols_el = sectPr.find(qn('w:cols'))
    if cols_el is None:
        cols_el = OxmlElement('w:cols')
        sectPr.append(cols_el)
    cols_el.set(qn('w:num'), str(cols))
    cols_el.set(qn('w:space'), '850')
    if cols > 1:
        cols_el.set(qn('w:equalWidth'), '1')

def set_footer(section, total_text):
    ft = section.footer
    ft.is_linked_to_previous = False
    p = ft.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run('第'); style_run(r, 9, False)
    r = p.add_run()
    f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'), 'begin'); r._r.append(f1)
    r = p.add_run()
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = 'PAGE'; r._r.append(it)
    r = p.add_run()
    f2 = OxmlElement('w:fldChar'); f2.set(qn('w:fldCharType'), 'end'); r._r.append(f2)
    r = p.add_run('頁，%s【%s】' % (total_text, FOOT)); style_run(r, 9, False)
    for run in p.runs:
        run.font.name = '標楷體'
        run._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')

def add_question(doc, idx, stem, opts, tag):
    star = '★' if idx >= 31 else ''
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.keep_with_next = True
    r = p.add_run('%s%d. %s' % (star, idx, stem))
    style_run(r, 10, False)
    for oi, opt in enumerate(opts):
        po = doc.add_paragraph()
        po.paragraph_format.space_before = Pt(0)
        po.paragraph_format.space_after = Pt(0)
        po.paragraph_format.left_indent = Mm(5)
        r = po.add_run('(%s) %s' % (LETTERS[oi], opt))
        style_run(r, 10, False)

def add_section_head(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text)
    style_run(r, 12, True)

doc = Document()
st = doc.styles['Normal']
st.font.size = Pt(10.5)
st.font.name = '標楷體'
st._element.rPr.rFonts.set(qn('w:eastAsia'), '標楷體')
st.paragraph_format.space_after = Pt(1)
st.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

sec1 = doc.sections[0]
set_page(sec1, cols=1)
set_footer(sec1, '共2頁')

pc = doc.add_paragraph()
r = pc.add_run('科目代碼：01')
style_run(r, 10, False)

t1 = doc.add_paragraph(); t1.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t1.add_run('%s %s' % (SCHOOL, TERM))
style_run(r, 15, True); t1.paragraph_format.space_after = Pt(1)
t2 = doc.add_paragraph(); t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t2.add_run(GRADE)
style_run(r, 16, True); t2.paragraph_format.space_after = Pt(2)

info = doc.add_paragraph(); info.alignment = WD_ALIGN_PARAGRAPH.RIGHT
r = info.add_run('班級：________　姓名：________　座號：________　得分：________')
style_run(r, 10, False)

add_section_head(doc, '一、綜合測驗（1至30題，每題2分，共60分）')

box = doc.add_table(rows=1, cols=1); box.alignment = WD_TABLE_ALIGNMENT.CENTER
cell = box.cell(0, 0); cell.text = ''
p0 = cell.paragraphs[0]
r = p0.add_run('【課文】' + ORIGINAL)
style_run(r, 9, False); p0.paragraph_format.space_after = Pt(1)
tcPr = cell._tc.get_or_add_tcPr()
shd = OxmlElement('w:shd'); shd.set(qn('w:fill'), 'F2F2F2'); shd.set(qn('w:val'), 'clear'); tcPr.append(shd)

doc.add_section(WD_SECTION.CONTINUOUS)
sec2 = doc.sections[1]
set_page(sec2, cols=2)
set_footer(sec2, '共2頁')

for idx, (stem, opts, ans, exp) in enumerate(QDATA, start=1):
    if idx == 31:
        add_section_head(doc, '二、素養閱讀題組（31至40題，每題4分，共40分）')
    add_question(doc, idx, stem, opts, QTAGS[idx - 1])

doc.add_section(WD_SECTION.NEW_PAGE)
sec3 = doc.sections[2]
set_page(sec3, cols=1)
set_footer(sec3, '教師用答案')
ah = doc.add_paragraph(); ah.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = ah.add_run('%s 答案卡與解析（教師用，請另印）' % SCHOOL)
style_run(r, 13, True)
ans_table = doc.add_table(rows=5, cols=8)
ans_table.style = 'Table Grid'
ans_table.alignment = WD_TABLE_ALIGNMENT.CENTER
flat = ['%d.%s' % (i + 1, LETTERS[a]) for i, (s, o, a, e) in enumerate(QDATA)]
k = 0
for rr in range(5):
    for cc in range(8):
        cell = ans_table.cell(rr, cc); cell.text = ''
        p = cell.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(flat[k]); style_run(run, 10, True); k += 1
        p.paragraph_format.space_after = Pt(0)
ap = doc.add_paragraph()
r = ap.add_run('【簡要解析】' + '；'.join(['%d%s%s' % (i + 1, LETTERS[a], e) for i, (s, o, a, e) in enumerate(QDATA)]) + '。')
style_run(r, 8, False)
cp = doc.add_paragraph()
r = cp.add_run('【108課綱對應】學習表現：5-IV-4理解文本、5-IV-5推論評鑑、6-IV-3形音義；核心素養：國-J-A2思辨、國-J-B1符號運用、國-J-C2品德與媒體識讀。素養題31至40對應生活應用與跨域。列印建議：紙張B4直向，窄邊界，雙面翻轉長邊。')
style_run(r, 8, False, color=(0x44, 0x44, 0x44))
doc.core_properties.title = '%s 定伯賣鬼B4考卷' % SCHOOL
docx_path = BASE + '.docx'
doc.save(docx_path)
print('docx saved:', docx_path)

# ================= 2. PDF =================
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

B4 = (257 * mm, 364 * mm)
pdfmetrics.registerFont(TTFont('KaiU', 'C:/Windows/Fonts/kaiu.ttf'))
sCode = ParagraphStyle('c', fontName='KaiU', fontSize=10, leading=13, alignment=0)
sT1 = ParagraphStyle('t1', fontName='KaiU', fontSize=15, leading=19, alignment=1, spaceAfter=2)
sT2 = ParagraphStyle('t2', fontName='KaiU', fontSize=16, leading=20, alignment=1, spaceAfter=4)
sInfo = ParagraphStyle('i', fontName='KaiU', fontSize=10, leading=13, alignment=2, spaceAfter=3)
sHead = ParagraphStyle('h', fontName='KaiU', fontSize=12, leading=15, alignment=0, spaceBefore=6, spaceAfter=3)
sBox = ParagraphStyle('b', fontName='KaiU', fontSize=8, leading=11, alignment=0)
sQ = ParagraphStyle('q', fontName='KaiU', fontSize=9.5, leading=12.5, alignment=0, spaceBefore=3, spaceAfter=1)
sO = ParagraphStyle('o', fontName='KaiU', fontSize=9.5, leading=12.5, alignment=0, leftIndent=14, spaceBefore=0, spaceAfter=0)
sA = ParagraphStyle('a', fontName='KaiU', fontSize=10, leading=13, alignment=1)
sE = ParagraphStyle('e', fontName='KaiU', fontSize=8, leading=11, alignment=0, spaceAfter=4)

pdf_path = BASE + '.pdf'

def footer(canvas, doc_):
    canvas.saveState()
    canvas.setFont('KaiU', 9)
    if doc_.page <= 2:
        txt = '第%d頁，共2頁【%s】' % (doc_.page, FOOT)
    else:
        txt = '教師用答案【%s】' % FOOT
    canvas.drawCentredString(B4[0] / 2, 11 * mm, txt)
    canvas.restoreState()

pdf = SimpleDocTemplate(pdf_path, pagesize=B4, topMargin=13 * mm, bottomMargin=15 * mm,
                        leftMargin=14 * mm, rightMargin=14 * mm, title='%s定伯賣鬼考卷' % SCHOOL)
story = [Paragraph('科目代碼：01', sCode),
         Paragraph('%s %s' % (SCHOOL, TERM), sT1),
         Paragraph(GRADE, sT2),
         Paragraph('班級：________　姓名：________　座號：________　得分：________', sInfo),
         Paragraph('一、綜合測驗（1至30題，每題2分，共60分）', sHead)]
torig = Table([[Paragraph('【課文】' + htmlmod.escape(ORIGINAL), sBox)]], colWidths=[229 * mm])
torig.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F2F2F2')),
                           ('BOX', (0, 0), (-1, -1), 0.5, colors.grey), ('INNERPADDING', (0, 0), (-1, -1), 5)]))
story.append(torig)
avail = 257 * mm - 28 * mm
colW = (avail - 6 * mm) / 2

def qcell(idx, stem, opts, tag):
    star = '★' if idx >= 31 else ''
    t = '<b>%s%d.</b> %s<br/>' % (star, idx, htmlmod.escape(stem))
    for oi, opt in enumerate(opts):
        t += '(%s) %s<br/>' % (LETTERS[oi], htmlmod.escape(opt))
    return Paragraph(t, sQ)

def qtable(qnums):
    rows = []
    for i in range(0, len(qnums), 2):
        cells = []
        for qn_ in qnums[i:i + 2]:
            stem, opts, ans, exp = QDATA[qn_ - 1]
            cells.append(qcell(qn_, stem, opts, QTAGS[qn_ - 1]))
        if len(cells) == 1:
            cells.append(Paragraph('', sQ))
        rows.append(cells)
    tq = Table(rows, colWidths=[colW, colW])
    tq.setStyle(TableStyle([('VALIGN', (0, 0), (-1, -1), 'TOP'), ('LEFTPADDING', (0, 0), (-1, -1), 5),
                            ('RIGHTPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 2)]))
    return tq

story.append(qtable(list(range(1, 31))))
story.append(Paragraph('二、素養閱讀題組（31至40題，每題4分，共40分）標示★，請結合生活經驗與文本推論作答。', sHead))
story.append(qtable(list(range(31, 41))))
story.append(PageBreak())
story.append(Paragraph('%s 答案卡與解析（教師用，請另印）' % SCHOOL, sT2))
flat = ['%d.%s' % (i + 1, LETTERS[a]) for i, (s, o, a, e) in enumerate(QDATA)]
arows = []
for r_ in range(5):
    arows.append([Paragraph('<b>%s</b>' % htmlmod.escape(flat[r_ * 8 + c]), sA) for c in range(8)])
ta = Table(arows, colWidths=[avail / 8] * 8)
ta.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 0.5, colors.grey), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                        ('TOPPADDING', (0, 0), (-1, -1), 3), ('BOTTOMPADDING', (0, 0), (-1, -1), 3)]))
story.append(ta)
story.append(Spacer(1, 3 * mm))
story.append(Paragraph('【簡要解析】' + '；'.join(['%d%s%s' % (i + 1, LETTERS[a], e) for i, (s, o, a, e) in enumerate(QDATA)]) + '。', sE))
story.append(Paragraph('【108課綱對應】學習表現：5-IV-4理解文本、5-IV-5推論評鑑、6-IV-3形音義；核心素養：國-J-A2思辨、國-J-B1符號運用、國-J-C2品德與媒體識讀。', sE))
pdf.build(story, onFirstPage=footer, onLaterPages=footer)
print('pdf saved:', pdf_path)

# ================= 3. HTML =================
html_path = BASE + '.html'
parts = ['<!DOCTYPE html><html lang="zh-Hant-TW"><head><meta charset="utf-8">',
         '<title>%s 定伯賣鬼B4考卷</title>' % SCHOOL,
         '<style>@page{size:B4 portrait;margin:14mm;}body{font-family:"標楷體","KaiU","BiauKai",serif;color:#111;}',
         '.page{max-width:225mm;margin:0 auto;} .code{font-size:15px;} h1{text-align:center;font-size:21px;margin:4px 0;} h2{text-align:center;font-size:23px;margin:4px 0 8px;}',
         '.info{text-align:right;font-size:15px;border-top:1px solid #999;border-bottom:1px solid #999;padding:6px 2px;margin:8px 0;}',
         '.dh{font-size:17px;font-weight:bold;margin:10px 0 4px;} .orig{background:#f2f2f2;border:1px solid #666;padding:8px;font-size:13px;line-height:1.7;}',
         '.cols{column-count:2;column-gap:26px;} .q{break-inside:avoid;padding:5px 0;border-bottom:1px dotted #ccc;} .stem{font-size:15px;} .opts{font-size:15px;padding-left:18px;line-height:1.65;}',
         '.foot{text-align:center;font-size:13px;margin:14px 0;} table.ans{border-collapse:collapse;width:100%;} table.ans td{border:1px solid #666;text-align:center;padding:4px;font-weight:bold;}</style></head><body><div class="page">',
         '<div class="code">科目代碼：01</div><h1>%s %s</h1><h2>%s</h2>' % (SCHOOL, TERM, GRADE),
         '<div class="info">班級：________　姓名：________　座號：________　得分：________</div>',
         '<div class="dh">一、綜合測驗（1至30題，每題2分，共60分）</div>',
         '<div class="orig">【課文】' + htmlmod.escape(ORIGINAL) + '</div><div class="cols">']
for idx, (stem, opts, ans, exp) in enumerate(QDATA, start=1):
    if idx == 31:
        parts.append('</div><div class="dh">二、素養閱讀題組（31至40題，每題4分，共40分）</div><div class="cols">')
    star = '★' if idx >= 31 else ''
    parts.append('<div class="q"><div class="stem">%s%d. %s</div><div class="opts">%s</div></div>' % (
        star, idx, htmlmod.escape(stem),
        '<br>'.join('(%s) %s' % (LETTERS[oi], htmlmod.escape(o)) for oi, o in enumerate(opts))))
parts.append('</div><div class="foot">第1至2頁，共2頁【%s】</div>' % FOOT)
parts.append('<div class="dh">%s 答案卡與解析（教師用）</div><table class="ans">' % SCHOOL)
for r_ in range(5):
    parts.append('<tr>' + ''.join('<td>%d.%s</td>' % (r_ * 8 + c + 1, LETTERS[QDATA[r_ * 8 + c][2]]) for c in range(8)) + '</tr>')
parts.append('</table><ol>')
for idx, (stem, opts, ans, exp) in enumerate(QDATA, start=1):
    parts.append('<li>%s：%s</li>' % (LETTERS[ans], htmlmod.escape(exp)))
parts.append('</ol></div></body></html>')
open(html_path, 'w', encoding='utf-8').write(''.join(parts))
print('html saved:', html_path)
