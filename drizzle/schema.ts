/**
 * echo-va-claims — VA Disability Claims Schema
 * Extracted from art-of-proof Domain 1
 *
 * These tables are 100% VA-specific.
 * Shared tables (users, documents, payments) live in art-of-proof
 * and are referenced by userId FK.
 *
 * Nathan Poinsette (∇θ Operator) | Echo Universe
 */

import {
  int, mysqlEnum, mysqlTable, text,
  timestamp, varchar, boolean, json
} from "drizzle-orm/mysql-core";

// ─── VA CLAIMS ───────────────────────────────────────────────────────────────

export const vaClaims = mysqlTable("va_claims", {
  id:               int("id").autoincrement().primaryKey(),
  userId:           int("userId").notNull(),  // FK → art-of-proof users table

  caseNumber:       varchar("caseNumber",       { length: 64  }).notNull().unique(),
  veteranName:      varchar("veteranName",       { length: 255 }).notNull(),
  veteranSSN:       varchar("veteranSSN",        { length: 11  }), // AES-256 encrypted
  veteranDOB:       varchar("veteranDOB",        { length: 10  }),
  serviceNumber:    varchar("serviceNumber",     { length: 64  }),
  branchOfService:  varchar("branchOfService",   { length: 64  }),
  serviceStartDate: varchar("serviceStartDate",  { length: 10  }),
  serviceEndDate:   varchar("serviceEndDate",    { length: 10  }),
  dischargeType:    varchar("dischargeType",     { length: 64  }),

  claimType: mysqlEnum("claimType", [
    "initial", "supplemental",
    "higher_level_review", "board_appeal", "cue",
  ]).default("initial").notNull(),

  status: mysqlEnum("status", [
    "draft", "documents_uploaded", "processing",
    "analysis_complete", "claim_generated",
    "ready_for_submission", "submitted", "completed",
  ]).default("draft").notNull(),

  evidenceScore:   int("evidenceScore").default(0),   // 0-100
  devilLensPassed: boolean("devilLensPassed").default(false),
  totalCost:       int("totalCost").default(0),       // cents
  createdAt:       timestamp("createdAt").defaultNow().notNull(),
  updatedAt:       timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  completedAt:     timestamp("completedAt"),
});

// ─── CONDITIONS ──────────────────────────────────────────────────────────────

export const conditions = mysqlTable("conditions", {
  id:                int("id").autoincrement().primaryKey(),
  claimId:           int("claimId").notNull(),
  conditionName:     varchar("conditionName", { length: 255 }).notNull(),
  icdCode:           varchar("icdCode",       { length: 16  }),
  cfrCode:           varchar("cfrCode",       { length: 32  }),
  serviceConnection: text("serviceConnection"),
  nexusLetter:       text("nexusLetter"),              // AI-generated
  evidenceScore:     int("evidenceScore").default(0),
  primaryConditionId:int("primaryConditionId"),        // null = primary
  secondaryBasis:    text("secondaryBasis"),
  createdAt:         timestamp("createdAt").defaultNow().notNull(),
  updatedAt:         timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

// ─── VA DOCUMENTS ─────────────────────────────────────────────────────────────

export const vaDocuments = mysqlTable("va_documents", {
  id:           int("id").autoincrement().primaryKey(),
  claimId:      int("claimId").notNull(),
  documentType: mysqlEnum("documentType", [
    "dd214",                     // Separation doc — weight: 10
    "meps_entry_physical",       // Enlistment baseline — weight: 9
    "separation_physical",       // Discharge baseline — weight: 8
    "service_treatment_records", // In-service medical — weight: 10
    "private_medical_records",   // Post-service treatment — weight: 7
    "nexus_letter",              // Nexus opinion — weight: 10
    "buddy_statement",           // Lay witness — weight: 5
    "personal_statement",        // Veteran statement — weight: 6
    "va_rating_decision",        // Prior decisions — weight: 7
    "c_and_p_exam_report",       // VA examination — weight: 9
    "dbq",                       // Disability Benefits Questionnaire — weight: 8
    "military_personnel_file",   // Service records — weight: 7
    "lay_evidence",              // Non-medical testimony — weight: 4
    "other",
  ]).notNull(),
  filename:      varchar("filename", { length: 255 }).notNull(),
  fileKey:       varchar("fileKey",  { length: 500 }).notNull(),
  fileUrl:       text("fileUrl").notNull(),
  mimeType:      varchar("mimeType", { length: 100 }),
  fileSize:      int("fileSize"),
  evidenceWeight:int("evidenceWeight").default(0),
  qualityScore:  int("qualityScore").default(0),
  parsedData:    json("parsedData"),
  uploadedBy:    int("uploadedBy"),
  createdAt:     timestamp("createdAt").defaultNow().notNull(),
  updatedAt:     timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

// ─── DEVIL LENS CHECKS ───────────────────────────────────────────────────────

export const devilLensChecks = mysqlTable("devil_lens_checks", {
  id:      int("id").autoincrement().primaryKey(),
  claimId: int("claimId").notNull(),

  p01_sourcePurity:          int("p01"),
  p02_regulatoryBasis:       int("p02"),
  p03_constructivePossession:int("p03"),
  p04_chronologicalContinuity:int("p04"),
  p05_jurisdictionalLock:    int("p05"),
  p06_effectiveDateAnchor:   int("p06"),
  p07_antiDevelopmentShield: int("p07"),
  p08_accountabilityClause:  int("p08"),
  p09_hazardAdlMapping:      int("p09"),
  p10_constructiveNarrative: int("p10"),
  p11_denialCountermeasure:  int("p11"),
  p12_recordLockStatement:   int("p12"),
  p13_retroactiveImpact:     int("p13"),

  totalScore: int("totalScore").default(0),
  passed:     boolean("passed").default(false),  // >= 10 of 13
  notes:      json("notes"),
  createdAt:  timestamp("createdAt").defaultNow().notNull(),
});

// ─── LEGAL THEORIES ──────────────────────────────────────────────────────────

export const legalTheories = mysqlTable("legal_theories", {
  id:           int("id").autoincrement().primaryKey(),
  claimId:      int("claimId").notNull(),
  theoryType:   mysqlEnum("theoryType", [
    "direct_service_connection",
    "aggravation",
    "presumptive",
    "continuity",
    "secondary_service_connection",
    "cue",
    "cfr_3_156c",
    "tdiu",
  ]).notNull(),
  cfrCitations: json("cfrCitations").$type<string[]>(),
  caseLaw:      json("caseLaw").$type<string[]>(),
  narrative:    text("narrative"),
  strengthScore:int("strengthScore").default(0),
  createdAt:    timestamp("createdAt").defaultNow().notNull(),
});

// ─── CLAIM FORMS ─────────────────────────────────────────────────────────────

export const claimForms = mysqlTable("claim_forms", {
  id:              int("id").autoincrement().primaryKey(),
  claimId:         int("claimId").notNull().unique(),
  formType:        mysqlEnum("formType", [
    "va_21_526ez",   // Standard disability compensation
    "va_21_0781",    // PTSD personal statement
    "va_21_4142",    // Records release authorization
    "va_21_10210",   // Lay/witness statement
    "sf_180",        // Request for military records
  ]).default("va_21_526ez").notNull(),
  formData:        json("formData").notNull(),
  generatedPdfUrl: text("generatedPdfUrl"),
  generatedAt:     timestamp("generatedAt").defaultNow().notNull(),
  updatedAt:       timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

// Type exports
export type VAClaim       = typeof vaClaims.$inferSelect;
export type Condition     = typeof conditions.$inferSelect;
export type VADocument    = typeof vaDocuments.$inferSelect;
export type DevilLensCheck= typeof devilLensChecks.$inferSelect;
export type LegalTheory   = typeof legalTheories.$inferSelect;
export type ClaimForm     = typeof claimForms.$inferSelect;
