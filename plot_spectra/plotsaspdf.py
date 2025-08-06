# %%
import matplotlib.pyplot as plt
import pandas as pd

from matplotlib.backends.backend_pdf import PdfPages

# NEW SPECTRA

bvt = pd.read_csv('202504_data/spectra_20250608/oldblue vane whitelight june8th.txt', sep='\t')
bvt = bvt.loc[:, ~bvt.columns.str.startswith("Capture_")].drop(columns=['Unnamed: 10'])

grn = pd.read_csv('202504_data/spectra_20250608/green board whitelight june8th.txt', sep='\t')
grn = grn.loc[:, ~grn.columns.str.startswith("Capture_")].drop(columns=['Unnamed: 12'])

yel = pd.read_csv('202504_data/spectra_20250608/yellow board whitelight june8th.txt', sep='\t')
yel = yel.loc[:, ~yel.columns.str.startswith("Capture_")].drop(columns=['Unnamed: 12'])


# BACKGROUNDS
# murdock = pd.read_csv('202504_data/UTF-8whitelight Murdock CMYc blue.txt', sep='\t')
# murdock = murdock.loc[:, ~murdock.columns.str.startswith("Capture_")].drop(columns=['Unnamed: 10'])
# murdock['avg'] = murdock[['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 9']].mean(axis=1)
# murdock = murdock.drop(columns=['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 9'])

# mirror = pd.read_csv('202504_data/UTF-8ag mirror background.txt', sep='\t')
# mirror = mirror.loc[:, ~mirror.columns.str.startswith("Capture_")].drop(columns=['Unnamed: 4'])
# mirror['avg'] = mirror[['Unnamed: 1', 'Unnamed: 3']].mean(axis=1)
# mirror = mirror.drop(columns=['Unnamed: 1', 'Unnamed: 3'])

rgb_bg = pd.read_csv('202504_data/rgb_white_background_refl.txt', sep='\t')
rgb_bg = rgb_bg.loc[:, ~rgb_bg.columns.str.startswith("Capture_")].drop(columns=['Unnamed: 10'])
rgb_bg['avg'] = rgb_bg[['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 9']].mean(axis=1)
rgb_bg = rgb_bg.drop(columns=['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 9'])

cmyc_bg = pd.read_csv('202504_data/cmyc_white_background_refl.txt', sep='\t')
cmyc_bg = cmyc_bg.loc[:, ~cmyc_bg.columns.str.startswith("Capture_")].drop(columns=['Unnamed: 12'])
cmyc_bg['avg'] = cmyc_bg[['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 9', 'Unnamed: 11']].mean(axis=1)
cmyc_bg = cmyc_bg.drop(columns=['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 9', 'Unnamed: 11'])

bg_dfs = {
    # 'murdock': murdock,
    # 'mirror': mirror,
    'rgb_bg': rgb_bg,
    'cmyc_bg': cmyc_bg
}

x_col = 'USB2G13063_1:101'
y_cols = ['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 9']

plt.figure()
for col in y_cols:
    plt.plot(bvt[x_col], bvt[col])

plt.title('raw bee trap')
plt.xlabel('nm')
plt.xlim(400,750)

for bg_name, bg_df in bg_dfs.items():
    plt.figure()
    for col in y_cols:
        norm_values = bvt[col] / bg_df['avg']
        plt.plot(bvt[x_col], norm_values, label=col)

    plt.title(f'normalized by {bg_name}')
    plt.xlabel('nm')
    plt.ylabel('Normalized Intensity')
    plt.xlim(400, 750)
 
x_col = 'USB2G13063_1:101'
y_cols = ['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 9', 'Unnamed: 11']

plt.figure()
for col in y_cols:
    plt.plot(grn[x_col], grn[col])

plt.xlabel('nm')
plt.title('raw green')
plt.xlim(400,750)

for bg_name, bg_df in bg_dfs.items():
    plt.figure()
    for col in y_cols:
        norm_values = grn[col] / bg_df['avg']
        plt.plot(bvt[x_col], norm_values, label=col)

    plt.title(f'normalized by {bg_name}')
    plt.xlabel('nm')
    plt.ylabel('Normalized Intensity')
    plt.xlim(400, 750)

x_col = 'USB2G13063_1:101'
y_cols = ['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 9', 'Unnamed: 11']

plt.figure()
for col in y_cols:
    plt.plot(yel[x_col], yel[col])

plt.xlabel('nm')
plt.title('raw yellow')
plt.xlim(400,750)

for bg_name, bg_df in bg_dfs.items():
    plt.figure()
    for col in y_cols:
        norm_values = yel[col] / bg_df['avg']
        plt.plot(bvt[x_col], norm_values, label=col)

    plt.title(f'normalized by {bg_name}')
    plt.xlabel('nm')
    plt.ylabel('Normalized Intensity')
    plt.xlim(400, 750)

from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

sources = {
    'bee trap': (bvt, ['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 9']),
    'grn': (grn, ['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 9', 'Unnamed: 11']),
    'yel': (yel, ['Unnamed: 1', 'Unnamed: 3', 'Unnamed: 5', 'Unnamed: 7', 'Unnamed: 9', 'Unnamed: 11']),
}

x_col = 'USB2G13063_1:101'

with PdfPages('spectra_20250608.pdf') as pdf:
    for source_name, (df_src, y_cols) in sources.items():
        fig, axs = plt.subplots(2, 2, figsize=(14, 10))
        axs = axs.flatten()

        ax_raw = axs[0]
        for col in y_cols:
            ax_raw.plot(df_src[x_col], df_src[col], label=col)
        ax_raw.set_title(f'raw {source_name}')
        ax_raw.set_xlabel('nm')
        ax_raw.set_ylabel('intensity')
        ax_raw.set_xlim(400, 750)

        fig.delaxes(axs[1])

        norm_axes = axs[2:]
        for ax, (bg_name, bg_df) in zip(norm_axes, bg_dfs.items()):
            for col in y_cols:
                norm_values = df_src[col] / bg_df['avg']
                ax.plot(df_src[x_col], norm_values, label=col)

            ax.set_title(f'{source_name} – normalized by {bg_name}')
            ax.set_xlabel('nm')
            ax.set_ylabel('normalized intensity')
            ax.set_xlim(400, 750)

        plt.tight_layout()
        pdf.savefig(fig)
        plt.close()
