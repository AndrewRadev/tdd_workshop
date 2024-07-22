# Add "category" to snps:
#
# 1. If snp is normal-specific, category = "Normal"
# 2. If snp is tumor-specific,  category = "Tumor"
# 3. If snp is both,            category = "Mixed"
# 4. If snp is neither,         category = NULL
#

def categorize_snps(db):
    db.execute('''
        UPDATE snp
        SET category = 'Normal'
        WHERE snp.snp in (
            SELECT snp
            FROM snp_call
            WHERE sample = 'TLE66_N'
            AND genotype_simple > 0
        )
    ''')

    db.execute('''
        UPDATE snp
        SET category = IIF(category IS NULL, 'Tumor', 'Mixed')
        WHERE snp.snp in (
            SELECT snp
            FROM snp_call
            WHERE sample = 'TLE66_T'
            AND genotype_simple > 0
        )
    ''')
