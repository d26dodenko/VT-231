# Запуск лабораторной №3 (Windows)

Сначала проверяем локально, только затем переносим папки в существующую Git-ветку. Нужны Node.js 22, Python 3.11+ и MongoDB 7 (локальная служба или Docker Desktop).

## 1. Быстрый запуск unit-тестов

Откройте PowerShell в распакованной папке, содержащей `lab3`:

```powershell
cd lab3/shop/frontend
node -v
npm run test:unit:coverage
```

Unit-тесты не требуют `npm ci`. Для сборки и линтера зависимости обязательны:

```powershell
npm ci
npm run lint
npm run build
```

## 2. MongoDB

Если локально уже работает MongoDB на порту 27017, используйте её. Иначе при установленном Docker Desktop:

```powershell
docker run --name guziev-lab3-mongo -p 127.0.0.1:27017:27017 -d mongo:7
```

При повторном запуске существующего контейнера: `docker start guziev-lab3-mongo`.

## 3. Backend (отдельный PowerShell в lab3)

```powershell
cd shop/backend
npm ci
$env:PORT = '5001'
$env:MONGO_URI = 'mongodb://127.0.0.1:27017/guziev_lab3_local'
$env:JWT_SECRET = (node -e "process.stdout.write(require('node:crypto').randomBytes(32).toString('hex'))")
node scripts/seedProducts.js
node index.js
```

Не закрывайте терминал, пока идут тесты. Адрес проверки: `http://127.0.0.1:5001/`.

## 4. Frontend (второй PowerShell в lab3)

```powershell
cd shop/frontend
npm ci
npm run dev -- --host 127.0.0.1 --port 5173 --strictPort
```

Откройте `http://127.0.0.1:5173/products`. Должно быть четыре тестовых товара.

## 5. Python-тесты (третий PowerShell в lab3)

```powershell
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m pytest tests/integration -v --junitxml=reports/integration.xml
python -m pytest tests/e2e -v --junitxml=reports/e2e.xml
```

Для видимого браузера:

```powershell
$env:HEADED = '1'
python -m pytest tests/e2e -v
```

Для проверок безопасности и линтера:

```powershell
python -m ruff check tests
python -m bandit -r tests --severity-level high --confidence-level high --skip B101
```

В `shop/frontend` и `shop/backend` отдельно выполните `npm audit --audit-level=critical`.

## 6. GitHub

В существующем репозитории `C:\Users\pixel\Downloads\VT-231-guziev` переключитесь на `guziev_daniil/lab1` и проверьте `git status`. Скопируйте папку `lab3` и **содержимое `.github/workflows/ci.yml`** из архива в соответствующие пути репозитория. Не заменяйте папки `lab1`, `lab2` или корневой README; badge уже есть в `lab3/README.md`. В корневой README можно добавить ссылку на третью работу и badge, сохранив старый текст. Не копируйте `node_modules`, `.venv`, логи и отчёты из локального запуска.

```powershell
git branch --show-current
git status --short --untracked-files=all
```

Если активна `guziev_daniil/lab1`, а изменения относятся только к `lab3` и `.github/workflows/ci.yml`, добавьте их и проверьте staged:

```powershell
git add lab3 .github/workflows/ci.yml
git diff --cached --stat
git commit -m "Add lab3 UI tests and CI quality gates"
git push origin guziev_daniil/lab1
```

Новая ветка не нужна. Дальнейшие демонстрации quality gates описаны в README. Не изменяйте `main` и настройки защиты без разрешения преподавателя.
