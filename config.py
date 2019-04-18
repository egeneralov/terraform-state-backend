from os import getenv

config = {
  'port': getenv('PORT', '80'),
  'database': getenv('DATABASE_URL', 'postgres://postgres@127.0.0.1:5432/postgres')
}
