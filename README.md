## Miscellaneous Scripts

In the cwd, change all file prefixes or suffixes. Filenames changes are printed to stdout.

- **change-ext.sh**
- **change-pref.sh**

Convert back and forth between tab-delimited files (extension agnostic) and MS Excel xlsx or xls files. Depends on modules Spreadsheet::ParseExcel, Spreadsheet::XLSX, and Excel::Writer::XLSX.

- **excel2tsv.pl**
- **tsv2excel.pl**

---

- **calc_all_pairwise_combinations.py** - Given a file of line-by-line identifiers (or first column identifiers in tab-delimited file), all unique pairwise comparisons will be listed excluding self-vs-self.
 - this example should list 52 pairs: `python calc_all_pairwise_combinations.py examples/list.txt | sort -k1,2 | grep -v 'self-to-self'`
