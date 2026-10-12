SELECT id, title, weight_g, fee, calc_version, created_at
FROM shipping_quotes
ORDER BY id DESC
LIMIT 100