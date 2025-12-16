# Vliv parametru Temperature na podobnost a kvalitu kódu generovaného LLM

**Externí přílohy k bakalářské práci**

Repozitář obsahuje experimentální data, analytické skripty a vizualizace pro bakalářskou práci zkoumající vliv teplotního parametru na kvalitu a podobnost kódu generovaného velkými jazykovými modely.

**Autor:** Filip Stehlík
**Vedoucí práce:** Ing. Mgr. Pavel Beránek
**Fakulta:** Přírodovědecká fakulta, UJEP Ústí nad Labem
**Rok:** 2026

---

## O experimentu

### Výzkumná otázka
Jak parametr **temperature** (T ∈ [0.0, 1.0]) ovlivňuje kvalitu a podobnost kódu generovaného velkými jazykovými modely?

### Hlavní zjištění

1. **Temperature NEMÁ vliv na kvalitu kódu**
   - Všechny metriky kvality konstantní: |r| < 0.04, p > 0.2
   - Funkční správnost: 68-70% nezávisle na teplotě

2. **Temperature MÁ silný vliv na podobnost kódu**
   - BLEU klesá o 35%: z 0.481 (T=0.0) na 0.313 (T=1.0), r = -0.350
   - CodeBLEU klesá o 21%: z 0.570 na 0.449, r = -0.315
   - Vyšší teplota = větší diverzita bez ztráty kvality

3. **Rozdíly mezi modely**
   - Claude Sonnet 4: Nejcitlivější (R² = 0.346)
   - Gemini 2.5 Pro: Nejstabilnější (R² = 0.062)
   - ChatGPT 4.1: Střední citlivost (R² = 0.089)

### Design experimentu

- **Rozsah:** 1,080 vygenerovaných Python souborů
- **Faktory:** 3 modely × 3 úlohy × 6 teplot × 20 iterací
- **Modely:** ChatGPT 4.1, Claude Sonnet 4, Gemini 2.5 Pro
- **Teploty:** 0.0, 0.2, 0.4, 0.6, 0.8, 1.0
- **Úlohy:** calculator, ascii_art, todo_list
- **Datum:** Prosinec 2024

---

## Struktura repozitáře

```
Serial_experiments_temperature/
├── code/                           # Python skripty pro analýzu
│   ├── generation/                 # Generování kódu přes OpenRouter API
│   ├── similarity_analysis/        # BLEU, CodeBLEU, AST Distance, TSED
│   ├── static_analysis/            # Halstead, Cyclomatic, MI
│   ├── static_visualization/       # Vizualizace statických metrik
│   ├── visualization/              # Vizualizace podobnosti
│   ├── utils/                      # Pomocné funkce
│   └── main.py                     # Hlavní runner
├── dry_run_output/                 # Experimentální data
│   ├── code/                       # 1,080 vygenerovaných .py souborů
│   │   ├── ascii_art/              # 360 souborů (3 modely × 6 T × 20 iter)
│   │   ├── calculator/             # 360 souborů
│   │   └── todo_list/              # 360 souborů
│   ├── response/                   # Raw LLM odpovědi (JSON)
│   ├── static_analysis/            # CSV výsledky metrik
│   └── similarity_analysis/        # CSV výsledky podobnosti
├── figures/                        # PDF grafy pro práci
│   ├── similarity/                 # 8 grafů podobnosti
│   │   ├── bleu_by_temperature.pdf
│   │   ├── temperature_effect.pdf
│   │   ├── consistency_codebleu.pdf
│   │   └── ...
│   ├── static_analysis/            # 9 grafů kvality
│   │   ├── pass_rate_boxplot.pdf
│   │   ├── quality_scatter_trends.pdf
│   │   ├── compilation_rate_comparison.pdf
│   │   └── ...
│   └── summary_comparison.pdf      # Souhrnný graf
├── prompts/                        # Zadání úloh
│   ├── ascii_art/                  # Prompt + testy
│   ├── calculator/                 # Prompt + testy
│   └── todo_list/                  # Prompt + testy
├── tables/                         # CSV tabulky s daty
├── extract_statistics.py           # Hlavní skript pro extrakci statistik
├── statistics_summary.txt          # Souhrn všech korelací a regresí
├── pyproject.toml                  # Závislosti (uv)
├── uv.lock                         # Lockfile
├── .gitignore
├── .python-version                 # Python 3.11
├── LICENSE                         # CC BY-NC-SA 4.0
└── README.md                       # Tento soubor
```

---

## Instalace a použití

### Požadavky

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager (doporučeno)

### Instalace závislostí

```bash
# Pomocí uv (doporučeno)
uv sync

# Alternativně pomocí pip
pip install -r requirements.txt
```

### Spuštění analýzy

```bash
# Aktivace virtual environmentu
source .venv/bin/activate  # Linux/Mac
# nebo
.venv\Scripts\activate     # Windows

# Extrakce statistik
python extract_statistics.py

# Generování grafů
python -m code.visualization.enhanced_plots
python -m code.static_visualization.static_plots
```

---

## Použité metriky

### Metriky kvality kódu (statická analýza)

1. **Kompilovatelnost** - Počet syntakticky správných souborů
2. **Pass rate** - Procento testů, které prošly
3. **Cyklomatická složitost** - Počet nezávislých cest kódem
4. **Halstead metriky** - Volume, Difficulty, Effort
5. **Maintainability Index** - Kompozitní index udržitelnosti (0-100)

### Metriky podobnosti kódu

1. **BLEU** - N-gram overlap (0-1, vyšší = podobnější)
2. **CodeBLEU** - BLEU + AST + data flow (0-1)
3. **AST Edit Distance** - Tree edit distance (nižší = podobnější)
4. **TSED** - Token Sequence Edit Distance (Concrete Syntax Tree)

---

## Klíčové soubory

### Data a výsledky

- **`statistics_summary.txt`** - Kompletní souhrn všech statistik
  - Korelace pro každou metriku
  - Lineární regrese podle modelů
  - Průměry, směrodatné odchylky, rozsahy

- **`dry_run_output/static_analysis/experiment_*/all_metrics.csv`** - Raw data metrik kvality
- **`dry_run_output/similarity_analysis/pairwise_within_temperature/*.csv`** - Raw data podobnosti

### Grafy použité v práci

Všechny grafy v `figures/` jsou ve formátu PDF a jsou přímo vloženy do bakalářské práce:

**Kvalita kódu (kapitola 2.4):**
- `compilation_rate_comparison.pdf` - Kompilovatelnost podle teploty
- `pass_rate_boxplot.pdf` - Distribuce funkční správnosti
- `quality_scatter_trends.pdf` - Scatter plot všech metrik kvality

**Podobnost kódu (kapitola 2.5):**
- `temperature_effect.pdf` - Vliv teploty na CodeBLEU, AST, TSED
- `bleu_by_temperature.pdf` - BLEU podle teploty s regresními liniemi
- `consistency_codebleu.pdf` - Konzistence CodeBLEU

### Skripty

- **`extract_statistics.py`** - Vypočítá korelace a regrese ze všech dat
- **`code/visualization/enhanced_plots.py`** - Generuje grafy podobnosti
- **`code/static_visualization/static_plots.py`** - Generuje grafy kvality

---

## Reprodukce experimentu

### 1. Generování kódu

```bash
# Vyžaduje OpenRouter API klíč
export OPENROUTER_API_KEY="your_key_here"

python -m code.main
```

### 2. Statická analýza

```bash
# Automaticky spuštěno v code.main
# Nebo manuálně:
python -m code.static_analysis.run_analysis
```

### 3. Analýza podobnosti

```bash
# Automaticky spuštěno v code.main
# Nebo manuálně:
python -m code.similarity_analysis.compute_similarities
```

### 4. Vizualizace

```bash
python -m code.visualization.enhanced_plots
python -m code.static_visualization.static_plots
```

---

## Závislosti

Hlavní Python balíčky (viz `pyproject.toml`):

- **radon** - Halsteadovy metriky, MI, cyklomatická složitost
- **nltk** - BLEU score
- **codebleu** - CodeBLEU metrika
- **zss** - Zhang-Shasha algoritmus pro AST distance
- **tree-sitter-python** - Parsing pro TSED
- **matplotlib** - Vizualizace
- **pandas** - Manipulace s daty
- **scipy** - Statistické výpočty

---

## Citace

Pokud používáte tato data nebo skripty, citujte prosím:

```bibtex
@thesis{stehlik2026temperature,
  author    = {Filip Stehlík},
  title     = {Vliv parametru Temperature na podobnost a kvalitu kódu
               generovaného velkými jazykovými modely},
  type      = {Bakalářská práce},
  school    = {Univerzita Jana Evangelisty Purkyně v Ústí nad Labem},
  year      = {2026},
  note      = {Vedoucí práce: Ing. Mgr. Pavel Beránek},
  url       = {https://github.com/stehlfi1/serial_experiment_temperature}
}
```

---

## Licence

Tento repozitář je licencován pod **Creative Commons BY-NC-SA 4.0**.

Můžete:
- ✓ Sdílet a upravovat obsah
- ✓ Používat pro nekomerční účely

Musíte:
- ✓ Uvést autora
- ✓ Zachovat stejnou licenci
- ✗ Nepoužívat komerčně

---

## Odkazy

- **Text práce:** [ki-thesis.pdf](../../tex/thesis_ki_ujep/ki-thesis.pdf)
- **GitHub repozitář:** https://github.com/stehlfi1/serial_experiment_temperature
- **Fakulta:** https://prf.ujep.cz/
- **UJEP:** https://www.ujep.cz/

---

## Kontakt

**Filip Stehlík**
Přírodovědecká fakulta UJEP
Ústí nad Labem, Česká republika

Pro dotazy ohledně experimentu nebo dat prosím otevřete issue na GitHubu.

---

**Poslední aktualizace:** Prosinec 2024
**Status:** Finální verze pro odevzdání
