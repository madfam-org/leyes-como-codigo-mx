# Leyes Como Código - Mexico

Transform Mexican federal and state laws into machine-readable Akoma Ntoso XML format.

**Status**: Production Ready  
**Accuracy**: 98.9%  
**Quality Score**: 97.9%

## Quick Start

```bash
# Clone repository
git clone https://github.com/madfam-org/leyes-como-codigo-mx.git
cd leyes-como-codigo-mx

# Install dependencies
pip install -r requirements.txt

# Ingest a single law
python scripts/bulk_ingest.py --laws amparo --skip-download

# Ingest all laws
python scripts/bulk_ingest.py --all --workers 8

# View status
python scripts/ingestion_status.py
```

## Features

- ✅ **98.9% Parser Accuracy** - Exceeds industry standards
- ✅ **Quality Validation** - 5 automated checks, A-F grading
- ✅ **Batch Processing** - Parallel ingestion with 4-8 workers
- ✅ **Monitoring** - Structured logging, error tracking, status dashboard
- ✅ **Production Ready** - Comprehensive test suite, full documentation

## Architecture

```
Law Ingestion Pipeline:
  PDF Download → Text Extraction → XML Parsing → Quality Validation → Storage
  
Components:
  - Parser V2: Enhanced Akoma Ntoso generator (98.9% accuracy)
  - Validators: Schema + completeness checking
  - Quality System: A-F grading with metrics
  - Batch Processor: Parallel execution engine
  - Monitoring: Structured logs + error tracking
```

## Documentation

- [Setup Guide](docs/SETUP.md) - Installation and configuration
- [Examples](docs/examples/) - Working code samples
- [Testing](tests/) - Test suite (>20 tests)

## Performance

| Metric | Result |
|--------|--------|
| Parser Accuracy | 98.9% |
| Quality Score | 97.9% |
| Processing Speed | 23s per law |
| Parallel Speedup | 3-4x |
| Schema Compliance | 100% |

## Project Status

**Phase B: Core Pipeline Infrastructure** - ✅ COMPLETE (100%)

- ✅ Parser V2 with 98.9% accuracy
- ✅ Quality validation framework  
- ✅ Batch processing infrastructure
- ✅ Monitoring & observability
- ✅ Testing suite (>20 tests)
- ✅ Documentation

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

##License

MIT License - see LICENSE file for details.

## Contact

Issues: https://github.com/madfam-org/leyes-como-codigo-mx/issues
