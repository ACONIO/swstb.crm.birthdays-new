-- Get E-Mail and date of birth for each client. --
SELECT
    per.PER_PERSONENID       AS "bmd_id",
    per.PER_FIRMENNR         AS "bmd_company_id",
    per.PER_GEBURTSDATUM     AS "dob"
FROM BUERO.PER_PERSON per
    JOIN BUERO.KLI_KUNDE_LIEFERANT kli  ON per.PER_PERSONENID = kli.KLI_KLID
                                        AND per.PER_FIRMENNR = kli.KLI_FIRMENNR
WHERE per.PER_FIRMENNR = 1
    AND per.PER_VORNAME IS NOT NULL
    AND per.PER_PERSONENID LIKE 'KL2000%%'
    AND kli.KLI_ISTAKTUELLKENNUNG = 1
    AND kli.KLI_ISTKUNDE = 1
    AND per.PER_GEBURTSDATUM IS NOT NULL
    AND per.PER_DISPLAY_EMAIL IS NOT NULL
    AND per.PER_DISPLAY_EMAIL NOT LIKE 'KA'
ORDER BY per.PER_NAME
;