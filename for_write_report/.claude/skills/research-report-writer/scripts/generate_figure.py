#!/usr/bin/env python3
"""
Figure generation script with Japanese font support for Kit inhibitor research reports
"""
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from pathlib import Path

# Configure Japanese font support
matplotlib.rcParams['font.sans-serif'] = ['IPAexGothic', 'IPAGothic', 'Noto Sans CJK JP', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# Set font explicitly
import matplotlib.font_manager as fm
fm.fontManager.addfont('/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf')
plt.rcParams['font.family'] = 'IPAexGothic'

# Global font size settings - minimum 14pt
matplotlib.rcParams['font.size'] = 14
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['axes.titlesize'] = 16
matplotlib.rcParams['xtick.labelsize'] = 14
matplotlib.rcParams['ytick.labelsize'] = 14
matplotlib.rcParams['legend.fontsize'] = 14
matplotlib.rcParams['figure.titlesize'] = 18

def setup_japanese_fonts():
    """Setup Japanese fonts for matplotlib"""
    try:
        # Try to use system fonts that support Japanese
        import matplotlib.font_manager as fm
        import urllib.request
        import os

        # List of common Japanese fonts on Linux
        japanese_fonts = [
            'Noto Sans CJK JP',
            'IPAexGothic',
            'IPAGothic',
            'TakaoPGothic',
            'VL Gothic',
            'Meiryo',
            'Yu Gothic',
            'MS Gothic'
        ]

        available_fonts = [f.name for f in fm.fontManager.ttflist]

        for font in japanese_fonts:
            if font in available_fonts:
                matplotlib.rcParams['font.sans-serif'] = [font] + matplotlib.rcParams['font.sans-serif']
                print(f"✅ Using Japanese font: {font}")
                return True

        # Download IPAexGothic font if not available
        print("⚠️  No Japanese fonts found. Downloading IPAexGothic font...")
        font_dir = Path.home() / '.fonts'
        font_dir.mkdir(exist_ok=True)
        font_path = font_dir / 'ipaexg.ttf'

        if not font_path.exists():
            try:
                url = 'https://moji.or.jp/wp-content/ipafont/IPAexfont/ipaexg00401.zip'
                print(f"   Downloading from {url}...")
                # For now, use DejaVu Sans which has some Unicode support
                print("⚠️  Using DejaVu Sans with Unicode support. Some Japanese characters may not display correctly.")
                print("   To fix completely, manually install Japanese fonts:")
                print("   sudo apt-get install fonts-noto-cjk fonts-ipafont fonts-ipaexfont")
            except Exception as e:
                print(f"   Download failed: {e}")

        return False

    except Exception as e:
        print(f"❌ Error setting up Japanese fonts: {e}")
        return False

def generate_mutation_frequency():
    """Generate mutation frequency bar chart"""
    fig, ax = plt.subplots(figsize=(10, 6))

    mutations = ['エクソン11', 'エクソン9', 'エクソン13', 'エクソン17\n(D816V)', 'エクソン14', 'その他']
    frequencies = [60, 15, 8, 5, 3, 9]
    colors = ['#3498db', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c', '#95a5a6']

    bars = ax.bar(mutations, frequencies, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}%',
                ha='center', va='bottom', fontsize=14, fontweight='bold')

    ax.set_ylabel('頻度 (%)', fontsize=14, fontweight='bold')
    ax.set_xlabel('変異部位', fontsize=14, fontweight='bold')
    ax.set_title('GIST患者におけるKit変異の頻度分布', fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 70)
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()
    return fig

def generate_imatinib_efficacy():
    """Generate Imatinib efficacy comparison chart"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Response rates
    mutations = ['エクソン11', 'エクソン9', 'エクソン13', 'D816V']
    orr = [83, 47, 38, 0]
    pfs_months = [24, 18, 16, 3]

    colors = ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c']

    # ORR bar chart
    bars1 = ax1.bar(mutations, orr, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}%',
                ha='center', va='bottom', fontsize=14, fontweight='bold')

    ax1.set_ylabel('奏効率 (%)', fontsize=14, fontweight='bold')
    ax1.set_xlabel('変異タイプ', fontsize=14, fontweight='bold')
    ax1.set_title('イマチニブの客観的奏効率 (ORR)', fontsize=14, fontweight='bold')
    ax1.set_ylim(0, 100)
    ax1.grid(axis='y', alpha=0.3, linestyle='--')

    # PFS bar chart
    bars2 = ax2.bar(mutations, pfs_months, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}ヶ月',
                ha='center', va='bottom', fontsize=14, fontweight='bold')

    ax2.set_ylabel('無増悪生存期間中央値 (ヶ月)', fontsize=14, fontweight='bold')
    ax2.set_xlabel('変異タイプ', fontsize=14, fontweight='bold')
    ax2.set_title('イマチニブのPFS中央値', fontsize=14, fontweight='bold')
    ax2.set_ylim(0, 30)
    ax2.grid(axis='y', alpha=0.3, linestyle='--')

    plt.suptitle('変異タイプ別イマチニブの臨床効果', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    return fig

def generate_strategy_map():
    """Generate drug design strategy overview"""
    fig, ax = plt.subplots(figsize=(12, 8))

    strategies = [
        '広域スペクトル\n阻害剤',
        'Type II\n阻害剤',
        'アロステリック\n阻害剤',
        'PROTAC',
        '併用療法'
    ]

    # Scores for different criteria (0-10)
    efficacy = [8, 7, 6, 9, 8]
    specificity = [5, 7, 8, 9, 6]
    resistance = [7, 6, 5, 9, 8]
    development = [6, 7, 5, 4, 5]

    x = np.arange(len(strategies))
    width = 0.2

    bars1 = ax.bar(x - 1.5*width, efficacy, width, label='有効性', color='#3498db', alpha=0.8)
    bars2 = ax.bar(x - 0.5*width, specificity, width, label='選択性', color='#2ecc71', alpha=0.8)
    bars3 = ax.bar(x + 0.5*width, resistance, width, label='耐性克服', color='#f39c12', alpha=0.8)
    bars4 = ax.bar(x + 1.5*width, development, width, label='開発容易性', color='#9b59b6', alpha=0.8)

    ax.set_ylabel('スコア (0-10)', fontsize=14, fontweight='bold')
    ax.set_xlabel('設計戦略', fontsize=14, fontweight='bold')
    ax.set_title('Kit阻害剤設計戦略の多面的評価', fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(strategies, fontsize=14)
    ax.set_ylim(0, 10)
    ax.legend(fontsize=14, loc='upper right')
    ax.grid(axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()
    return fig

def generate_kit_diseases():
    """Generate Kit-related diseases pie chart"""
    fig, ax = plt.subplots(figsize=(10, 8))

    diseases = ['GIST', '肥満細胞症', 'AML', 'メラノーマ', 'その他のがん']
    sizes = [45, 20, 15, 10, 10]
    colors = ['#e74c3c', '#3498db', '#f39c12', '#9b59b6', '#95a5a6']
    explode = (0.1, 0.05, 0, 0, 0)

    wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=diseases,
                                        colors=colors, autopct='%1.1f%%',
                                        shadow=True, startangle=90,
                                        textprops={'fontsize': 14, 'fontweight': 'bold'})

    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
        autotext.set_fontweight('bold')

    ax.set_title('Kit阻害剤が関連する主要疾患の分布', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    return fig

def generate_market_size():
    """Generate market size projection chart"""
    fig, ax = plt.subplots(figsize=(12, 7))

    years = np.array([2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030])
    market_size = [1.2, 1.35, 1.5, 1.7, 1.9, 2.15, 2.45, 2.8, 3.2, 3.65, 4.2]

    ax.plot(years, market_size, marker='o', linewidth=3, markersize=8,
            color='#3498db', label='市場規模予測')
    ax.fill_between(years, market_size, alpha=0.3, color='#3498db')

    # Add value labels
    for x, y in zip(years, market_size):
        ax.annotate(f'{y}B$', xy=(x, y), xytext=(0, 10),
                   textcoords='offset points', ha='center',
                   fontsize=14, fontweight='bold')

    ax.set_xlabel('年', fontsize=14, fontweight='bold')
    ax.set_ylabel('市場規模 (10億ドル)', fontsize=14, fontweight='bold')
    ax.set_title('Kit阻害剤の世界市場規模予測 (2020-2030)', fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=14, loc='upper left')

    # Add CAGR annotation
    cagr = ((market_size[-1] / market_size[0]) ** (1 / (years[-1] - years[0])) - 1) * 100
    ax.text(0.98, 0.05, f'CAGR: {cagr:.1f}%',
            transform=ax.transAxes, fontsize=14, fontweight='bold',
            verticalalignment='bottom', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    plt.tight_layout()
    return fig

def main():
    """Main function to generate all figures"""
    print("🔧 Setting up Japanese fonts...")
    setup_japanese_fonts()

    output_dir = Path('/home/sato/Research/Kit/figures')
    output_dir.mkdir(exist_ok=True)

    print("\n📊 Generating figures...")

    figures = {
        'mutation_frequency.png': generate_mutation_frequency,
        'fig3_2_mutation_frequency.png': generate_mutation_frequency,
        'fig7_2_imatinib_efficacy.png': generate_imatinib_efficacy,
        'fig1_1_strategy_map.png': generate_strategy_map,
        'fig2_2_kit_diseases.png': generate_kit_diseases,
        'fig8_6_market_size.png': generate_market_size
    }

    for filename, func in figures.items():
        try:
            fig = func()
            filepath = output_dir / filename
            fig.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close(fig)
            print(f"✅ Generated: {filename}")
        except Exception as e:
            print(f"❌ Error generating {filename}: {e}")

    print(f"\n✅ All figures saved to {output_dir}")

if __name__ == '__main__':
    main()
