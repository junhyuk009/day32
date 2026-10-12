INSERT INTO shipping_quotes (title, weight_g, fee, calc_version, request_key)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (request_key) DO NOTHING
RETURNING id