#!/usr/bin/env python3
"""Generate YuJin Hong Portfolio PDF."""

from fpdf import FPDF

# ── Colors ──────────────────────────────────────────────
BG       = (10, 10, 15)
BG2      = (18, 18, 26)
BG3      = (26, 26, 46)
TEXT     = (228, 228, 231)
TEXT2    = (161, 161, 170)
ACCENT   = (99, 102, 241)
GREEN    = (16, 185, 129)
BORDER   = (39, 39, 42)
WHITE    = (255, 255, 255)
PRIVATE  = (139, 92, 246)

FONT_PATH = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"


class PortfolioPDF(FPDF):
    def __init__(self):
        super().__init__("P", "mm", "A4")
        self.add_font("WQY", "", FONT_PATH)
        self.add_font("WQY", "B", FONT_PATH)
        self.set_auto_page_break(auto=True, margin=20)

    def dark_bg(self):
        self.set_fill_color(*BG)
        self.rect(0, 0, 210, 297, "F")

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font("WQY", "", 8)
        self.set_text_color(*TEXT2)
        self.cell(0, 10, f"YuJin Hong Portfolio  |  Page {self.page_no()}", align="C")

    # ── Helper methods ──

    def section_title(self, number, title):
        self.set_font("WQY", "B", 18)
        self.set_text_color(*ACCENT)
        self.cell(0, 12, f"{number}. {title}", new_x="LMARGIN", new_y="NEXT")
        # accent line
        self.set_draw_color(*ACCENT)
        self.set_line_width(0.8)
        y = self.get_y()
        self.line(self.l_margin, y, self.l_margin + 50, y)
        self.ln(6)

    def body_text(self, text, size=10):
        self.set_font("WQY", "", size)
        self.set_text_color(*TEXT)
        self.multi_cell(0, 6, text)
        self.ln(2)

    def sub_text(self, text, size=9):
        self.set_font("WQY", "", size)
        self.set_text_color(*TEXT2)
        self.multi_cell(0, 5.5, text)
        self.ln(1)

    def tag_row(self, tags):
        x_start = self.get_x()
        y_start = self.get_y()
        x = x_start
        for tag in tags:
            self.set_font("WQY", "", 8)
            w = self.get_string_width(tag) + 8
            if x + w > 210 - self.r_margin:
                x = x_start
                y_start += 7
            self.set_xy(x, y_start)
            self.set_fill_color(*BG3)
            self.set_text_color(*ACCENT)
            self.cell(w, 6, tag, fill=True, align="C")
            x += w + 3
        self.set_xy(x_start, y_start + 8)
        self.ln(2)

    def feature_list(self, items):
        self.set_font("WQY", "", 9)
        self.set_text_color(*TEXT)
        for item in items:
            x0 = self.l_margin + 4
            self.set_x(x0)
            self.cell(5, 5.5, "-")
            self.set_x(x0 + 5)
            w = 210 - self.r_margin - x0 - 5
            if w < 20:
                w = 150
            self.multi_cell(w, 5.5, item)
        self.ln(2)

    def project_card(self, title, subtitle, desc, features, tags, badge=None, links=None):
        # check space
        if self.get_y() > 220:
            self.add_page()
            self.dark_bg()

        y0 = self.get_y()
        # card background
        self.set_fill_color(*BG2)
        self.set_draw_color(*BORDER)
        self.rect(self.l_margin, y0, 210 - self.l_margin - self.r_margin, 4, "F")

        # title row
        self.set_font("WQY", "B", 13)
        self.set_text_color(*WHITE)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")

        # badge
        if badge:
            self.set_font("WQY", "", 8)
            if badge == "Private":
                self.set_text_color(*PRIVATE)
                self.cell(0, 5, f"[{badge}]", new_x="LMARGIN", new_y="NEXT")
            elif badge == "Live":
                self.set_text_color(*GREEN)
                self.cell(0, 5, f"[{badge}]", new_x="LMARGIN", new_y="NEXT")
            else:
                self.set_text_color(*TEXT2)
                self.cell(0, 5, f"[{badge}]", new_x="LMARGIN", new_y="NEXT")

        # subtitle
        self.set_font("WQY", "", 10)
        self.set_text_color(*TEXT2)
        self.cell(0, 6, subtitle, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

        # description
        self.body_text(desc, 9)

        # features
        if features:
            self.set_font("WQY", "B", 9)
            self.set_text_color(*ACCENT)
            self.cell(0, 6, "Key Features:", new_x="LMARGIN", new_y="NEXT")
            self.feature_list(features)

        # tech tags
        self.tag_row(tags)

        # links
        if links:
            self.set_font("WQY", "", 8)
            self.set_text_color(*ACCENT)
            for label, url in links:
                self.cell(0, 5, f"{label}: {url}", new_x="LMARGIN", new_y="NEXT", link=url)
            self.ln(2)

        # separator
        self.set_draw_color(*BORDER)
        self.set_line_width(0.3)
        self.line(self.l_margin, self.get_y(), 210 - self.r_margin, self.get_y())
        self.ln(6)


def build_pdf():
    pdf = PortfolioPDF()

    # ═══════════════ COVER PAGE ═══════════════
    pdf.add_page()
    pdf.dark_bg()

    # centered content
    pdf.ln(60)
    pdf.set_font("WQY", "B", 36)
    pdf.set_text_color(*WHITE)
    pdf.cell(0, 16, "YuJin Hong", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)
    pdf.set_font("WQY", "", 16)
    pdf.set_text_color(*ACCENT)
    pdf.cell(0, 10, "Software Engineer Portfolio", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(8)
    pdf.set_font("WQY", "", 11)
    pdf.set_text_color(*TEXT2)
    pdf.cell(0, 7, "Full-Stack Development  |  AI Applications  |  Robotics", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(20)
    pdf.set_draw_color(*ACCENT)
    pdf.set_line_width(0.8)
    pdf.line(70, pdf.get_y(), 140, pdf.get_y())

    pdf.ln(10)
    pdf.set_font("WQY", "", 10)
    pdf.set_text_color(*TEXT2)
    pdf.cell(0, 6, "github.com/dbwls99706", align="C", new_x="LMARGIN", new_y="NEXT",
             link="https://github.com/dbwls99706")
    pdf.cell(0, 6, "velog.io/@dbwls", align="C", new_x="LMARGIN", new_y="NEXT",
             link="https://velog.io/@dbwls")

    pdf.ln(30)
    pdf.set_font("WQY", "", 8)
    pdf.set_text_color(*TEXT2)
    pdf.cell(0, 5, "February 2026", align="C", new_x="LMARGIN", new_y="NEXT")

    # ═══════════════ ABOUT ═══════════════
    pdf.add_page()
    pdf.dark_bg()

    pdf.section_title("01", "About Me")

    pdf.body_text(
        "소프트웨어 엔지니어로서 AI 애플리케이션, 풀스택 웹 개발, "
        "로보틱스 분야에서 실제 문제를 해결하는 프로젝트를 만들어왔습니다."
    )
    pdf.body_text(
        "카카오톡 기반 가상 주식 투자 게임, OpenAI GPT-4o 기반 자동 일기 앱을 개발하고, "
        "오픈소스 기여를 시각화하는 도구를 만들며, "
        "한국 기술 커뮤니티를 위한 블로그 백업 서비스를 운영하고 있습니다."
    )
    pdf.body_text(
        "ROS2 기반 로봇 시스템과 MATLAB 제어 시뮬레이션까지, "
        "소프트웨어와 하드웨어의 경계를 넘나드는 프로젝트를 수행합니다."
    )

    # stats
    pdf.ln(4)
    stats = [("10+", "Public Repos"), ("4", "Tech Domains"), ("2", "Live Services"), ("8+", "GitHub Stars")]
    x_start = pdf.l_margin
    box_w = (210 - pdf.l_margin - pdf.r_margin) / 4
    y_stat = pdf.get_y()
    for i, (val, label) in enumerate(stats):
        x = x_start + i * box_w
        pdf.set_xy(x, y_stat)
        pdf.set_fill_color(*BG2)
        pdf.rect(x, y_stat, box_w - 3, 18, "F")
        pdf.set_xy(x, y_stat + 2)
        pdf.set_font("WQY", "B", 16)
        pdf.set_text_color(*ACCENT)
        pdf.cell(box_w - 3, 8, val, align="C")
        pdf.set_xy(x, y_stat + 10)
        pdf.set_font("WQY", "", 7)
        pdf.set_text_color(*TEXT2)
        pdf.cell(box_w - 3, 6, label, align="C")
    pdf.set_y(y_stat + 26)

    # ═══════════════ FEATURED PROJECTS ═══════════════
    pdf.ln(8)
    pdf.section_title("02", "Featured Projects")

    # ── Stock King Bot ──
    pdf.project_card(
        title="Stock King Bot",
        subtitle="KakaoTalk Virtual Stock Trading Game",
        desc=(
            "카카오톡에서 즐기는 가상 주식 투자 게임입니다. "
            "한국투자증권 KIS API를 연동하여 실시간 시세를 기반으로 "
            "가상 자금으로 투자하며, 미니게임과 PvP 배틀 기능을 제공합니다."
        ),
        features=[
            "KIS API 연동 실시간 한국 주식 시세 조회 (급등/급락/거래량 TOP)",
            "가상 5,000만원 시작 자금 기반 매수/매도 시뮬레이션",
            "미니게임: 복권, 슬롯머신, 동전던지기, 룰렛, 하이로우",
            "PvP 주가 예측 배틀 및 수익률 기반 랭킹 시스템",
            "한글 단축키 지원 (/ㅅㅅ, /ㅁㅅ, /ㅈㄱ 등 20+개 명령어)",
        ],
        tags=["Python", "FastAPI", "PostgreSQL", "KIS API", "KakaoTalk Bot", "Docker", "Render"],
        badge="Private",
    )

    # ── One Page Today ──
    pdf.project_card(
        title="One Page Today",
        subtitle="AI Auto-Generated Daily Diary from Smartphone Data",
        desc=(
            "스마트폰 사용 흔적으로 자동 생성되는 하루 한 페이지 일기 앱입니다. "
            "OpenAI GPT-4o와 Vision API로 사진과 위치 데이터를 분석하여 "
            "사용자 입력 없이 일기를 자동 작성합니다. "
            "조코딩 x OpenAI x Primer AI 해커톤 2026 출품작."
        ),
        features=[
            "GPS 클러스터링 + 카카오 로컬 API로 체류 장소 및 매장명 자동 감지",
            "OpenAI Vision API로 사진 속 장면을 분석하여 일기에 반영",
            "위치, 사진, 걸음수, 날씨, 캘린더, 앱 사용 패턴 7가지 데이터 자동 수집",
            "Firebase Auth + Firestore 클라우드 동기화, API 키 암호화",
            "사진 x 장소 교차 매칭 알고리즘으로 컨텍스트 기반 서술 생성",
        ],
        tags=["React Native", "Expo", "OpenAI GPT-4o", "Vision API", "Firebase", "SQLite", "Kakao API"],
        badge="Private",
    )

    # ── OpenSource-contribution-card ──
    pdf.project_card(
        title="OpenSource-contribution-card",
        subtitle="Display Your Open-Source Contributions on GitHub Profile",
        desc=(
            "GitHub 프로필 README에 외부 오픈소스 기여를 자동으로 보여주는 도구입니다. "
            "Merged PR을 자동 수집하고, 5가지 테마의 SVG 카드를 생성하며, "
            "GitHub Actions로 매일 자동 업데이트됩니다."
        ),
        features=[
            "Merged PR 자동 수집 (외부 프로젝트 기여만 필터링)",
            "5 themes: Light, Dark, Nord, Dracula, Tokyo",
            "GitHub의 light/dark 모드 자동 감지 및 테마 전환",
            "OSS Score = (Merged PRs x 10) + (Contributing Repos x 20)",
            "Organization 필터링, 기간 설정, PR 라벨 자동 분류",
        ],
        tags=["JavaScript", "GitHub Actions", "SVG Generation", "GitHub API", "CI/CD"],
        badge="6 Stars",
        links=[("GitHub", "https://github.com/dbwls99706/OpenSource-contribution-card")],
    )

    # ── Velog Backup ──
    pdf.project_card(
        title="Velog Backup",
        subtitle="Velog Blog Backup Service",
        desc=(
            "한국의 기술 블로그 플랫폼 Velog의 글과 이미지를 안전하게 백업하는 풀스택 웹 서비스입니다. "
            "GitHub OAuth 로그인, 이메일 알림, ZIP 다운로드 기능을 제공합니다."
        ),
        features=[
            "Frontend: Next.js 14 (Vercel 배포) - SSR 기반 대시보드",
            "Backend: FastAPI (Railway 배포) - 비동기 백업 처리",
            "Database: PostgreSQL (Supabase) - 메타데이터 및 사용자 관리",
            "GitHub OAuth 인증, 이메일 알림, 이미지 포함 ZIP 다운로드",
            "Privacy-first: 사용자별 독립된 백업 데이터 격리",
        ],
        tags=["Python", "FastAPI", "Next.js 14", "PostgreSQL", "Supabase", "Vercel", "Railway", "GitHub OAuth"],
        badge="Live",
        links=[
            ("GitHub", "https://github.com/dbwls99706/Velog_Backup"),
            ("Live Site", "https://velog-backup.vercel.app"),
        ],
    )

    # ═══════════════ OTHER PROJECTS ═══════════════
    if pdf.get_y() > 200:
        pdf.add_page()
        pdf.dark_bg()

    pdf.ln(4)
    pdf.set_font("WQY", "B", 14)
    pdf.set_text_color(*TEXT)
    pdf.cell(0, 10, "Other Projects", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    pdf.project_card(
        title="YOLOv8 on Raspberry Pi 4",
        subtitle="Real-time Object Detection on Edge Device",
        desc=(
            "ROS2 기반 Raspberry Pi 4B에서 YOLOv8 실시간 객체 탐지 패키지. "
            "로봇 기반 전동 휠체어 시스템의 장애물 감지에 활용."
        ),
        features=[],
        tags=["Python", "ROS2", "YOLOv8", "Raspberry Pi", "Edge AI"],
        links=[("GitHub", "https://github.com/dbwls99706/yolov8_on_raspberrypi4")],
    )

    pdf.project_card(
        title="Robotics Control",
        subtitle="MATLAB Robotics Control Simulations",
        desc=(
            "MATLAB 기반 로보틱스 제어 프로젝트 5종. "
            "Lagrangian 동역학, Kalman 필터, PID 제어, 궤적 추적을 1-DOF부터 3-DOF까지 구현."
        ),
        features=[],
        tags=["MATLAB", "Lagrangian", "Kalman Filter", "PID Control", "Trajectory"],
        links=[("GitHub", "https://github.com/dbwls99706/Robotics_Control")],
    )

    # ═══════════════ TECH STACK ═══════════════
    pdf.add_page()
    pdf.dark_bg()

    pdf.section_title("03", "Tech Stack")

    categories = [
        ("Languages", ["Python", "TypeScript", "JavaScript", "MATLAB"]),
        ("AI / ML", ["OpenAI GPT-4o / Vision API", "YOLOv8", "Chatbot Development"]),
        ("Web Development", ["React / React Native", "Next.js", "FastAPI", "Expo"]),
        ("Robotics", ["ROS2", "Raspberry Pi", "Control Systems", "Kalman Filters"]),
        ("DevOps / Infra", ["Docker", "GitHub Actions", "Vercel", "Railway", "Netlify"]),
        ("Database", ["PostgreSQL", "Firebase / Firestore", "Supabase", "SQLite"]),
    ]

    for cat_name, items in categories:
        pdf.set_font("WQY", "B", 11)
        pdf.set_text_color(*WHITE)
        pdf.cell(0, 8, cat_name, new_x="LMARGIN", new_y="NEXT")
        pdf.tag_row(items)
        pdf.ln(1)

    # ═══════════════ CONTACT ═══════════════
    pdf.ln(8)
    pdf.section_title("04", "Contact")

    pdf.body_text("새로운 기회나 협업에 관심이 있습니다. 아래 링크를 통해 연락해주세요.")

    pdf.ln(4)
    pdf.set_font("WQY", "", 11)
    pdf.set_text_color(*ACCENT)
    pdf.cell(0, 7, "GitHub: github.com/dbwls99706", new_x="LMARGIN", new_y="NEXT",
             link="https://github.com/dbwls99706")
    pdf.cell(0, 7, "Velog: velog.io/@dbwls", new_x="LMARGIN", new_y="NEXT",
             link="https://velog.io/@dbwls")

    # ── Save ──
    output_path = "/home/user/AI_portfolio/YuJin_Hong_Portfolio.pdf"
    pdf.output(output_path)
    print(f"PDF generated: {output_path}")


if __name__ == "__main__":
    build_pdf()
