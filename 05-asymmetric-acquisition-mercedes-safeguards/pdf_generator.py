import io
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute and draw total page numbers and institutional footers.
    """
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "GLOBAL EV MARKET INTELLIGENCE SUITE | EXECUTIVE BOARD BRIEFING")
            self.drawRightString(558, 750, "CONFIDENTIAL / BOARD USE ONLY")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Footer (all pages)
        self.setFont("Helvetica", 8)
        self.drawString(54, 36, f"Generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')} | German Auto Triad Safeguard Suite")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_str)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        self.restoreState()


def generate_board_briefing_pdf(sim_data: dict) -> io.BytesIO:
    """
    Generates a high-resolution, institutional-grade Executive Board Briefing Dossier (PDF).
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Hierarchy
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=12
    )
    section_h1 = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#334155')
    )
    body_bold = ParagraphStyle(
        'BodyBoldDark',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#0F172A')
    )
    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#0F172A')
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor('#1E293B')
    )
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    story = []

    # 1. Header Banner & Title
    badge_data = [[
        Paragraph("<font color='#BE123C'><b>POLICY BRIEFING &amp; DECISION DOSSIER</b></font>", body_bold),
        Paragraph("<font color='#047857'><b>STATUS: ACTION REQUIRED</b></font>", body_bold)
    ]]
    badge_table = Table(badge_data, colWidths=[250, 254])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#FFE4E6')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#D1FAE5')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ]))
    story.append(badge_table)
    story.append(Paragraph("The German Auto Triad's China Trap", title_style))
    story.append(Paragraph("Asymmetric IDAR Absorption, Governance Vulnerabilities (AktG §179) &amp; The Phased De-risking Playbook (2019–2035)", subtitle_style))

    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0F172A'), spaceAfter=10))

    # 2. Executive Problem Statement Callout
    exec_summary_text = (
        "<b>Executive Problem Statement:</b> Between 2019 and 2025, the German Auto Triad (Mercedes-Benz, BMW, VW) experienced a "
        "<b>-28.1% delivery collapse (-1.59M units)</b> and a <b>-48.0% drop in Chinese EBIT contributions</b> due to Chinese state-capitalist "
        "IDAR absorption and outbound statutory lock-in. With €45.0B in cumulative sunk CapEx and 89.2% local production lock-in, immediate decoupling "
        "is unviable. This dossier details the <b>Phased De-risking (Scenario B)</b> path to restore board autonomy and technological sovereignty."
    )
    exec_box = Table([[Paragraph(exec_summary_text, callout_style)]], colWidths=[504])
    exec_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94A3B8')),
        ('LINELEFT', (0,0), (0,-1), 4, colors.HexColor('#0284C7')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(exec_box)
    story.append(Spacer(1, 10))

    # 3. Live Parametric Simulation Results (4 KPI Cards)
    story.append(Paragraph("1. Live Parametric Simulation Results (Active Configuration)", section_h1))
    
    ebit_val = sim_data.get('adjusted_ebit', 31.2)
    margin_val = sim_data.get('margin_pct', 8.21)
    effective_power = sim_data.get('effective_cn_power', 24.43)
    veto_active = sim_data.get('blocking_veto', False)
    pack_penalty = sim_data.get('unit_pack_penalty', 1944)
    total_deductions = sim_data.get('total_battery_penalty_b', 2.33) + sim_data.get('china_ebit_loss_b', 2.4) + sim_data.get('tariff_loss_b', 0.2)

    kpi_col1 = f"<b>Adjusted Group EBIT</b><br/><font size='14' color='#0F172A'><b>€{ebit_val:.1f}B</b></font><br/><font size='7.5' color='#64748B'>Margin: {margin_val:.2f}% (Deductions: -€{total_deductions:.2f}B)</font>"
    kpi_col2 = f"<b>Effective Chinese Voting</b><br/><font size='14' color='{'#BE123C' if veto_active else '#047857'}'><b>{effective_power:.2f}%</b></font><br/><font size='7.5' color='#64748B'>Baseline: 19.67% (Diluted: {sim_data.get('s_cn', 17.1):.2f}%)</font>"
    kpi_col3 = f"<b>AktG §179 Veto Status</b><br/><font size='12' color='{'#BE123C' if veto_active else '#047857'}'><b>{'25% VETO ACTIVE' if veto_active else '25% VETO BROKEN'}</b></font><br/><font size='7.5' color='#64748B'>Threshold: &lt;25.00% Required</font>"
    kpi_col4 = f"<b>Battery Unit Penalty</b><br/><font size='14' color='#B45309'><b>+€{pack_penalty:.0f}/EV</b></font><br/><font size='7.5' color='#64748B'>Total Hit: -€{sim_data.get('total_battery_penalty_b', 2.33):.2f}B</font>"

    kpi_data = [[
        Paragraph(kpi_col1, body_style),
        Paragraph(kpi_col2, body_style),
        Paragraph(kpi_col3, body_style),
        Paragraph(kpi_col4, body_style)
    ]]
    kpi_table = Table(kpi_data, colWidths=[126, 126, 126, 126])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 10))

    # 4. Active Policy Lever Inputs Table
    story.append(Paragraph("Active Policy Lever Inputs for this Run:", body_bold))
    story.append(Spacer(1, 3))
    
    levers_data = [
        [
            Paragraph("<b>Parameter</b>", table_header),
            Paragraph("<b>Simulated Value</b>", table_header),
            Paragraph("<b>Econometric &amp; Legal Context</b>", table_header)
        ],
        [
            Paragraph("1. Strategic Capital Dilution", table_cell),
            Paragraph(f"+{sim_data.get('dilution_pct', 15)}% New Shares", table_cell),
            Paragraph("Issued to European Sovereign Mobility Funds under §182 AktG to dilute non-EU equity.", table_cell)
        ],
        [
            Paragraph("2. Allied Proxy Turnout", table_cell),
            Paragraph(f"{sim_data.get('allied_turnout', 85)}% Turnout", table_cell),
            Paragraph(f"Allied turnout >=85% drives total turnout to {sim_data.get('total_turnout', 69.0):.1f}%, breaking 25% veto.", table_cell)
        ],
        [
            Paragraph("3. China Volume Shock", table_cell),
            Paragraph(f"-{sim_data.get('china_volume_shock', 15)}% Contraction", table_cell),
            Paragraph(f"Contraction of joint venture sales resulting in -€{sim_data.get('china_ebit_loss_b', 2.4):.2f}B EBIT impact.", table_cell)
        ],
        [
            Paragraph("4. Non-China Mineral Premium", table_cell),
            Paragraph(f"+{sim_data.get('mineral_premium', 20)}% Surcharge", table_cell),
            Paragraph(f"Western upstream refining premium leading to +€{pack_penalty:.0f}/EV unit pack cost delta.", table_cell)
        ],
        [
            Paragraph("5. Triad BEV Annual Volume", table_cell),
            Paragraph(f"{(sim_data.get('bev_volume', 1200000) / 1000000):.2f}M Units", table_cell),
            Paragraph(f"Total annual battery surcharge of -€{sim_data.get('total_battery_penalty_b', 2.33):.2f}B across global production.", table_cell)
        ],
        [
            Paragraph("6. EU Countervailing Tariff", table_cell),
            Paragraph(f"{sim_data.get('tariff_rate', 21)}% Duty", table_cell),
            Paragraph(f"Tariff impact on re-exported vehicles causing -€{(sim_data.get('tariff_loss_b', 0.2)*1000):.0f}M margin compression.", table_cell)
        ]
    ]
    levers_table = Table(levers_data, colWidths=[150, 110, 244])
    levers_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(levers_table)

    # Page Break for Page 2
    story.append(PageBreak())

    # 5. Page 2: Audited Empirical Time-Series (2019-2025)
    story.append(Paragraph("2. Audited Empirical Delivery Baseline (2019–2025)", section_h1))
    story.append(Paragraph(
        "Statutory filing audit across Volkswagen Group, Mercedes-Benz Group, and BMW Group verifying the continuous structural collapse in deliveries, market share, and joint venture EBIT contributions.",
        body_style
    ))
    story.append(Spacer(1, 6))

    hist_data = [
        [
            Paragraph("<b>Year</b>", table_header),
            Paragraph("<b>VW (k)</b>", table_header),
            Paragraph("<b>MB (k)</b>", table_header),
            Paragraph("<b>BMW (k)</b>", table_header),
            Paragraph("<b>Total (k)</b>", table_header),
            Paragraph("<b>Local Prod</b>", table_header),
            Paragraph("<b>Share</b>", table_header),
            Paragraph("<b>NEV %</b>", table_header),
            Paragraph("<b>China EBIT</b>", table_header)
        ],
        [Paragraph("2019", table_cell), Paragraph("4,233", table_cell), Paragraph("693", table_cell), Paragraph("724", table_cell), Paragraph("5,650", table_cell), Paragraph("89.5%", table_cell), Paragraph("25.1%", table_cell), Paragraph("4.9%", table_cell), Paragraph("€15.2B", table_cell)],
        [Paragraph("2020", table_cell), Paragraph("3,850", table_cell), Paragraph("774", table_cell), Paragraph("777", table_cell), Paragraph("5,401", table_cell), Paragraph("89.3%", table_cell), Paragraph("24.5%", table_cell), Paragraph("5.8%", table_cell), Paragraph("€14.8B", table_cell)],
        [Paragraph("2021", table_cell), Paragraph("3,300", table_cell), Paragraph("758", table_cell), Paragraph("846", table_cell), Paragraph("4,904", table_cell), Paragraph("89.1%", table_cell), Paragraph("21.5%", table_cell), Paragraph("15.5%", table_cell), Paragraph("€14.2B", table_cell)],
        [Paragraph("2022", table_cell), Paragraph("3,180", table_cell), Paragraph("751", table_cell), Paragraph("792", table_cell), Paragraph("4,723", table_cell), Paragraph("90.2%", table_cell), Paragraph("19.8%", table_cell), Paragraph("27.8%", table_cell), Paragraph("€13.5B", table_cell)],
        [Paragraph("2023", table_cell), Paragraph("3,236", table_cell), Paragraph("737", table_cell), Paragraph("825", table_cell), Paragraph("4,798", table_cell), Paragraph("90.1%", table_cell), Paragraph("18.2%", table_cell), Paragraph("35.7%", table_cell), Paragraph("€12.8B", table_cell)],
        [Paragraph("2024", table_cell), Paragraph("2,980", table_cell), Paragraph("675", table_cell), Paragraph("705", table_cell), Paragraph("4,360", table_cell), Paragraph("89.8%", table_cell), Paragraph("15.1%", table_cell), Paragraph("47.5%", table_cell), Paragraph("€9.8B", table_cell)],
        [Paragraph("2025", table_cell), Paragraph("2,780", table_cell), Paragraph("630", table_cell), Paragraph("650", table_cell), Paragraph("4,060", table_cell), Paragraph("89.2%", table_cell), Paragraph("12.8%", table_cell), Paragraph("53.5%", table_cell), Paragraph("€7.9B", table_cell)],
        [
            Paragraph("<b>Delta</b>", table_cell),
            Paragraph("<font color='#BE123C'><b>-34.3%</b></font>", table_cell),
            Paragraph("<font color='#BE123C'><b>-9.1%</b></font>", table_cell),
            Paragraph("<font color='#BE123C'><b>-10.2%</b></font>", table_cell),
            Paragraph("<font color='#BE123C'><b>-28.1%</b></font>", table_cell),
            Paragraph("<font color='#475569'><b>-1,435k</b></font>", table_cell),
            Paragraph("<font color='#BE123C'><b>-12.3%p</b></font>", table_cell),
            Paragraph("<font color='#047857'><b>+48.6%p</b></font>", table_cell),
            Paragraph("<font color='#BE123C'><b>-48.0%</b></font>", table_cell)
        ]
    ]
    hist_table = Table(hist_data, colWidths=[40, 56, 56, 56, 58, 62, 54, 58, 64])
    hist_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [colors.white, colors.HexColor('#F8FAFC')]),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#FEE2E2')),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
    ]))
    story.append(hist_table)
    story.append(Spacer(1, 12))

    # 6. Triad Asymmetric Vulnerability Summary
    story.append(Paragraph("3. Triad Structural Vulnerability & Corporate Hostage Breakdown", section_h1))
    
    triad_vuln = [
        [
            Paragraph("<b>Mercedes-Benz Group AG</b>", body_bold),
            Paragraph("<b>Volkswagen Group AG</b>", body_bold),
            Paragraph("<b>BMW Group AG</b>", body_bold)
        ],
        [
            Paragraph("<b>Capital Collar Trap:</b> BAIC (9.98%) + Geely (9.69%) control 19.67% equity (~37.5% AGM vote). S-Class (38%) and Maybach (45%) revenue concentration constrained management into anti-tariff lobbying.", table_cell),
            Paragraph("<b>Software Subcontracting Trap:</b> Despite 92.8% local assembly, CARIAD losses (>€6B) forced a $705M injection into XPENG (CEA zonal E/E) and Horizon Robotics, reducing VW to a software licensee.", table_cell),
            Paragraph("<b>Global Export Trap:</b> Acquired 75% BBA Shenyang (€3.73B) as global iX3 export hub with 100% CATL battery dependency, making BMW the primary victim of EU 20.7% countervailing tariffs.", table_cell)
        ]
    ]
    triad_table = Table(triad_vuln, colWidths=[168, 168, 168])
    triad_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(triad_table)
    story.append(Spacer(1, 12))

    # 7. German AktG §179 Mathematical Model Box
    story.append(Paragraph("4. German Corporate Law (AktG §179) Veto Elimination Proof", section_h1))
    aktg_proof_text = (
        "<b>Statutory Governance Rule:</b> Charter amendments require a 75% AGM supermajority. Any shareholder with &gt;25% "
        "represented capital holds an absolute veto (<i>Sperrminorität</i>).<br/>"
        "<b>Model A (Turnout Threshold):</b> Diluting Chinese stake to 17.10% (via 15% new shares to European Sovereign Funds) "
        "and mobilizing overall AGM attendance to <b>70.0%</b> reduces Chinese voting power to <b>24.43% (&lt;25.0%)</b>.<br/>"
        "<b>Model B (Disaggregated Multi-Class):</b> Under Chinese 100% and retail 38% turnout, allied-only turnout of <b>85.0%+</b> "
        "drives total attendance to <b>69.04%</b>, achieving an effective voting share of <b>24.77% (&lt;25.0%)</b>."
    )
    aktg_box = Table([[Paragraph(aktg_proof_text, callout_style)]], colWidths=[504])
    aktg_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F0FDF4' if not veto_active else '#FEF2F2')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#16A34A' if not veto_active else '#DC2626')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(aktg_box)

    # Page Break for Page 3
    story.append(PageBreak())

    # 8. Page 3: 5 Strategic Truths & Board Supervisory Checklist
    story.append(Paragraph("5. Five Executive Strategic Truths (Policy Directives)", section_h1))
    
    truths_data = [
        [
            Paragraph("<b>TRUTH 01: TARIFF PARADOX</b><br/>Unilateral border duties compress margins for Western OEMs re-exporting from China (BMW Shenyang iX3), while non-EU competitors circumvent tariffs through Eastern European assembly plants.", table_cell),
            Paragraph("<b>TRUTH 02: THE COST OF DECOUPLING</b><br/>Abruptly forfeiting €45.0B in cumulative sunk CapEx and €12.8B in annual JV dividends causes severe liquidity deficits across Western headquarters.", table_cell)
        ],
        [
            Paragraph("<b>TRUTH 03: GOVERNANCE DEFENSE</b><br/>Executing 15% strategic dilution and mobilizing proxy turnout to achieve total AGM turnout >= 70.0% (or allied turnout >= 85.0%) eliminates AktG §179 blocking vetoes.", table_cell),
            Paragraph("<b>TRUTH 04: SUPPLY CHAIN ALLIANCE</b><br/>Unit battery cost premiums (+€1,944/EV) cannot be absorbed alone; OEMs must form multilateral procurement alliances with Korean, Japanese, and Western Tier-1 suppliers.", table_cell)
        ],
        [
            Paragraph("<b>TRUTH 05: DATA AIR-GAP MANDATE</b><br/>Deploy 100% localized digital stacks for mainland domestic vehicles, while enforcing NATO-certified sovereign data air-gaps on all Western global fleets.", table_cell),
            Paragraph("<b>STRATEGIC SWEET SPOT (SCENARIO B)</b><br/>Phased De-risking enables steady margin expansion to 10.2% post-2032 while restoring 85% of strategic bargaining power.", table_cell)
        ]
    ]
    truths_table = Table(truths_data, colWidths=[252, 252])
    truths_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(truths_table)
    story.append(Spacer(1, 10))

    # 9. 6-Point Supervisory Board Checklist
    story.append(Paragraph("6. C-Level & Supervisory Board 6-Point Oversight Checklist", section_h1))
    
    checklist_data = [
        [Paragraph("<b>#</b>", table_header), Paragraph("<b>Supervisory Action Item</b>", table_header), Paragraph("<b>Statutory Oversight Requirement</b>", table_header)],
        [Paragraph("01", table_cell), Paragraph("Shareholder Governance Oversight", table_cell), Paragraph("Verify non-EU AGM voting power is strictly controlled below 25.0% under German AktG §179.", table_cell)],
        [Paragraph("02", table_cell), Paragraph("Software Source Code Black-Boxing", table_cell), Paragraph("Supply only compiled binary firmware to Chinese JVs; root algorithm source code isolated in European HSMs.", table_cell)],
        [Paragraph("03", table_cell), Paragraph("Outbound Data Air-Gapping", table_cell), Paragraph("Enforce complete physical and cryptographic air-gapping on NATO-certified sovereign clouds (PRC Art. 7 defense).", table_cell)],
        [Paragraph("04", table_cell), Paragraph("30% Battery Supply Concentration Cap", table_cell), Paragraph("Cap single-nation battery BOM dependency below 30% through 10-year offtake agreements with allied suppliers.", table_cell)],
        [Paragraph("05", table_cell), Paragraph("Unilateral JV Exit & IP Revocation", table_cell), Paragraph("Codify automatic buy-back options and immediate IP invalidation covenants upon state technology transfer decrees.", table_cell)],
        [Paragraph("06", table_cell), Paragraph("Board Geopolitical Risk Committee", table_cell), Paragraph("Mandate unanimous Geopolitical Risk Committee approval on all new foreign capital investments and joint ventures.", table_cell)]
    ]
    checklist_table = Table(checklist_data, colWidths=[20, 160, 324])
    checklist_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(checklist_table)
    story.append(Spacer(1, 10))

    # 10. Final Executive Sign-off Box
    verdict_text = (
        "<b>Supervisory Board Sign-off Directive:</b> The Supervisory Board must reject both passive inaction (Status Quo) "
        "and emotional cliff-edge withdrawal. Management is instructed to execute <b>Scenario B (Phased De-risking)</b>, "
        "commencing capital restructuring and data air-gapping immediately."
    )
    verdict_box = Table([[Paragraph(verdict_text, callout_style)]], colWidths=[504])
    verdict_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ECFDF5')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#059669')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(verdict_box)

    # Build PDF using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer
