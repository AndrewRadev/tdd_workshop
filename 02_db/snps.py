def categorize_snps(db):
    db.execute("""
        UPDATE snp SET category = 'Normal'
        WHERE snp.snp IN (
            SELECT snp FROM snp_call
            WHERE genotype_simple > 0
            AND sample = 'TLE66_N'
        )
    """)

    db.execute("""
        UPDATE snp SET category = IIF(category IS NULL, 'Tumor', 'Mixed')
        WHERE snp.snp IN (
            SELECT snp FROM snp_call
            WHERE genotype_simple > 0
            AND sample = 'TLE66_T'
        )
    """)
