CREATE TABLE IF NOT EXISTS "phastcons" (
  "snp" TEXT,
  "phastcons" REAL
);
CREATE TABLE IF NOT EXISTS "snp" (
  "snp" TEXT,
  "chrom" TEXT,
  "pos" INTEGER,
  "quality" REAL,
  "ref" TEXT,
  "type" TEXT,
  "alt" TEXT,
  "category" TEXT
);
CREATE TABLE IF NOT EXISTS "snp_call" (
  "snp" TEXT,
  "sample" TEXT,
  "genotype" TEXT,
  "genotype_simple" INTEGER
);
CREATE TABLE IF NOT EXISTS "snp_effect" (
  "snp" TEXT,
  "allele" TEXT,
  "effect" TEXT,
  "impact" TEXT,
  "gene" TEXT,
  "gene_id" TEXT,
  "feature_type" TEXT,
  "feature_id" TEXT,
  "biotype" TEXT,
  "rank" TEXT,
  "hgvs.c" TEXT,
  "hgvs.p" TEXT,
  "cdna_pos" TEXT,
  "cds_pos" TEXT,
  "prot_pos" TEXT,
  "distance_to_feature" INTEGER,
  "messages" TEXT
);
CREATE TABLE IF NOT EXISTS "phastcons_exam" (
  "snp" TEXT,
  "phastcons" REAL
);
CREATE UNIQUE INDEX snps_unique on phastcons_exam (snp);
