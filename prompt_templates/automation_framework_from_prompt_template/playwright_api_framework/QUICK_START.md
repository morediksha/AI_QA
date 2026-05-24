# Quick Start Guide - Get Running in 5 Minutes

## 1️⃣ Setup (2 minutes)

```bash
# Navigate to framework directory
cd playwright_api_framework

# Run automated setup
chmod +x setup.sh
./setup.sh

# Activate environment (if needed)
source venv/bin/activate
```

## 2️⃣ Configure (1 minute)

```bash
# Create .env file
cp .env.example .env

# Open and edit (optional - defaults work fine)
nano .env
```

## 3️⃣ Run Tests (2 minutes)

```bash
# Activate environment
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Or run with parallel execution
pytest tests/ -v -n 4

# Or run with HTML report
pytest tests/ --html=reports/report.html --self-contained-html
```

## ✅ Verify Success

You should see output like:
```
tests/test_posts_api.py::TestPostsAPI::test_get_all_posts PASSED
tests/test_posts_api.py::TestPostsAPI::test_get_specific_post PASSED
...
======================== 15 passed in 3.45s ========================
```

## 🎯 Common Tasks

| Task | Command |
|------|---------|
| Run smoke tests only | `pytest tests/ -m smoke -v` |
| Run specific test file | `pytest tests/test_posts_api.py -v` |
| Run with HTML report | `pytest tests/ --html=reports/report.html --self-contained-html` |
| Run parallel (4 workers) | `pytest tests/ -n 4 -v` |
| Debug failing test | `pytest tests/test_posts_api.py::TestPostsAPI::test_get_all_posts -vv -s` |
| Run with logs | `pytest tests/ -v --log-cli-level=DEBUG` |
| Generate Allure report | `pytest tests/ --alluredir=reports/allure && allure serve reports/allure` |

## 📚 Next Steps

1. **Understand the structure:** Read [README.md](README.md)
2. **Learn how to write tests:** Check [TESTING_GUIDE.md](TESTING_GUIDE.md)
3. **Follow best practices:** Review [BEST_PRACTICES.md](BEST_PRACTICES.md)
4. **Understand architecture:** See [ARCHITECTURE.md](ARCHITECTURE.md)
5. **Setup in CI/CD:** Use [.github/workflows/api-tests.yml](.github/workflows/api-tests.yml) or [Jenkinsfile](Jenkinsfile)

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `pytest not found` | `pip install -r requirements.txt` |
| `ModuleNotFoundError` | Ensure `source venv/bin/activate` is run |
| Tests timeout | Increase `RETRY_ATTEMPTS` and `RETRY_DELAY` in `.env` |
| Parallel tests fail | Run `pytest tests/ -v` without `-n` flag |

## 📖 Full Documentation

- [README.md](README.md) - Project overview
- [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) - Detailed setup
- [TESTING_GUIDE.md](TESTING_GUIDE.md) - Complete testing reference
- [BEST_PRACTICES.md](BEST_PRACTICES.md) - Writing good tests
- [ARCHITECTURE.md](ARCHITECTURE.md) - Framework design
- [.github/workflows/api-tests.yml](.github/workflows/api-tests.yml) - GitHub Actions CI/CD
- [Jenkinsfile](Jenkinsfile) - Jenkins CI/CD
- [Dockerfile](Dockerfile) & [docker-compose.yml](docker-compose.yml) - Docker setup

---

**You're all set! Happy testing! 🚀**
