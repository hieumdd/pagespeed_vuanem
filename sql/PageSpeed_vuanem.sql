SELECT
    analysisUTCTimestamp AS ts,
    CAST(
        TIMESTAMP_TRUNC(analysisUTCTimestamp, DAY) AS date
    ) AS date,
    lighthouseResult.categories.performance.score
FROM
    `voltaic-country-280607.Ecom._ext_PageSpeed_vuanem`
