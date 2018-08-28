# Load employer in-house activity filings (F635, Section P3D, line 3)
LOAD_EMPLOYER_ACTIVITIES_OTHER = """
INSERT INTO lobbying_activity (filing_id, amendment_id, form_type, entity_code, filer_id, filer_name, filer_last_name, filer_first_name, employer_id, employer_name, employer_last_name, employer_first_name, employer_city, employer_state, employer_zip, employer_phone, filing_date, start_date, end_date, lobbyer_id, lobbyer_name, lobbyer_last_name, lobbyer_first_name, lobbyer_city, lobbyer_state, lobbyer_zip, lobbyer_phone, type, interests, compensation, reimbursement, period_total, involved_entities)
SELECT
  covers."FILING_ID" AS filing_id,
  CAST (covers."AMEND_ID" AS INTEGER) AS amendment_id,
  covers."FORM_TYPE" AS form_type,
  covers."ENTITY_CD" AS entity_code,
  covers."FILER_ID" AS filer_id,
  covers."FILER_NAMF" || ' ' || covers."FILER_NAML" AS filer_name,
  covers."FILER_NAML" AS filer_last_name,
  covers."FILER_NAMF" AS filer_first_name,
  covers."FILER_ID" AS employer_id,
  covers."FILER_NAMF" || ' ' || covers."FILER_NAML" AS employer_name,
  covers."FILER_NAML" AS employer_last_name,
  covers."FILER_NAMF" AS employer_first_name,
  covers."FIRM_CITY" AS employer_city,
  covers."FIRM_ST" AS employer_state,
  covers."FIRM_ZIP4" AS employer_zip,
  covers."FIRM_PHON" AS employer_phone,
  covers."RPT_DATE" AS filing_date,
  covers."FROM_DATE" AS start_date,
  covers."THRU_DATE" AS end_date,
  -- still seems reasonable to name the employer as lobbyer
  -- in these "other payments to influence" types
  covers."FILER_ID" AS lobbyer_id,
  covers."FILER_NAMF" || ' ' || covers."FILER_NAML" AS lobbyer_name,
  covers."FILER_NAML" AS lobbyer_last_name,
  covers."FILER_NAMF" AS lobbyer_first_name,
  covers."FIRM_CITY" AS lobbyer_city,
  covers."FIRM_ST" AS lobbyer_state,
  covers."FIRM_ZIP4" AS lobbyer_zip,
  covers."FIRM_PHON" AS lobbyer_phone,
  'other' AS type,
  covers."LBY_ACTVTY" AS interests,
  summary."AMOUNT_A" AS compensation,
  '0.00' AS reimbursement,
  summary."AMOUNT_A" AS period_total,
  -- we will need to programmatically add session_total for these
  covers."FILER_NAMF" || ' ' || covers."FILER_NAML" AS involved_entities
FROM
  "CVR_LOBBY_DISCLOSURE_CD" covers
INNER JOIN
  "SMRY_CD" summary
    ON
      summary."FILING_ID" = covers."FILING_ID"
    AND
      summary."AMEND_ID" = covers."AMEND_ID"
WHERE
  covers."FORM_TYPE" = 'F635'
AND
  summary."FORM_TYPE" = 'F635P3D'
AND
  summary."LINE_ITEM" = '3'
AND
  summary."AMOUNT_A" > 0
ORDER BY
  covers."FILING_ID" DESC;
"""
