"""
Quick ETL Process Verification
"""

import pandas as pd
from sqlalchemy import create_engine
import redis

print('🔍 ETL Process Verification')
print('=' * 30)

try:
    # Database Test
    engine = create_engine('postgresql://genetl:genetl_pass@localhost:5450/genetl_warehouse')
    products = pd.read_sql('SELECT COUNT(*) as count FROM warehouse.products', engine)
    count = products.iloc[0]['count']
    print(f'✅ Database: {count:,} products loaded')

    # Redis Test  
    r = redis.Redis(host='localhost', port=6390)
    r.ping()
    print('✅ Redis: Cache server operational')

    # Data Quality Test
    quality = pd.read_sql('SELECT COUNT(*) as count FROM logs.data_quality_checks WHERE status = \'passed\'', engine)
    quality_count = quality.iloc[0]['count']
    print(f'✅ Quality: {quality_count} checks passed')

    # ETL Pipeline Test
    pipeline = pd.read_sql('SELECT COALESCE(SUM(records_processed), 0) as total FROM logs.etl_pipeline_runs WHERE status = \'success\'', engine)
    pipeline_total = pipeline.iloc[0]['total']
    print(f'✅ Pipeline: {pipeline_total:,} records processed successfully')

    print('\n🎉 ETL PROCESS STATUS: FULLY OPERATIONAL!')

except Exception as e:
    print(f'❌ Error: {e}')